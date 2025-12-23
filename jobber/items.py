# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossJobItem(scrapy.Item):
    job_title = scrapy.Field()  # 职位名称
    company = scrapy.Field()  # 公司名称
    keywords = scrapy.Field()  # 关键词标签
    description = scrapy.Field()  # 职位描述
    boss_name = scrapy.Field()  # 招聘者姓名
    boss_title = scrapy.Field()  # 招聘者职位
    detail_url = scrapy.Field()  # 详情页链接
