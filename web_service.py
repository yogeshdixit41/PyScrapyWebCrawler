#!flask/bin/python
# @author : Yogesh (date : 28 march 2014 )
from flask import Flask, jsonify
import sys
import json
import difflib
from array import *
import datetime


app = Flask(__name__)


@app.route('/toi/<string:news_string>', methods = ['GET'])
def get_TOInews(news_string):



    item = [] # list for storing the final results
    ignore_this_words =['been','more','all','from','on','how','however','for','will','they','said','a','was','with','by','i','you','an','the','but','no','not','nor',
                        'which','where','what','who','when','why','either','has','had','neither','he','his','her','she','me','my','mine','them','their','there','that',
                        'this','then','of','as','if','do','in','it','is','to','and','at','also','its','every','be','off','have','are','here','being','later','could',
			'would','does','did','we','were','these','some','into','other','per','only','able','still','out','can','good','your','before','ever']



    with open('TodaysToiScrapedItemsOutput.json') as f: #load json file
	data = json.load(f)

    with open('toiNewsIndex.json') as f: #load json file
        data_1 = json.load(f)

    input_headline = news_string
    input_headline_list =  input_headline.split()
    temp_input_headline_list = []

    for each_word in input_headline_list:
	temp_input_headline_list.append(each_word)


    for each_word in temp_input_headline_list:
	if (each_word.lower() in ignore_this_words):
		input_headline_list.remove(each_word)


#print input_headline_list
#print temp_input_headline_list

    hit_cnt=0
    key_and_hit_cnt_dict={}
    key_and_location_dict={}
    cnt = 0
    for each_key in data_1:
        for each_word in input_headline_list:
            if(each_word.lower() in data_1[cnt]["key"]):
		hit_cnt = hit_cnt + 1	
	key_and_hit_cnt_dict[data_1[cnt]["key"]] = hit_cnt
        key_and_location_dict[data_1[cnt]["key"]] = data_1[cnt]["value"] 
	hit_cnt=0
        cnt = cnt +1


    sorted_keys_wrt_hitcnt = sorted(key_and_hit_cnt_dict, key= key_and_hit_cnt_dict.__getitem__,reverse=True)

    if(key_and_hit_cnt_dict[sorted_keys_wrt_hitcnt[0]] == 0): #check if first news has hit-count zero then no news match the given input
        item.append({'body':'No news found'})
        return jsonify({'item':item})
    
    i=0
    for each_entry in sorted_keys_wrt_hitcnt:
	if(i<5):
                if(key_and_hit_cnt_dict[each_entry] == 0):
                    pass
                else:
                    location=key_and_location_dict[each_entry]
		    item.append({ 'body' : data[location]["body"],'location':location,'key':each_entry,'words':input_headline_list})
		    i = i+1

    return jsonify({'item':item})
#END OF TOI



@app.route('/ht/<string:news_string>', methods = ['GET'])
def get_HTnews(news_string):



    item = [] # list for storing the final results
    ignore_this_words =['been','more','all','from','on','how','however','for','will','they','said','a','was','with','by','i','you','an','the','but','no','not','nor',
                        'which','where','what','who','when','why','either','has','had','neither','he','his','her','she','me','my','mine','them','their','there','that',
                        'this','then','of','as','if','do','in','it','is','to','and','at','also','its','every','be','off','have','are','here','being','later','could',
			'would','does','did','we','were','these','some','into','other','per','only','able','still','out','can','good','your','before','ever']



    with open('TodaysHtScrapedItemsOutput.json') as f: #load json file
	data = json.load(f)

    with open('htNewsIndex.json') as f: #load json file
        data_1 = json.load(f)

    input_headline = news_string
    input_headline_list =  input_headline.split()
    temp_input_headline_list = []

    for each_word in input_headline_list:
	temp_input_headline_list.append(each_word)


    for each_word in temp_input_headline_list:
	if (each_word.lower() in ignore_this_words):
		input_headline_list.remove(each_word)


#print input_headline_list
#print temp_input_headline_list

    hit_cnt=0
    key_and_hit_cnt_dict={}
    key_and_location_dict={}
    cnt = 0
    for each_key in data_1:
        for each_word in input_headline_list:
            if(each_word.lower() in data_1[cnt]["key"]):
		hit_cnt = hit_cnt + 1	
	key_and_hit_cnt_dict[data_1[cnt]["key"]] = hit_cnt
        key_and_location_dict[data_1[cnt]["key"]] = data_1[cnt]["value"] 
	hit_cnt=0
        cnt = cnt +1


    sorted_keys_wrt_hitcnt = sorted(key_and_hit_cnt_dict, key= key_and_hit_cnt_dict.__getitem__,reverse=True)


    if(key_and_hit_cnt_dict[sorted_keys_wrt_hitcnt[0]] == 0): #check if first news has hit-count zero then no news match the given input
        item.append({'body':'No news found'})
        return jsonify({'item':item})
    
    i=0
    for each_entry in sorted_keys_wrt_hitcnt:
	if(i<5):
                if(key_and_hit_cnt_dict[each_entry] == 0):
                    pass
                else:
                    location=key_and_location_dict[each_entry]
		    item.append({ 'body' : data[location]["body"],'location':location,'key':each_entry,'words':input_headline_list})
		    i = i+1

    return jsonify({'item':item})





if __name__ == '__main__':
    app.run(debug = True)
