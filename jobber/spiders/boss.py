import scrapy
from scrapy_playwright.page import PageMethod

from ..items import BossJobItem  # 导入刚才定义的 Item


# 简化后的滚动脚本：使用原生 for 循环，减少 Promise 嵌套带来的上下文销毁风险
scroll_script = """
async () => {
    for (let i = 0; i < 20; i++) {
        window.scrollBy(0, 800);
        // 手动等待，不依赖复杂的 setInterval
        await new Promise(r => setTimeout(r, 1500));
        // 如果发现页面已经跳转（URL变了），主动停止防止报错
        if (!window.location.href.includes('jobs')) break;
    }
}
"""


class BossSpider(scrapy.Spider):
    name = "boss"
    allowed_domains = ["www.zhipin.com"]
    start_urls = [
        "https://www.zhipin.com/web/geek/jobs?query=python&city=101280600",
        "https://www.zhipin.com/web/geek/jobs?city=101280600&query=java",
        # "https://www.zhipin.com/web/geek/jobs?city=101280600&query=%E5%85%BC%E8%81%8C",
    ]

    # 必须保留这个入口，内部重定向到你的 start
    def start_requests(self):
        return self.start()

    async def start(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(
                url,
                callback=self.parse,
                # 给不同的搜索请求分配不同的优先级，数值越小越晚执行
                priority=100 - index, 
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", "delete navigator.__proto__.webdriver"),
                        PageMethod("wait_for_selector", ".rec-job-list", timeout=30000),
                        PageMethod("evaluate", scroll_script),
                        PageMethod("wait_for_timeout", 3000),
                    ],
                    "playwright_context_kwargs": {
                        "storage_state": "boss_state.json",
                    },
                    # 关键：每个搜索任务使用独立的浏览器上下文
                    "playwright_context": f"search_context_{index}",
                },
            )

    async def parse(self, response):
        # 增加一个保护判断
        if "security-check" in response.url:
            self.logger.error("糟糕！被重定向到了验证码页面")
            return

        jobs = response.css(".job-card-wrap")
        self.logger.info(f"成功进入解析函数，发现 {len(jobs)} 个职位")

        for job in jobs:
            item_link = job.css("a.job-name")
            job_title = item_link.css("::text").get()
            relative_url = item_link.css("::attr(href)").get()

            if relative_url:
                full_url = response.urljoin(relative_url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_detail,
                    priority=200,
                    meta={
                        "playwright": True,
                        "playwright_context": response.meta["playwright_context"],
                        "playwright_context_kwargs": {"storage_state": "boss_state.json"},
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", ".job-box", timeout=15000),
                            PageMethod("wait_for_timeout", 1200),
                        ],
                        "item": {
                            "job_title": job_title.strip() if job_title else "N/A",
                            "company": job.css(".boss-name::text").get(),
                        },
                    },
                )

    async def parse_detail(self, response):
        # 初始化 Item 对象
        item = BossJobItem()

        # 获取列表页传过来的数据
        list_data = response.meta.get("item", {})
        item["job_title"] = list_data.get("job_title")
        item["company"] = list_data.get("company")

        # 详情页提取
        item["keywords"] = response.css(".job-keyword-list li::text").getall()
        item["description"] = "".join(response.css(".job-sec-text::text").getall()).strip()

        # 招聘者信息
        boss_name = response.css(".job-boss-info .name::text").get()
        item["boss_name"] = boss_name.strip() if boss_name else "N/A"

        item["detail_url"] = response.url

        yield item  # 这个 item 会被送往 Pipeline
