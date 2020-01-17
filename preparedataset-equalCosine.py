from scipy import spatial
import os
import pickle
import math
import time

zero = [0]*300

def normalize_cosine_similarity(x):
	return 0.5 *(x+1);
	
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
				result = normalize_cosine_similarity(result)
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
	return CP1	
				
		


NUM_CLUSTERS = 5
clusters_withGR = []
clusters_withoutGR = []
for i in range(NUM_CLUSTERS):
	cluster = str(os.getcwd())+'/'+ "Clusters/withGR/Cluster-"+str(i)+".txt"
	clusters_withGR.append(cluster)
	cluster = str(os.getcwd())+'/'+ "Clusters/withGR/Cluster-"+str(i)+".txt"
	clusters_withoutGR.append(cluster)




twitterAccounts = str(os.getcwd())+'/'+ "TrainUserAccounts.txt"
account_list = []


fname1 = str(os.getcwd())+'/'+ "traindataset_withGR_newV3.txt"
#fname2 = str(os.getcwd())+'/' +'traindataset_withoutGR.txt'
dataset1 = open(fname1, 'a+')
#dataset2 = open(fname2, 'a+')


debug = open("debug.txt", 'a+')
zero = [0] * 300
count = 0
countratings = [0, 0, 0, 0, 0]
clNum = 0

bookNum = 0
for cluster in clusters_withGR:
	print("Inside new cluster", clNum)
	clNum += 1
	account_list = []
	with open(cluster) as fp:
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
	acNum = 0
	
	for account in account_list:
		print("Working with new account:", acNum)
		acNum += 1
		twpath = str(os.getcwd())+'/UserData/UserProfiles_withGR/'+account+'.txt'
		ratingpath =  str(os.getcwd())+'/UserData/BookRatingData/'+account+'/BookRatingData.txt'
		if(os.path.isfile(ratingpath)==False):
			continue
		(readbooks,ratings) = get_readbooks(ratingpath)
		
		count_taken = 0
		for i in range(len(readbooks)):
			print("Working with new BOOK:", bookNum)
			
			curbpath = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+readbooks[i]+'.txt'
			if(os.path.isfile(curbpath)== False or ratings[i]=='0'):
				continue
			curr_rating = int(ratings[i])
			if(countratings[curr_rating-1]<=4000):
				CP = get_CP(account_list, readbooks[i])
				with open(twpath, "rb") as fp:
					UP = pickle.load(fp)
				with open(curbpath, "rb") as fp:
					BP = pickle.load(fp)
				result = 1 - spatial.distance.cosine(UP, BP)
				result = normalize_cosine_similarity(result)
				#print(str(result)+" 0 "+rating)
				
				countratings[curr_rating-1] +=1
				count = count+1	
				dataset1.write(str(result)+" "+str(CP)+" "+ratings[i]+'\n')
				bookNum += 1
				print(countratings)
				print("Remaining:", 20000-bookNum)
				count_taken += 1
				if count_taken >= 40:
					break
			
print("In with GR: ")
print(countratings)	

'''
countratings = [0,0,0,0,0]
for cluster in clusters_withoutGR:
	account_list = []
	with open(cluster) as fp:
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
	for account in account_list:
		#print(account)
		twpath = str(os.getcwd())+'/UserData/UserProfiles_withoutGR/'+account+'.txt'
		ratingpath =  str(os.getcwd())+'/UserData/BookRatingData/'+account+'/BookRatingData.txt'
		if(os.path.isfile(ratingpath)==False):
			continue
		reviewdata = get_readbooks(ratingpath)
		readbooks = reviewdata[0]
		ratings = reviewdata[1]
		bookNum = 0
		for i in range(len(readbooks)):
			curbpath = str(os.getcwd())+'/BookData/BookProfiles/BookProfile_Book'+readbooks[i]+'.txt'
			if(os.path.isfile(curbpath)== False or ratings[i]=='0'):
				continue
			CP = get_CP(account_list, readbooks[i])
			with open(twpath, "rb") as fp:
				UP = pickle.load(fp)
			with open(curbpath, "rb") as fp:
				BP = pickle.load(fp)
			result = 1 - spatial.distance.cosine(UP, BP)
			#print(str(result)+" 0 "+rating)
		
			countratings[int(ratings[i])-1] +=1
			count = count+1	
			dataset2.write(str(result)+" "+str(CP)+" "+ratings[i]+'\n')
			bookNum += 1
			if(bookNum >= 15):
				break

print("In without GR: ")
print(countratings)			
'''
