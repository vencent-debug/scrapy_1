# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SinaproPipeline:
    conn = None

    def open_spider(self, spider):
        self.conn = spider.conn

    def process_item(self, item, spider):
        dic = {
            'title': item['title'],
            'content': item['content']
        }
        # print(dic)
        self.conn.lpush('sina', dic)
        return item

class LocaldownloadproPipeline:
    fp = None

    def open_spider(self,spider):
        print("本地开始爬虫")
        self.fp = open('./Sinanews.txt','w',encoding='utf-8')
    def process_item(self, item, spider):
        print(item)
        title = item['title']
        content = item['content']
        self.fp.write(title+'   '+content+'\n')

        return item

    def close_spider(self,spider):
        print('结束爬虫')
        self.fp.close()