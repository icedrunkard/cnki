# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
#from cnki.settings import COLLECTION_NAME

class MongoPipeline(object):
    #collection_name = COLLECTION_NAME+'_papers2'

    def __init__(self,mongo_host):
        self.mongo_host=mongo_host
        #self.mongo_db=mongo_db

    @classmethod    
    def from_crawler(cls,crawler):
        return cls(
                mongo_host=crawler.settings.get('MONGO_HOST'),
                #mongo_db=crawler.settings.get('MONGO_DATABASE')
        )
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db = self.client[item['short']]
        self.collection_name=item['dpt']+'_papers1'
        self.db[self.collection_name].insert( dict(item))
        #self.db[self.collection_name].update({'paper_link': item['paper_link']}, dict(item), True)
        return item
