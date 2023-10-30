# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyDushuPipeline:
    def open_spider(self, spider):
        self.fp = open('dushu.txt', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item
    def close_spider(self, spider):
        self.fp.close()

import pymysql
#加载settings文件
from scrapy.utils.project import get_project_settings
class MysqlPipline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.db = settings['DB_NAME']
        self.port = settings['DB_PORT']
        self.charset = settings['DB_CHARSET']
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(host=self.host, 
                                    user=self.user, 
                                    password=self.password, 
                                    db=self.db, 
                                    charset=self.charset, 
                                    port=self.port)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        sql = 'insert into dushuwang(name,src) values("{}","{}")'.format(item['name'],item['src'])
        self.cursor.execute(sql)
        self.conn.commit()
        return item    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()