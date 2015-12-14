import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy.selector import Selector
from spidercrawler.items import *
import time

class hindustanTimesSpiderClass(CrawlSpider):
    name = "hindustantimes"
    allowed_domains = ["hindustantimes.com"]
    start_urls = ["http://m.hindustantimes.com/home.action"]
            
    def parse(self, response):
	sel = Selector(response)	
			
	print "Main Response Body", response
			
	
	for link in sel.xpath("//html/body/div[@class='page_wdh']/div[@class='both_margin']/div[@class='more']/div[@class='blu']/a/@href").extract():
		final_url = urlparse.urljoin(response.url, link)
		yield Request(final_url, callback=self.my_parse)
	for link in sel.xpath("//html/body/div[@class='page_wdh']/div[@class='both_margin']/div[@class='more']/div[@class='red']/a/@href").extract():
		final_url = urlparse.urljoin(response.url, link)
		yield Request(final_url, callback=self.my_parse)		
	for link in sel.xpath("//html/body/div[@class='page_wdh']/div[@class='both_margin']/div[@class='more']/div[@class='grn']/a/@href").extract():
		final_url = urlparse.urljoin(response.url, link)
		yield Request(final_url, callback=self.my_parse)
	for link in sel.xpath("//html/body/div[@class='page_wdh']/div[@class='both_margin']/div[@class='more']/div[@class='pur']/a/@href").extract():
		final_url = urlparse.urljoin(response.url, link)
		yield Request(final_url, callback=self.my_parse)
								
    def my_parse(self, response):
	self.log('Hi this is in first_parse and doing nothing') 
	sel = Selector(response)
	for ti in sel.xpath("//h2[@class='news_head_30']/a/text()").extract():
		#yield Item(title=ti)
		print "doing nothing"
	
	for url in sel.xpath("//h2[@class='news_head_30']/a/@href").extract():
		itemLink = urlparse.urljoin(response.url, url)	
		#yield Item(link=itemLink)	
		yield Request(itemLink, callback=self.second_parse)
		
    def second_parse(self, response):
	sel = Selector(response)
	self.log('A response from second_parse just arrived!')
	news=sel.xpath("//html/body/div[@class='page_wdh']/div[@class='both_margin']/div[@class='sty_box']/div[@class='sty_kicker']/p/text()").extract()
	yield Item(body=news)
	time.sleep(5) 	
	
