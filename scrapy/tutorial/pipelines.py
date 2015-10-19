# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from MeteorClient import MeteorClient
# try to reconnect every second
client = MeteorClient('ws://127.0.0.1:3333/websocket', auto_reconnect=True, auto_reconnect_timeout=1)
client.connect()

def insert_callback(error, data):
    if error:
        print(error)
        return
    print(data)

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
        client.insert('listings', {
            'name': item['name'],
            'year_published':item['year_published'],
            'mfg_suggested_players':item['mfg_suggested_players'],
            'user_suggested_players':item['user_suggested_players'],
            'mfg_suggested_ages':item['mfg_suggested_ages'],
            'playing_time':item['playing_time'],
            'user_suggested_ages':item['user_suggested_ages'],
            'languages':item['languages'],
            'honors': item['honors'],
            'subdomains':item['subdomains'],
            'categories':item['categories'],
            'mechanics':item['mechanics'],
            'expansions':item['expansions'],
            'rank':item['rank'],
            'count_ratings':item['count_ratings'],
            'avg_ratings':item['avg_ratings'],
            'std_deviation':item['std_deviation'],
            'count_views':item['count_views']
            }, callback=insert_callback)
        self.exporter.export_item(item)

        # name = scrapy.Field()
        # year_published = scrapy.Field()
        # mfg_suggested_players = scrapy.Field()
        # user_suggested_players = scrapy.Field()
        # mfg_suggested_ages = scrapy.Field()
        # playing_time = scrapy.Field()
        # user_suggested_ages = scrapy.Field()
        # languages = scrapy.Field()
        # honors = scrapy.Field()
        # subdomains = scrapy.Field()
        # categories = scrapy.Field()
        # mechanics = scrapy.Field()
        # expansions = scrapy.Field()
        # rank = scrapy.Field()
        # count_ratings = scrapy.Field()
        # avg_ratings = scrapy.Field()
        # std_deviation = scrapy.Field()
        # count_views = scrapy.Field()
