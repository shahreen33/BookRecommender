from scipy import spatial
import os
import pickle
import math

twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []

fname = str(os.getcwd())+'/'+ "dataset.txt"
dataset = open(fname, 'a+')

with open(twitterAccounts) as fp:
   line = fp.readline().strip()
   account_list.append(line)
   cnt = 1
   while line:
       line = fp.readline().strip()
       if(line == ""):
       	break
       account_list.append(line)
       cnt += 1
debug = open("debug.txt", 'a+')
zero = [0] * 300
count = 0
countratings = [0,0,0,0,0]
for account in account_list:
	#print(account)
	twpath = str(os.getcwd())+'/UserData/UserProfiles/'+account+'.txt'
	curbpath = str(os.getcwd())+'/BookData2/'+account+'/BookProfiles/'
	currpath = str(os.getcwd())+'/BookData2/'+account+'/BookRatingData/'
	with open(twpath, "rb") as fp:
		UP = pickle.load(fp)
	for filename in os.listdir(curbpath):
		if filename.endswith(".txt"):
			f1 = curbpath+filename
			with open(f1, "rb") as fp:
				BP = pickle.load(fp)
			result = 1 - spatial.distance.cosine(UP, BP)
			f2 = currpath+filename
			with open(f2, "r") as fp:
				rating = fp.readline().strip()
			#print(str(result)+" 0 "+rating)
			if(rating != '0'):
				countratings[int(rating)-1] +=1
				count = count+1	
				if(count == 2780):
					continue
				dataset.write(str(result)+" 1 "+rating+'\n')	

print(countratings)			

