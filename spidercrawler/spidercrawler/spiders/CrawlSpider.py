#@author:Yogesh@Arxxus TOI Crawler - 3 March 2014
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy.selector import Selector
from spidercrawler.items import *

class MySpider(CrawlSpider):
    name = 'timesnews'
    allowed_domains = ['timesofindia.com']
    start_urls = ['http://mobiletoi.timesofindia.com/mobile.aspx']
    global visited_urls 
    visited_urls = []
    

    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
	city_tag = 'Pune'
	counter = 0
	temp_counter = 0

        sel = Selector(response)
        item = Item()
        #item['id'] = sel.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
	for tagname in sel.xpath("//a[@class='pda']/text()").extract():
		temp_counter=temp_counter+1
		if tagname==city_tag:
			self.log('-------------------Hi,this is in if %s ---------' % tagname)
			#yield Item(name=tagname)
			break
	for link in sel.xpath("//a[@class='pda']/@href").extract():
		counter=counter+1
		if counter==temp_counter:
			self.log('-------------------Hi,this is in if %s ---------' % link)
			final_url = urlparse.urljoin(response.url, link)
			#yield Item(url=final_url)
			yield Request(final_url, callback=self.first_parse)

	
    def first_parse(self, response):
	cnt_break1 = 0
	cnt_break2 = 0
	global visited_urls
	self.log('Hi this is in first_parse and doing nothing') 
	sel = Selector(response)
	for ti in sel.xpath("//a[@class='pda']/text()").extract():
		cnt_break1= cnt_break1 +1
		#yield Item(title=ti)
		if(ti == "Pune Times"):
			break
	for url in sel.xpath("//a[@class='pda']/@href").extract():
		cnt_break2= cnt_break2 +1
		itemLink = urlparse.urljoin(response.url, url)
		visited_urls.append(itemLink)
		if(cnt_break2 == cnt_break1):
			break
		#yield Item(link=itemLink)	
		#yield Request(itemLink, callback=self.second_parse) 
	cnt_break2=0
	for url in sel.xpath("//a[@class='pda']/@href").extract():
		cnt_break2= cnt_break2 +1
		itemLink = urlparse.urljoin(response.url, url)	
		#yield Item(link=itemLink)	
		yield Request(itemLink, callback=self.second_parse)
		if(cnt_break2 == cnt_break1):
			break
		 
  
    def second_parse(self, response):
	global visited_urls
	sel = Selector(response)
	self.log('A response from second_parse just arrived!')
	#for head in sel.xpath("//b[@class='pda']/text()").extract():
		#yield Item(page_title=head)
	for url_desc in sel.xpath("//a[@class='pda']/@href").extract():
		itemLinkDesc = urlparse.urljoin(response.url, url_desc)
		if(itemLinkDesc in visited_urls):
			continue	
		else:		
			#yield Item(desc_link=url_desc)	
			yield Request(itemLinkDesc, callback=self.third_parse)	

    def third_parse(self, response):
	end_str = "\r\n"
	sel = Selector(response)
	self.log('ENTERED ITERATION OF MY_PARSE_DESC!')
	for body_text in sel.xpath("//font[@class='pda']/text()").extract():
		yield Item(body=body_text)
	yield Item(body=end_str)	     
        
