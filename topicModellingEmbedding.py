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
    print("Data preprocessing done.")
    return data
def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


alpha = 0.3
folder_name = "UserData/withGR"
directory = str(os.getcwd())+'/'+folder_name+'/'

print(directory)
filelist = []
accountlist = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        url = filename[:-4]
        accountlist.append(url)
        filelist.append(os.path.join(directory, filename))
        continue
    else:
        continue
dataset = []
print(accountlist)

c = 0
for filename in filelist:	
	f = open(filename, 'r')
	temp = f.read().strip()
	temp = preprocess(temp)
	dataset.append(temp)
	
#print(dataset)

N = len(dataset)
processed_text= []
count = 0
for i in dataset[:N]:
    count = count+1
    print("Working on dataset : %d..." %(count)) 
    processed_text.append(word_tokenize(str(i)))

DF = {}
fx = open("data2.txt", 'a+')
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
'''
for i in DF:
	if DF[i] >1:
		print(i)
'''
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

word2vecModel = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
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
	for j in range(topicWord):
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
		for k in range(topicWord):
			summ = summ + topicVectors[i][k][j]
		avg = summ/topicWord
		userProfile[i].append(avg)
	
	fileName =str(os.getcwd())+"/UserData/UserProfilesGR/"+accountlist[i]+".txt"	
	with open(fileName, "wb") as fp:   #Pickling
		pickle.dump(userProfile[i], fp)

