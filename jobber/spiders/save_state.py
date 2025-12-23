import asyncio
from playwright.async_api import async_playwright


async def save_login_state():
    async with async_playwright() as p:
        # 使用和你 Scrapy 配置一样的浏览器
        browser = await p.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=False
        )
        context = await browser.new_context()
        page = await context.new_page()

        # 访问登录页
        await page.goto("https://www.zhipin.com/web/user/login")

        print("请在弹出的浏览器中完成登录（扫码或验证码）...")

        # 循环检查，直到登录成功（比如看到了某个登录后的特有元素）
        # 这里等待 60 秒，足够你手动操作了
        try:
            await page.wait_for_selector(".nav-figure", timeout=60000)
            # 保存状态到 JSON 文件
            await context.storage_state(path="boss_state.json")
            print("登录成功！状态已保存到 boss_state.json")
        except Exception as e:
            print(f"登录超时或失败: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(save_login_state())
