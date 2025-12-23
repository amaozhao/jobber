import csv


class BossPipeline:
    def open_spider(self, spider):
        # 爬虫启动时创建文件
        self.file = open("boss_jobs.csv", "w", encoding="utf-8-sig", newline="")
        self.writer = csv.writer(self.file)
        # 写入表头
        self.writer.writerow(["职位名称", "公司", "关键词", "描述", "招聘者", "链接"])

    def process_item(self, item, spider):
        # 处理 item 数据并写入一行
        # 关键词列表转成逗号分隔的字符串
        keywords_str = ",".join(item.get("keywords", []))

        self.writer.writerow([
            item.get("job_title"),
            item.get("company"),
            keywords_str,
            item.get("description"),
            f"{item.get('boss', {}).get('boss_name')}({item.get('boss', {}).get('boss_title')})",
            item.get("detail_url"),
        ])
        return item

    def close_spider(self, spider):
        # 爬虫结束时关闭文件
        self.file.close()
