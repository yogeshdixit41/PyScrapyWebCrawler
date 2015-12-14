import os
import json
from array import *
import codecs
import unicodedata
import difflib
import shelve
import simplejson
from nltk.corpus import stopwords





#function to initiate toi crawler
def crawl_toi_website():
    os.system('scrapy crawl timesnews')

#function to initiate ht crawler
def crawl_ht_website():
    os.system('scrapy crawl hindustantimes')

#function to parse the toiscrapeditems file and create toiscrapeditemsoutput 
def toi_parser():
    cnt2 = 0 # counter for iteration over JSON file
    omitString = "\r\n"
    doubleQuote = "\""

    try:
        destination = open("TodaysToiScrapedItemsOutput.json","w") # open JSON file for output
    except IOError:
        pass

    with open("TodaysToiScrapedItems.json","r") as f: #open and load input JSON file
        data = json.load(f)


    flag_is_first_body_tag = 0 # flag to determine whether its first body tag of the news
    flag_for_last_body_tag = 0 # special flag to check if last body tag of the document is \r\n 
    item = []

    for allBodyElement in data:
        if(flag_is_first_body_tag == 0): # if first body tag
            if(data[cnt2]["body"].find(omitString) != -1 ): # if first body tag is \r\n special condition for document starting with \r\n
                pass	
            else:       # if first body and not \r\n then write first opening body for the news
                flag_for_last_body_tag = 0
                news = data[cnt2]["body"].replace(doubleQuote,"")
                flag_is_first_body_tag = 1

	elif(flag_is_first_body_tag == 1): # not the first body of the news
            if(data[cnt2]["body"].find(omitString) != -1 ): # end of news found
                item.append({'body':news})
		flag_is_first_body_tag = 0
		flag_for_last_body_tag = 1
            else:  # in between body tags
		news = news +" "+data[cnt2]["body"].replace(doubleQuote,"")
			
        cnt2 = cnt2 + 1

    jsondata = simplejson.dumps(item, indent=1)
    destination.write(jsondata)
    destination.close()



#function to parse the htscrapeditems file and create htscrapeditemsoutput
def ht_parser():
    item = []
    cnt = 0
    my_news = ""
    doubleQuote = '\"'
    end_o_string = '\r\n'


    try:
        destination = open("TodaysHtScrapedItemsOutput.json","w") # open JSON file for output
    except IOError:
        pass

    with open('TodaysHtScrapedItems.json','r') as f: #load json file
        data = json.load(f)

    for dataobj in data:
        for news in data[cnt]["body"]:
            news = news.encode("utf-8")
	    news = news.replace(doubleQuote,"")
	    news = news.replace(end_o_string,"")
	    if(news !=""):
	        my_news = my_news +" "+ news
	item.append({'body':my_news})
        my_news = ""
	cnt= cnt + 1
    jsondata = simplejson.dumps(item, indent=1)
    destination.write(jsondata)
    destination.close()



#function to extract imp keywords from news
def extract_keywords(news):
    copy_of_all_words_in_news = []
    news_word_count_dict = {}
    ignore_this_words =stopwords.words('english')
    
    all_words_in_news = news.split()


    for word in all_words_in_news:
	copy_of_all_words_in_news.append(word.lower())
    
    for word in all_words_in_news:
	word = word.lower()
	if(word in ignore_this_words):
		copy_of_all_words_in_news.remove(word)
    for word in copy_of_all_words_in_news:
	if word not in news_word_count_dict.keys():
		news_word_count_dict[word] = copy_of_all_words_in_news.count(word)
    
    sorted_list_of_words = sorted(news_word_count_dict, key = news_word_count_dict.__getitem__)
    reverse_sorted_list_of_words = sorted(news_word_count_dict, key = news_word_count_dict.__getitem__,reverse = True)
    
    i=0
    index_key=""
    for word in reverse_sorted_list_of_words:
	if i<15:
		
		index_key += " " + word
		i=i+1
    i=0
    for word in sorted_list_of_words:
	if i<5:
		
		index_key += " " + word
		i=i+1
    index_key=index_key.encode("utf-8")
    return index_key



#function which creates one time TOI index file
def create_toi_index():
    index_list = []
    with open('TodaysToiScrapedItemsOutput.json') as f: #load json file
	data = json.load(f)

    try:
        destination = open('toiNewsIndex.json','w')
    except:
        pass

    news_content = ""

    ignore_this_characters = [',','.',';',':','\"','\'','?','(',')']

    cnt = 0
    for dataobj in data:
	if(data[cnt]["body"] != "\r\n"):
		news_content = data[cnt]["body"] 
		for character in ignore_this_characters:
			news_content = news_content.replace(character," ")
		key = extract_keywords(news_content)
        index_list.append({'key':key, 'value': cnt})
	cnt = cnt +1
        

    jsondata = simplejson.dumps(index_list, indent=1)
    destination.write(jsondata)
    destination.close()
    


#function which creates one time HT index file
def create_ht_index():
    index_list = []
    with open('TodaysHtScrapedItemsOutput.json') as f: #load json file
	data = json.load(f)

    try:
        destination = open('htNewsIndex.json','w')
    except:
        pass

    news_content = ""

    ignore_this_characters = [',','.',';',':','\"','\'','?','(',')']

    cnt = 0
    for dataobj in data:
	if(data[cnt]["body"] != "\r\n"):
		news_content = data[cnt]["body"] 
		for character in ignore_this_characters:
			news_content = news_content.replace(character," ")
		key = extract_keywords(news_content)
        index_list.append({'key':key, 'value': cnt})
	cnt = cnt +1

    jsondata = simplejson.dumps(index_list, indent=1)
    destination.write(jsondata)
    destination.close()

def main():
    
    crawl_toi_website()
    print "Toi website finished crawling"
    crawl_ht_website()
    print "HT website finished crawling"
    toi_parser()
    print "Toi website finished parsing"
    ht_parser()
    print "HT website finished parsing"
    create_toi_index()
    print "TOI index file created"
    create_ht_index()
    print "HT index file created"
	
if __name__ == "__main__":
    main()
                

