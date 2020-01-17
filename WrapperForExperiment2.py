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

model = load_model("withGRlinks.h5")
def get_datetime_from_GR(date_time_str):
	date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')

	#print('Date:', date_time_obj.date())
	#print('Time:', date_time_obj.time())
	#print('Date-time:', date_time_obj)
	return date_time_obj;

def get_datetime_from_TW(date_time_str):
	date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')

	#print('Date:', date_time_obj.date())
	#print('Time:', date_time_obj.time())
	#print('Date-time:', date_time_obj)
	return date_time_obj;

def get_custom_tw_profile(account_name, date):
	fname = str(os.getcwd())+"/UserRawData/"+ account_name+"_withGR.csv"
	tw_content = ""
	with open(fname) as csv_file:
		csv_reader = csv.reader(csv_file)
		line_count = 0
		for row in csv_reader:
			if(line_count == 0):
				line_count +=1
				continue		
			else:
				currdate = row[0]
				if(currdate==""):
					continue
				temp = currdate.split(" ")
				twdate = get_datetime_from_TW(temp[0])
				if((date-twdate).days >= 7):
					#print("not exceeded")
					tw_content += " "
					tw_content += row[1]	
				else:
					#print("exxxcedcd")
					continue
			line_count += 1
	return tw_content



zero = [0]*300
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

def get_CP(AC, bookId):
	CP = 0
	nowBook = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+bookId+'.txt'
	with open(nowBook, "rb") as fp:
		X = pickle.load(fp)
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
		CP += (maxi * maxir)
	
	CP1 = CP/len(AC)
	return CP1	

				
		
def pick_random_books(BookId, n):
	books = []
	cnt = 0
	while cnt <= n:
		now = random.randrange(0, len(BookDB),1)
		if(BookDB[now] != BookId):
			books.append(BookDB[now])
			cnt += 1
		else:
			continue
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

def ClusterUP(handle, UP):
	alpha = 0.7
	tempfile = str(os.getcwd())+"/UserData/UserProfilesT2/"+handle+".txt"
	with open(tempfile, "rb") as fp:
		UP2 = pickle.load(fp)
	x1 = np.array(UP)
	y = np.array(UP2)
	result1 = np.add(alpha * x1, (1-alpha)*y)
	maxi = -99
	maxir = -1
	for i in range(NUM_CLUSTERS):
		cluster = str(os.getcwd())+'/'+ "Clusters/withGR/Cluster-"+str(i)+"-Centroid.txt"
		fp = open(cluster, 'rb')
		centroid = pickle.load(fp)
		result = 1 - spatial.distance.cosine(result1, centroid)
		if maxi < result:
			maxi = result
			maxir = i
	return maxir
	
def get_recommended_books(handle, UP, DB):
	cluster = ClusterUP(handle, UP)
	print(cluster)
	cl_members = get_cluster_members(cluster)
	
	tempdata = []
	for book in DB:
		curbpath = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+book+'.txt'
		with open(curbpath, "rb") as fp:
			BP = pickle.load(fp)
		result = 1 - spatial.distance.cosine(UP, BP)
			#print(str(result)+" 0 "+rating)
		CP = get_CP(cl_members, book)
		xdata = [result, CP]
		tempdata.append(xdata)
		#print(str(result)+" "+str(CP))
	data = np.asarray(tempdata)
	prediction = model.predict(data)
	result_tupple = []
	for j in range(len(prediction)):
		exp_rating = 0
		for l in range(5):
			exp_rating += (l+1) * prediction[j][l]
		tup = (DB[j], exp_rating)
		result_tupple.append(tup)	
	recommended_books = sorted(result_tupple, key=lambda tup: tup[1],reverse = True)
	return recommended_books

		
		
	
	
def get_minimum_req(handle,UP, BookId):
	LocalDB = pick_random_books(BookId, 100)
	LocalDB.append(BookId)
	recommend = get_recommended_books(handle,UP, LocalDB)
	for k in range(len(recommend)):
		if(recommend[k][0] == BookId):
			return k
	

NUM_CLUSTERS = 10



twitterAccounts = str(os.getcwd())+'/'+ "TestUserAccounts.txt"
account_list = []



zero = [0] * 300
count = 0
countratings = [0,0,0,0,0]

with open(twitterAccounts) as fp:
		line = fp.readline().strip()
		temp = line.split(" ")
		account_list.append(temp[0])
		cnt = 1
		while line:
			line = fp.readline().strip()
			if(line == ""):
				break
			temp = line.split(" ")
			account_list.append(temp[0])
			cnt += 1
print(len(account_list))

minimum_req = []

for i in range(len(account_list)):
	BRPath = str(os.getcwd())+'/UserData/BookRatingData/'+account_list[i]+'/BookRatingData.txt'
	if(os.path.isfile(BRPath)==False):
		continue
	BR = open(BRPath, 'r')
	line = BR.readline().strip()
	temp = line.split(" ")
	print(account_list[i])
	user_total = 0
	if(temp[1] == '5'):
		dateReadstr = temp[3]+" "+temp[4]+" "+temp[7]
		dateRead = get_datetime_from_GR(dateReadstr)
		print(dateRead)
		tw_content = get_custom_tw_profile(account_list[i], dateRead)
		UP = UPMaker.MakeUP1(tw_content)
		print(len(UP))
		if(np.array_equal(np.array(UP), np.array(zero)) == False):
			k = get_minimum_req(account_list[i],UP,temp[0])
			print(k)
			minimum_req.append(k)
			user_total+=1
			
	
	cnt = 1
	while line:
		line = BR.readline().strip()
		if(line=="" or user_total == 4):
			break
		temp = line.split(" ")
		if(temp[1] == '5'):
			dateReadstr = temp[3]+" "+temp[4]+" "+temp[7]
			dateRead = get_datetime_from_GR(dateReadstr)
			print(dateRead)
			tw_content = get_custom_tw_profile(account_list[i], dateRead)
			UP = UPMaker.MakeUP1(tw_content)
			print(len(UP))
			if(np.array_equal(np.array(UP), np.array(zero)) == False):
				k = get_minimum_req(account_list[i],UP,temp[0])
				print(k)
				minimum_req.append(k)
				user_total+=1
		cnt += 1
	break
resultFile = str(os.getcwd())+"/ExperimentResults/Experiment2_1strun_withGR.txt"
FP = open(resultFile,'a+')
minimum_req.sort()
total = len(minimum_req)
median = minimum_req[int(total/2)]
Q1 = minimum_req[int(total/4)]
Q3 = minimum_req[total-int(total/4)]
FP.write("New Experiment:\n\n\n")
FP.write(str(minimum_req)+'\n\n\n')
FP.write(str(Q1)+" "+str(median)+" "+str(Q3)+'\n\n\n')



