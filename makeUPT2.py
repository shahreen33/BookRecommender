from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
import string
import preprocessor as p

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
import collections
import gensim
import ast

def print_doc(id):
    print(dataset[id])
    file = open(dataset[id][0], 'r', encoding='cp1250')
    text = file.read().strip()
    file.close()
    print(text)

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text
   

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def remove_userNames(data):
	temp = " ".join(filter(lambda x:x[0]!='@', str(data).split()))
	return temp
	

def preprocess(data):
    data = re.sub(r"http\S+", "", data)
    data = data.encode('ascii', 'ignore').decode('ascii')
    data = convert_lower_case(data)
    data = remove_userNames(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
   # data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
   # data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    #print("Data preprocessing done.")
    return data
def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

fname = str(os.getcwd())+"/UserAccounts.txt"
grfiles = []
twfiles = []
accountlist = []
with open(fname) as fp:
	line = fp.readline().strip()
	temp = line.split(" ")
	accountlist.append(temp[0])
	line = str(os.getcwd())+"/UserData/UserProfilesT2/gr/"+temp[1]+".txt"
	grfiles.append(line)
	line = str(os.getcwd())+"/UserData/UserProfilesT2/tw/"+temp[0]+".txt"
	twfiles.append(line)
	while line:
		line = fp.readline().strip()
		if(line == ""):
			break
		temp = line.split(" ")
		accountlist.append(temp[0])
		line = str(os.getcwd())+"/UserData/UserProfilesT2/gr/"+temp[1]+".txt"
		grfiles.append(line)
		line = str(os.getcwd())+"/UserData/UserProfilesT2/tw/"+temp[0]+".txt"
		twfiles.append(line)

dataset = []
for i in range(len(grfiles)):
	curg = grfiles[i]
	curgfp = open(curg, 'r')
	x = ast.literal_eval(curgfp.read())
	curt = twfiles[i]
	curtfp = open(curt, 'r')
	y = ast.literal_eval(curtfp.read())
	about = x['about']
	description = y['description']
	interests = x['interests']
	data = ""
	if(about!=None):
		data +=about
	if(interests != None):
		data += " "+ interests
	if( description != None):
		data += " "+description
	
	dataset.append(preprocess(data))


#print(dataset)

N = len(dataset)
print(N)
processed_text= []
count = 0
for i in dataset[:N]:
    count = count+1
    print("Working on dataset : %d..." %(count-1)) 
    processed_text.append(word_tokenize(str(i)))

DF = {}
for i in range(N):
    tokens = processed_text[i]
    a = 0
    b = 0
    print(len(tokens))
    for w in tokens:
        try:
            DF[w].add(i)
            #fx.write("now a it is "+ str(w)+"and "+ str(DF[w])+" \n")
            a = a+1
        except:
            DF[w] = {i}
            #fx.write("now b it is "+ str(w)+ "and "+ str(DF[w])+" \n")
            b = b+1

#print(str(a)+" "+str(b))
for i in DF:
    DF[i] = len(DF[i])

total_vocab_size = len(DF)

#print(total_vocab_size)

total_vocab = [x for x in DF]
#print(DF)

doc = 0

tf_idf = {}
tf_idf_list = []
print(N)
print("hello")
for i in range(N):
    
    tokens = processed_text[i]
    counter = Counter(tokens)
    words_count = len(tokens)
    tf_idf_list.append([])
    for token in np.unique(tokens):
        tf = counter[token]/words_count
        df = doc_freq(token) 
        idf = np.log((N+1)/(df+1))
        
        tf_idf[doc, token] = tf*idf
        tf_idf_list[doc].append(( token, tf_idf[doc, token]))
      

    doc += 1

word2vecModel = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True, limit = 10000)
wordVectors = word2vecModel.wv
dimension = word2vecModel.vector_size	
zeroVector = [0] * dimension
topicVectors = []

#print(tf_idf_list)
tf_idf_sorted = []
topicWord = 10
topic = []
for i in range(N):
	taken = 0
	tf_idf_sorted.append([])
	topic.append([])
	tf_idf_sorted[i] = sorted(tf_idf_list[i], key=lambda tup: tup[1], reverse = True)
	for j in range(len(tf_idf_sorted[i])):
		if(taken == topicWord):
			break
		if(tf_idf_sorted[i][j][0] in wordVectors):
			topic[i].append(tf_idf_sorted[i][j][0])
			taken = taken + 1
		
		
print(topic)
		
for i in range(N):
	topicVectors.append([])
	for j in range(len(topic[i])):
		word = topic[i][j]
		if word in wordVectors:
			topicVectors[i].append(wordVectors[word])
		else: 
			topicVectors[i].append(zeroVector)

#print(topicVectors)

userProfile = []

for i in range(N):
	userProfile.append([])
	for j in range(dimension):
		summ = 0
		for k in range(len(topicVectors[i])):
			summ = summ + topicVectors[i][k][j]
		avg = summ/topicWord
		userProfile[i].append(avg)
	
	fileName =str(os.getcwd())+"/UserData/UserProfilesT2/"+accountlist[i]+".txt"	
	with open(fileName, "wb") as fp:   #Pickling
		pickle.dump(userProfile[i], fp)



exit(0)
	
		
	
	


#ast.literal_eval(writer1.read())
