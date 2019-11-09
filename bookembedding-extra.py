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
    #data = remove_userNames(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
  # data = stemming(data)
    data = remove_punctuation(data)
   #data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
   # print("Data preprocessing done.")
    return data
def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []
csv_list = []
with open(twitterAccounts) as fp:
   line = fp.readline().strip()
   account_list.append(line)
   cnt = 1
   while line:
       print(line)
       line = fp.readline().strip()
       if(line == ""):
       	break
       account_list.append(line)
       cnt += 1

    #open the spreadsheet we will write to
print(account_list)

word2vecModel = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
wordVectors = word2vecModel.wv
dimension = word2vecModel.vector_size	
zeroVector = [0] * dimension

for account in account_list:
	path = str(os.getcwd())+'/BookData2/'+account+'/BookProfiles'
	if not os.path.exists(path):
		os.mkdir(path)
	directory = str(os.getcwd())+'/BookData2/'+account+'/BookDescData/'
	#folder_name = "BookData/BookDescData1"
	#directory = str(os.getcwd())+'/'+folder_name+'/'
	BookIds = []
	print(directory)
	filelist = []
	for filename in os.listdir(directory):
		if filename.endswith(".txt"):
			BookIds.append(filename)
			filelist.append(os.path.join(directory, filename))
			continue
		else:
			continue
	dataset = []
	dataset1 = []
	#print(BookIds)
	ValidBookIds = []
	valid = 0
	for filename in filelist:	
		f = open(filename, 'r')
		temp = f.read().strip()
		print("Now processing file:" +filename)
		temp = preprocess(temp)
		if(temp == ""):
			valid = valid + 1
			continue
		dataset.append(temp)
		ValidBookIds.append(BookIds[valid])
		valid = valid +1 

	print(len(ValidBookIds))
		
	#print(dataset)

	N = len(dataset)
	processed_text= []
	count = 0
	maxi = 0
	mini = 999999999
	minix = "nothing"
	for i in dataset[:N]:
		count = count+1
		print("Working on dataset : %d..." %(count)) 
		if maxi < len(i):
			maxi = len(i)
		if mini > len(i):
			mini = len(i)
			minix = filename
		processed_text.append(word_tokenize(i))

	#print(processed_text[0])
	print(maxi)
	print(mini)
	print(minix)
	print(N)
	
	#BookProfile = []


	for i in range(N):
		sz = len(processed_text[i])
		nparr = np.empty([1,dimension])
		for j in range(sz):
			word = processed_text[i][j]
			if word in wordVectors:
				if(j == 0):
					nparr[0] = wordVectors[word]
				else:
					nparr = np.vstack((nparr,wordVectors[word]))
			else: 
				if(j == 0):
					nparr[0] = zeroVector
				else:
					nparr = np.vstack((nparr,zeroVector))
			

		newarr = np.sum(nparr, axis=0)
		newarr = newarr / sz
		#print(topicVectors)
		#BookProfile.append(newarr)
		fileName =path+"/"+ValidBookIds[i]
		with open(fileName, "wb") as fp:   #Pickling
			pickle.dump(newarr, fp)
	'''
	testfile = str(os.getcwd())+"/BookData/BookProfiles/BookProfile_"+BookIds[6]
	with open(testfile, "rb") as fp:   # Unpickling 
		b = pickle.load(fp)


	print(b[255])
	'''
