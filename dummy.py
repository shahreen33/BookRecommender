import xml.etree.ElementTree as ET
import requests
import os
import csv
import re
import time
import tweepy
import ast
def twitter_user(username):
    consumer_key = "E1LzGWAStrYQ1hNjUBNRziDAb"
    consumer_secret = "AF7hqvrdufBFtTiGog55hJ4AIYwNP4y144ZkXlirR9ZrmceAMY"
    access_token = "1181492495412125696-fmaoPMwyI5nKEe6S0mEQ3aVfHwxYn8"
    access_token_secret = "85cGYR1WORBpdFPxVmyrbRjdHAw3j8mBd2sUHYmdn9kmr"
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    temp = {}
    #initialize Tweepy API
    api = tweepy.API(auth)
    item = api.get_user(username)
    temp['description'] = item.description
    temp['location'] = item.location
    return temp

def gr_user(username):
	fname = str(os.getcwd())+"/UserData/raws/"+ username+".xml"
	requestURL = 'https://www.goodreads.com/user/show/'+username+'.xml?key=IzTRndFKRignOkxxlNn0ng'
	res = requests.get(requestURL)	
	print(res)
	print(fname)
	cur = res.text
	writer = open(fname,'w')
	writer.write(cur)
	#print(fname)
	temp = {}
	try:
		tree = ET.parse(fname)
	except:
		temp['about'] = None
		temp['age'] =None
		temp['gender'] = None
		temp['location'] = None
		temp['interests'] = None
		return temp
	root = tree.getroot()
	print(root.tag)
	
	
	for child in root:
		if child.tag == 'user':
			for gchild in child:
				if gchild.tag == 'about':
					temp['about'] = gchild.text
				elif gchild.tag == 'age':
					temp['age'] = gchild.text
				elif gchild.tag == 'gender':
					temp['gender'] = gchild.text
				elif gchild.tag == 'location':
					temp['location'] = gchild.text
				elif gchild.tag == 'interests':
					temp['interests'] = gchild.text
	
			
	return temp


   

'''
handles = {}
keep = open(str(os.getcwd())+"/accounts.txt", 'a+')
with open('getdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
       # print(row[2])
        #print(line_count)
        if line_count == 0:
            line_count +=1
            continue
        else:
           handle =row[2]
           tweet = row[1]
           #print(handle)
           if handle not in handles:
                handles[handle] = tweet

           keep.write(row[2]+'\n')
           line_count +=1
		

print(len(handles))
new_handles = {}
i = 0
grrvw = open("test/rvw/rvws.txt", 'a+')
for handle in handles:
	tweet = handles[handle]
	try:
		url = re.search("(?P<url>https?://[^\s]+)", tweet).group("url")
	except:
		continue
	requestURL = url
	res = requests.get(requestURL)
	cur = res.text
	#writer = open("test/test"+str(i)+".xml",'w')
	#writer.write(cur)
	first = cur.find('/user/show/')
	print(first)
	if(first !=-1):
		last = first +200
		review = ""
		for i in range(first,last):
			if(cur[i] == '\"'):
				break
			review += cur[i]
		new_handles[handle] = review
		grrvw.write(handle+' '+review+'\n')
		#grrvw.write(review+'\n')
		print(review)
		time.sleep(1)
		i+=1
'''
grrvw = open(str(os.getcwd())+"/UserAccounts.txt", 'r')
new_handles = {}
line = grrvw.readline().strip()
while line:
	temp = line.split(" ")
	if(temp[0] not in new_handles):
		new_handles[temp[0]] = temp[1]
	line = grrvw.readline().strip()
print(len(new_handles))
#print(new_handles)


path1 = str(os.getcwd())+"/test/tw/"
path2 = str(os.getcwd())+ "/test/gr/"

	
            
freq = {}
freq['tw_description'] = 0
freq['location'] = 0
freq['about'] = 0
freq['age'] = 0
freq['gender'] = 0
freq['interests'] = 0
elig = open("eligibles.txt", 'a+')
count = 0
eligible = 0

for handle in new_handles:
	grid = new_handles[handle]

	
	
	fname1_mod = str(os.getcwd())+"/UserData/UserProfilesT2/tw/"+ handle+".txt"
	fname2_mod = str(os.getcwd())+"/UserData/UserProfilesT2/gr/"+grid+".txt"	
	try:
		x = open(fname1_mod, 'r')
		y = open(fname2_mod, 'r')
	except:
		continue
	print(fname1_mod)
	print(fname2_mod)
	tw_info = ast.literal_eval(x.read())
	gr_info = ast.literal_eval(y.read())
	
	
	count = 0
	if(tw_info['description']!='' or gr_info['about'] != None):
		freq['tw_description'] +=1
		count += 1
	if(tw_info['location']!='' or gr_info['location']!= None):
		freq['location'] +=1
		count +=1
	if(gr_info['age']!= None):
		freq['age'] +=1
		count+=1
	if(gr_info['gender']!= None):
		freq['gender'] +=1
	if(gr_info['interests']!= None):
		freq['interests'] +=1
		count+=1
	
	print(count)
	
	if(count >= 3):
		eligible += 1
		elig.write(handle+' '+grid+'\n')
	else:
		os.remove(fname1_mod)
		os.remove(fname2_mod)
	
print(freq)
print(eligible)


exit(0)

#key=IzTRndFKRignOkxxlNn0ng

