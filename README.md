# Jobber - Boss直聘爬虫

一个基于 Scrapy + Playwright 的 Boss 直聘职位信息爬虫项目，支持自动登录和动态渲染页面爬取。

## 📋 项目简介

Jobber 是一个高效的 Boss 直聘爬虫项目，通过以下技术栈实现：

- **Scrapy**: 强大的网络爬虫框架，处理请求和响应管理
- **Playwright**: 现代化的浏览器自动化工具，支持动态渲染页面
- **Python 3.12**: 编程语言

该项目支持自动登录、页面滚动加载、数据提取等功能。

## 🚀 快速开始

### 前置要求

- Python 3.12+
- Chrome 浏览器
- pip 或 conda 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
Playwright install
```

依赖包括：
- `Scrapy==2.13.4` - 网络爬虫框架
- `playwright==1.57.0` - 浏览器自动化工具
- `scrapy-playwright==0.0.44` - Scrapy 与 Playwright 集成中间件
- `playwright-stealth==2.0.0` - 隐身模式扩展

### 使用步骤

#### 1. 保存登录状态

首先运行 `save_state.py` 脚本，完成 Boss 直聘登录并保存会话状态：

```bash
python jobber/spiders/save_state.py
```

脚本会：
- 打开 Chrome 浏览器访问登录页面
- 等待你手动完成登录（扫码或验证码）
- 自动保存登录状态到 `boss_state.json` 文件
- 超时时间为 60 秒

#### 2. 运行爬虫

登录状态保存成功后，运行爬虫脚本爬取职位信息：

```bash
scrapy crawl boss
```

爬虫会：
- 加载保存的登录状态
- 爬取指定城市和关键词的职位信息
- 自动处理页面滚动加载
- 提取并保存职位数据到 CSV 文件

## 📁 项目结构

```
jobber/
├── README.md                  # 项目文档
├── requirements.txt           # Python 依赖
├── scrapy.cfg                 # Scrapy 配置文件
├── boss_state.json            # 登录状态文件（运行后生成）
├── boss_jobs.csv              # 爬取的职位数据（运行后生成）
└── jobber/
    ├── __init__.py
    ├── items.py               # 数据模型定义
    ├── middlewares.py         # 中间件配置
    ├── pipelines.py           # 数据处理管道
    ├── settings.py            # Scrapy 设置
    └── spiders/
        ├── __init__.py
        ├── boss.py            # Boss 爬虫核心脚本
        └── save_state.py      # 登录状态保存脚本
```

## ⚙️ 配置说明

### settings.py 关键配置

- **USER_AGENT**: 浏览器标识符
- **ROBOTSTXT_OBEY**: 遵守 robots.txt
- **CONCURRENT_REQUESTS**: 并发请求数
- **PLAYWRIGHT_BROWSER_TYPE**: 使用 Chrome 浏览器
- **DOWNLOADER_MIDDLEWARES**: Playwright 中间件集成

### save_state.py 说明

该脚本用于首次登录并保存认证状态，包含以下步骤：

1. 启动 Chrome 浏览器
2. 访问 Boss 直聘登录页面
3. 等待用户手动登录（支持扫码或验证码）
4. 验证登录成功（检查特定元素出现）
5. 保存会话到 `boss_state.json`

### boss.py 爬虫说明

核心爬虫脚本包含：

- **多关键词搜索**: 支持 Python、Java 等不同岗位搜索
- **自动滚动加载**: 通过滚动触发无限加载
- **反爬虫对策**: 移除 webdriver 标识，添加随机延迟
- **数据提取**: 使用 CSS/XPath 选择器提取职位信息
- **CSV 导出**: 通过 pipelines 保存数据到 CSV 文件

## 📊 爬取数据

爬虫会将职位信息保存到 `boss_jobs.csv` 文件，包含以下字段：

- 职位名称
- 公司名称
- 薪资范围
- 工作地点
- 学历要求
- 工作经验
- 职位描述
- 职位标签

## ⚠️ 注意事项

1. **登录首次必做**: 首次使用必须运行 `save_state.py` 完成登录
2. **会话有效期**: `boss_state.json` 登录状态可能过期，需要重新登录
3. **爬虫礼仪**: 不要设置过小的延迟，避免对网站造成压力
4. **频率限制**: 建议在晚间运行爬虫，避免频繁请求导致 IP 被封
5. **反爬虫**: 网站可能更新反爬虫策略，需要及时调整代码

## 🔧 故障排查

| 问题 | 解决方案 |
|------|--------|
| 浏览器启动失败 | 检查 Chrome 浏览器路径是否正确 |
| 登录超时 | 增加 timeout 值或检查网络连接 |
| 爬虫无数据 | 检查选择器是否过期，验证登录状态 |
| 页面加载失败 | 检查 Playwright 依赖是否完整安装 |

## 📝 文件说明

- `items.py`: 定义 `BossJobItem` 数据模型，包含职位信息字段
- `pipelines.py`: 数据处理管道，将爬取的数据保存到 CSV 文件
- `middlewares.py`: 自定义中间件，处理请求头、代理等
- `boss_state.json`: Playwright 会话状态文件，包含登录 Cookie 和本地存储

## 📚 参考资源

- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Playwright 官方文档](https://playwright.dev/)
- [scrapy-playwright 中间件](https://github.com/scrapy-plugins/scrapy-playwright)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

Created with ❤️ for job hunters
