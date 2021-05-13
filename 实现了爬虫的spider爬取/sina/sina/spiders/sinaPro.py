import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sina.items import SinaItem

class SinaproSpider(CrawlSpider):
    name = 'sinaPro'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=']

    # 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
    link = LinkExtractor(allow=r'pageid=153&lid=2509&k=&num=50&page=\d+')

    rules = (
        # 规则解析器：将链接提取器提取到的链接进行指定规则（callback）的解析操作
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 注意：xpath表达式中不可以出现tbody标签
        tr_list = response.xpath('//*[@id="d_list"]/ul[1]//li').extract()
        for tr in tr_list:
            new_url = tr.xpath('./span[2]/a/@href')[0]
            new_title = tr.xpath('./span[2]/a//text()').extract()
            item = SinaItem()
            item['title'] = new_title
            item['new_url'] = new_url

            yield item
