import os
from langdetect import detect
import numpy as np


def RepresentsInt(s):
	for i in range(len(s)):
		try:
			print(s[i])
			int(s[i])
			return True
		except ValueError:
			return False


def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

fname = open(str(os.getcwd())+"/BookData/BookDatabase.txt", 'a+')
path = str(os.getcwd())+"/BookData/BookDescData/"
count = 0

DB = {}
for filename in os.listdir(path):
		if filename.endswith(".txt"):
			profile = str(os.getcwd())+"/BookData/BookProfiles/BookProfile_"+filename			
			fullname = str(os.getcwd())+"/BookData/BookMetaData/"+filename
			descName = str(os.getcwd())+"/BookData/BookDescData/"+filename
			if(os.path.isfile(profile)==False):
				try:
					print(fullname)
				except:
					continue
				print(descName)
				os.remove(fullname)
				os.remove(descName)
				continue

			f1 = open(fullname, 'r')
			bookName = f1.readline()
	
			key = bookName.strip()	
			temp = bookName.split(" by ")

			title = temp[0]
			author = temp[1]		   
			fnum = filename[4:-4]
			if(key in DB and DB[key]!=int(fnum)):
				#print(bookName)
				os.remove(fullname)
				os.remove(descName)
				continue
			if(key not in DB):
				DB[key] = int(fnum)
			#print(fnum)
			fname.write(bookName)
			fname.write(fnum+'\n')
			count +=1	
print(count)	
			
