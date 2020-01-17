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

				
CP_Random = []
for i in range(10):
	CP_Random.append({})		
def get_random_books(n):
	books = []
	cur_file = open(str(os.getcwd())+'/'+ "CPDataforRandomBooksV2.txt", 'r')
	while True:
		temp = cur_file.readline()
		if(temp==""):
			break
		temp.strip()
		tmp = temp.split(" ")
		if(tmp[1] == '0' and len(books)<1000):
			books.append(tmp[0])
		CP_Random[int(tmp[1])][tmp[0]] = float(tmp[2])
	print(CP_Random)		
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

def get_recommended_books_with_dp(handle, UP, DB):
	cluster = ClusterUP(handle, UP)
	print(cluster)
	cl_members = get_cluster_members(cluster)
	
	tempdata = []
	currentBook = 0
	for book in DB:
		curbpath = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+book+'.txt'
		if(os.path.isfile(curbpath)==False):
			print("ERRORRRR: ", book)
			exit(0)
			continue
		with open(curbpath, "rb") as fp:
			BP = pickle.load(fp)
		result = 1 - spatial.distance.cosine(UP, BP)
			#print(str(result)+" 0 "+rating)
		if(currentBook == len(DB)-1):
			CP = get_CP_with_dp(cluster, book)
		else:
			CP = CP_Random[cluster][book]
		xdata = [result, CP]
		tempdata.append(xdata)
		#print(str(result)+" "+str(CP))
		currentBook +=1
	data = np.asarray(tempdata)
	prediction = model.predict(data)
	result_tupple = []
	for j in range(len(prediction)):
		exp_rating = 0
		for l in range(5):
			exp_rating += (l+1) * prediction[j][l]
		tup = (DB[j], data[j][0], data[j][1], exp_rating)
		result_tupple.append(tup)
	recommended_books_by_CS = sorted(result_tupple, key=lambda tup: tup[1],reverse = True)
	recommended_books_by_CP = sorted(result_tupple, key=lambda tup: tup[2],reverse = True)
	recommended_books_by_rating = sorted(result_tupple, key=lambda tup: tup[3],reverse = True)
	return (recommended_books_by_CS, recommended_books_by_CP, recommended_books_by_rating)


import getrandombooks as grb

LocalDB = get_random_books(1000)


yolo = 0
def get_minimum_req_with_dp(handle,UP, BookId):
	global yolo
	LocalDB.append(BookId)
	(recommend_CS, recommend_CP, recommend_rating) = get_recommended_books_with_dp(handle, UP, LocalDB)
	LocalDB.pop()
	
	
		
	for k in range(len(recommend_CS)):
		if(recommend_CS[k][0] == BookId):
			k_CS = k

	for k in range(len(recommend_CP)):
		if(recommend_CP[k][0] == BookId):
			k_CP = k
	for k in range(len(recommend_rating)):
		if(recommend_rating[k][0] == BookId):
			k_rating = k

	return (k_CS, k_CP, k_rating)

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

minimum_req_CS = []
minimum_req_CP = []
minimum_req_rating = []
words_count_limit=20000
big_profile =0
global_total = 0
for i in range(len(account_list)):
	if(global_total>340):
		break
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
		(UP, words_count) = UPMaker.MakeUP1(tw_content)
		if(words_count >= words_count_limit):
			big_profile+=1
			print(len(UP))
			if(np.array_equal(np.array(UP), np.array(zero)) == False):
				checkfile = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+temp[0]+'.txt'
				if(os.path.isfile(checkfile)!=False):
					(k_CS, k_CP, k_rating) = get_minimum_req_with_dp(account_list[i],UP,temp[0])
					minimum_req_CS.append(k_CS)
					minimum_req_CP.append(k_CP)
					minimum_req_rating.append(k_rating)
					user_total+=1
					global_total +=1
			
	
	cnt = 1
	while line:
		line = BR.readline().strip()
		if(line=="" or user_total ==10):
			break
		temp = line.split(" ")
		if(temp[1] == '5'):
			dateReadstr = temp[3]+" "+temp[4]+" "+temp[7]
			dateRead = get_datetime_from_GR(dateReadstr)
			print(dateRead)
			tw_content = get_custom_tw_profile(account_list[i], dateRead)
			(UP, words_count) = UPMaker.MakeUP1(tw_content)
			if(words_count >= words_count_limit):
				big_profile+=1
				print("now "+str(big_profile))
				print(len(UP))
				if(np.array_equal(np.array(UP), np.array(zero)) == False):
					checkfile = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+temp[0]+'.txt'
				if(os.path.isfile(checkfile)!=False):
					(k_CS, k_CP, k_rating) = get_minimum_req_with_dp(account_list[i],UP,temp[0])
					minimum_req_CS.append(k_CS)
					minimum_req_CP.append(k_CP)
					minimum_req_rating.append(k_rating)
					user_total+=1
					global_total +=1
			else:
				break
		cnt += 1

print(big_profile)	
resultFile = str(os.getcwd())+"/Experiment2_Newrun_withGR.txt"
FP = open(resultFile,'a+')
minimum_req_CS.sort()
minimum_req_CP.sort()
minimum_req_rating.sort()
total = len(minimum_req_CS)
median_CS = minimum_req_CS[int(total/2)]
Q1_CS = minimum_req_CS[int(total/4)]
Q3_CS = minimum_req_CS[total-int(total/4)]

median_CP = minimum_req_CP[int(total/2)]
Q1_CP = minimum_req_CP[int(total/4)]
Q3_CP = minimum_req_CP[total-int(total/4)]

median_rating = minimum_req_rating[int(total/2)]
Q1_rating = minimum_req_rating[int(total/4)]
Q3_rating = minimum_req_rating[total-int(total/4)]

FP.write("New Experiment:\n\n\n")

FP.write("For Cosine Similarity:\n\n")
FP.write(str(minimum_req_CS)+'\n\n\n')
FP.write(str(Q1_CS)+" "+str(median_CS)+" "+str(Q3_CS)+'\n\n\n')

FP.write("For Cluster Preference:\n\n")
FP.write(str(minimum_req_CP)+'\n\n\n')
FP.write(str(Q1_CP)+" "+str(median_CP)+" "+str(Q3_CP)+'\n\n\n')

FP.write("For Predicted Rating:\n\n")
FP.write(str(minimum_req_rating)+'\n\n\n')
FP.write(str(Q1_rating)+" "+str(median_rating)+" "+str(Q3_rating)+'\n\n\n')



exit
