# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from MeteorClient import MeteorClient
# try to reconnect every second
#client = MeteorClient('ws://127.0.0.1:3333/websocket', auto_reconnect=True, auto_reconnect_timeout=1)
client = MeteorClient('ws://127.0.0.1:3004/websocket', auto_reconnect=True, auto_reconnect_timeout=1)
client.connect()

def insert_callback(error, data):
    if error:
        print(error)
        return
    print(data)

def item_to_dictionary(item,keys):

    dictionary = {}

    for key in keys:
        if (key in item.keys()):
            dictionary[key] = item[key]
        else :
            dictionary[key] = 'null'

    return dictionary

class GameListingPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):

        keys = ['name','address','zipCode','jobCostMin','jobCostMax',
            'contactName','contactPhone','website','licenseNumber',
            'averageRating','profileUrl','followers','following',
            'badgeCount','projectCount','reviewCount','commentCount']
        dictionary = item_to_dictionary(item,keys)
        print 'document to insert',dictionary
        client.insert('listings', dictionary, callback=insert_callback)

        self.exporter.export_item(item)
