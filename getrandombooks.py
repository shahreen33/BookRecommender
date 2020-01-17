import os

fname = str(os.getcwd())+ "/BookData/BookDatabase.txt"
fp = open(fname, 'r')
DB = [-1]*200000
line = "dummy"
count = 0
while line:
	line = fp.readline().strip()
	if(line == ""):
		break
	ID = fp.readline().strip()
	intid = int(ID)
	DB[intid] = 0
	

twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []
count = 0
for i in range(len(DB)):
	if(DB[i] == 0):
		count+=1
print(count)
	

count = 0
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


for i in range(len(account_list)):
	BRPath = str(os.getcwd())+'/UserData/BookRatingData/'+account_list[i]+'/BookRatingData.txt'
	if(os.path.isfile(BRPath)==False):
		continue
	BR = open(BRPath, 'r')
	line = "dummy"
	
	
	while line:
		line = BR.readline().strip()
		if(line== ""):
			break
		temp = line.split(" ")
		bookid = int(temp[0])
		DB[bookid] = 1
		
for i in range(len(DB)):
	if(DB[i] == 1):
		count+=1
print(count)

ValidBooks = []
for i in range(len(DB)):
	if(DB[i] == 0):
		ValidBooks.append(i)
print(len(ValidBooks))
import random

def get_random_books(n):
	cnt = 0
	RandomBooks = []
	while cnt < n:
		now = random.randrange(0, len(ValidBooks), 1)
	
		if(ValidBooks[now]==-1):
			continue
		RandomBooks.append(str(ValidBooks[now]))
		ValidBooks[now] = -1
		
		cnt += 1
	return RandomBooks
	
#print(get_random_books(1000))	
