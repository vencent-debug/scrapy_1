# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class ChinanewsproPipeline:
    fp = None

    def open_spider(self,spider):
        print("开始爬虫")
        self.fp = open('./chinanews.txt','w',encoding='utf-8')
    def process_item(self, item, spider):
        print(item)
        title = item['title']
        content = item['content']
        model_url = item['model_url']
        self.fp.write(title+'   '+content+'\n')

        return item

    def close_spider(self,spider):
        print('结束爬虫')
        self.fp.close()
class mysqlPileLine:
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='00000000',db='china',charset='utf8')

    def process_item(self,item,spider):
        self.cursor = self.conn.cursor()
        try:

             self.cursor.execute('insert into china values("%s","%s")'%(item["title"],item["content"]))
             self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()


