import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from chinaPro.items import ChinaproItem
from time import sleep

class ChinaSpider(CrawlSpider):
    name = 'china'
    # allowed_domains = ['www.china.com.cn']
    start_urls = ['http://app.tech.china.com.cn/news/my.php?cname=%E7%A7%91%E6%8A%80&p=']

    link = LinkExtractor(allow=r'cname=%E7%A7%91%E6%8A%80&p=\d+')
#http://tech.china.com.cn/elec/20210409/376154.shtml
    link_detail = LinkExtractor(allow=r'http://tech.china.com.cn/elec/.*?')
    print('可以的')

    rules = (
        Rule(link, callback='parse_item', follow=True),
        Rule(link_detail, callback='parse_detail')

    )
    # 创建redis链接对象
    conn = Redis(host='127.0.0.1', port=6379)

    def parse_item(self, response):
        # 注意：xpath表达式中不可以出现tbody标签
        print("我进来了")
        tr_list = response.xpath('/html/body/div[4]/div[1]/ul[1]/li')  # //*[@id="result"]/div[4]/h2/a
        # print(tr_list)
        for tr in tr_list:
            # new_title = tr.xpath('./h2/a//text()').extract()/html/body/div[4]/div[1]/ul[1]/li[1]/a
            detail_url = tr.xpath('./a[2]/@href').extract_first()
            print(detail_url)

            # 将详情页的url存入redis的set中
            ex = self.conn.sadd('urls', detail_url)
            if ex == 1:
                print('该url没有被爬取过，可以进行数据的爬取')
                yield scrapy.Request(url=detail_url, callback=self.parst_detail)
            else:
                print('数据还没有更新，暂无新数据可爬取！')

    # 解析详情页中的电影名称和类型，进行持久化存储
    def parst_detail(self, response):
        print("进入详情页")
        print(response.url)
        item = ChinaproItem()
        title = response.xpath('/html/body/div[4]/h1/text()').extract_first()
        new_content = response.xpath('//*[@id="fontzoom"]//text()').extract()
        content = ''.join(new_content)
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
            text = text.replace('\t', '')
            text = text.replace('\u3000', '')
            if text is '':
                continue
            string = string + text
        # print(string)
        content = string

        item['content'] = content
        item['title'] = title
        if item==None :
            ex = self.conn.SREM('urls', response.url)
        print(item)

        yield item

