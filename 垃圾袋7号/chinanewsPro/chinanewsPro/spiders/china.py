import scrapy
from selenium import webdriver
from chinanewsPro.items import ChinanewsproItem

class ChinaSpider(scrapy.Spider):
    name = 'china'
    # allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/']
    models_urls = []

    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='/Users/wyw/Desktop/软件杯/爬虫/爬虫课件/第八章：scrapy框架/chromedriver')

    def parse(self, response):#//*[@id="nav"]/ul/li[7]/a
        li_list = response.xpath('//*[@id="nav"]/ul/li')
        alist = [5,7,8,12,13]
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract()[0]
            model_url = 'http:' +model_url
            print(model_url)
            self.models_urls.append(model_url)
        for url in self.models_urls:  # 对每一个板块的url进行请求发送
            yield scrapy.Request(url, callback=self.parse_model)



    # 每一个板块对应的新闻标题相关的内容都是动态加载
    def parse_model(self, response):  # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
        # response.xpath()
        div_list = response.xpath('//*[@id="ent0"]/li')#//*[@id="cont_1_1_2"]/div[5]
        for index in div_list:
            title = index.xpath('./div/div/div[1]/em/a//text()').extract_first()
            model_url = index.xpath('./div/div/div[1]/em/a/@href').extract_first()
            model_url = 'http:'+ model_url


            item = ChinanewsproItem()
            item['title'] = title
            item['model_url'] = model_url

            # 对新闻详情页的url发起请求
            yield scrapy.Request(url=model_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):  # 解析新闻内容
        content = response.xpath('//*[@id="cont_1_1_2"]/div[5]//text()').extract()
        content = ''.join(content)
        string = ''
        for text in content:
            # 替换空白字符
            text = text.replace('\n\t', '')
            text = text.replace('\r', '')
            text = text.replace('a-z', '')
            text = text.replace('A-Z', '')
            text = text.replace('//', '')
            text = text.replace('\r\n', '')
            text = text.replace('\n', '')
            text = text.replace('<', '')
            text = text.replace('>', '')
            text = text.replace('p', '')
            text = text.replace(' ', '')
            text = text.replace('\u3000', '')
            if text is '':
                continue
            string = string + text
        # print(string)
        content = string

        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()


