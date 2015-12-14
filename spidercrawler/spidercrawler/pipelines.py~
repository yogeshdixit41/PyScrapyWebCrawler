# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# @Himanshu : 19 Feb 2014
#@author : Yogesh@Arxxus - updated (3 march 2014)
# Create a file to collect the crawled data

from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.exporter import JsonItemExporter




class SpidercrawlerPipeline(object):
	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.files = {}
		#file = open('ScrapedItems.json', 'w+b')
		self.exporter = JsonItemExporter(file)
	
	def spider_opened(self, spider):
		if(spider.name == 'timesnews'):
			file = open('TodaysToiScrapedItems.json', 'w+b')
		else :
			file = open('TodaysHtScrapedItems.json', 'w+b')
		self.files[spider] = file
		self.exporter = JsonItemExporter(file)
		self.exporter.start_exporting()
	
	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()
		
	def process_item(self, item, spider):
		self.exporter.export_item(item)
	        return item
