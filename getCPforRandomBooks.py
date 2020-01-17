from scipy import spatial
import os
import pickle
import math
import time
import random
import keras
import csv

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from keras.models import load_model

import datetime
import MakeUPforTest as UPMaker
import numpy as np

NUM_CLUSTERS = 5

BookDB = []
BookDataBase = str(os.getcwd())+"/BookData/BookDatabase.txt"
with open(BookDataBase) as fp:
	name = fp.readline().strip()
	ID = fp.readline().strip()
	BookDB.append(ID)
	while name:
		name = fp.readline().strip()
		if(name == ""):
			break
		ID = fp.readline().strip()
		BookDB.append(ID)

model = load_model("withGRlinks16kdata.h5")

def get_readbooks(filename):
	booklist = []
	bookrating = []
	with open(filename) as fp:
		line = fp.readline().strip()
		temp = line.split(" ")
		booklist.append(temp[0])
		bookrating.append(temp[1])
		cnt = 1
		while line:
			line = fp.readline().strip()
			if(line == ""):
				break
			temp = line.split(" ")
			booklist.append(temp[0])
			bookrating.append(temp[1])
			cnt += 1
	return(booklist, bookrating)
dpCP = []
for i in range(NUM_CLUSTERS):
	dpCP.append({})
	
def get_CP_with_dp(clusterId, bookId):
	if(bookId in dpCP[clusterId]):
		return dpCP[clusterId][bookId]
	
	AC = get_cluster_members(clusterId)
	CP = 0
	nowBook = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+bookId+'.txt'
	with open(nowBook, "rb") as fp:
		X = pickle.load(fp)
	total_users = 0
	for member in AC:
		rp =  str(os.getcwd())+'/UserData/BookRatingData/'+member+'/BookRatingData.txt'
		if(os.path.isfile(rp)==False):
			continue
		rd = get_readbooks(rp)
		books = rd[0]
		rt = rd[1]
		if(rt == "0"):
			continue
		maxi = -1
		maxir = 0
		for i in range(len(books)):
			curbpath = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+books[i]+'.txt'
			if(os.path.isfile(curbpath)==False):
				continue
			with open(curbpath, "rb") as fp:
				BP = pickle.load(fp)
				result = 1 - spatial.distance.cosine(X, BP)
				if(result > maxi):
					maxi = result
					maxir = int(rt[i])
		if maxi > 0.3:		
			CP += (maxi * maxir)
			total_users += 1
	if(total_users == 0):
		CP1 = 3
		print("Found No similar books!!")
	else:
		CP1 = CP/total_users
	dpCP[clusterId][bookId] = CP1
	return CP1	

				
		
def pick_random_books(n):
	books = []
	cnt = 0
	while cnt <= n:
		now = random.randrange(0, len(BookDB),1)
		books.append(BookDB[now])
		cnt += 1
		
	return books

def get_cluster_members(Cluster_No):
	cluster = str(os.getcwd())+'/'+ "Clusters/withGR/Cluster-"+str(Cluster_No)+".txt"
	accounts = []
	with open(cluster) as fp:
		line = fp.readline().strip()
		temp = line.split(" ")
		accounts.append(temp[0])
		cnt = 1
		while line:
			line = fp.readline().strip()
			if(line == ""):
				break
			temp = line.split(" ")
			accounts.append(temp[0])
			cnt += 1
	return accounts






import getrandombooks as grb
Path = str(os.getcwd())+'/'+ "CPDataforRandomBooksV2.txt"
FP = open(Path, 'a+')
LocalDB = grb.get_random_books(1000)

for i in range(NUM_CLUSTERS):
	for j in range(len(LocalDB)):
		BookId = LocalDB[j]
		Curr_CP = get_CP_with_dp(i, BookId)
		FP.write(BookId+" "+str(i)+" "+str(Curr_CP)+"\n")	
	


