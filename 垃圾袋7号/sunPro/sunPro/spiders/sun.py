import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver

class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.sun.com']
    start_urls = ['http://www.chinanews.com/']#/html/body/div[3]/div[3]/div[1]/div/a[4]
    models_urls = []  # 存储五个板块对应详情页的url

    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='/Users/wyw/Desktop/软件杯/爬虫/爬虫课件/第八章：scrapy框架/chromedriver')

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
