# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SinaPipeline:
    fp = None

    def open_spider(self, spider):
        print("开始爬虫")
        self.fp = open('./sinanews.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        print(item)
        title = item['new_title']

        new_url = item['new_url']
        self.fp.write(title + '   ' + new_url + '\n')

        return item

    def close_spider(self, spider):
        print('结束爬虫')
        self.fp.close()