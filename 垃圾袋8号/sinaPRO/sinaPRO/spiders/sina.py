import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from sinaPRO.items import SinaproItem
from time import sleep

class SinaSpider(CrawlSpider):
    name = 'sina'
    # allowed_domains = ['www.sina.com']
    start_urls = ['https://search.sina.com.cn/?q=%e8%b4%a2%e7%bb%8f&c=news&from=home&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=']
    link = LinkExtractor(
        allow=r'q=%e8%b4%a2%e7%bb%8f&c=news&from=home&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=\d+')
    link_detail = LinkExtractor(allow=r'\w+.sina.com.cn/\w+/\w+/\d+/\w+')

    rules = (
        Rule(link, callback='parse_item', follow=True),
        # follow=True：可以将链接提取器 继续作用到 连接提取器提取到的链接 所对应的页面中
        Rule(link_detail, callback='parse_detail')
        # #follow=True：可以将链接提取器 继续作用到 连接提取器提取到的链接 所对应的页面中
    )
    # 创建redis链接对象
    conn = Redis(host='127.0.0.1', port=6379)

    def parse_item(self, response):
        # 注意：xpath表达式中不可以出现tbody标签
        print("我进来了")
        tr_list = response.xpath('//*[@id="result"]/div')  # //*[@id="result"]/div[4]/h2/a
        # print(tr_list)
        for tr in tr_list[4:]:
            # new_title = tr.xpath('./h2/a//text()').extract()
            detail_url = tr.xpath('./h2/a/@href').extract_first()

            # 将详情页的url存入redis的set中
            ex = self.conn.sadd('urls', detail_url)
            if ex == 1:
                print('该url没有被爬取过，可以进行数据的爬取')
                yield scrapy.Request(url=detail_url, callback=self.parst_detail)
            else:
                print('数据还没有更新，暂无新数据可爬取！')

    # 解析详情页中的电影名称和类型，进行持久化存储
    def parst_detail(self, response):
        item = SinaproItem()
        title = response.xpath('/html/body/div[3]/h1/text()').extract_first()
        new_content = response.xpath('//*[@id="artibody"]/p//text()').extract()
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
            text = text.replace('\u3000', '')
            if text is '':
                continue
            string = string + text
        # print(string)
        content = string

        item['content'] = content
        item['title'] = title
        print(item)

        yield item
