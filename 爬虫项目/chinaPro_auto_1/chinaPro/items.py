# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinaproItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    label = scrapy.Field()
