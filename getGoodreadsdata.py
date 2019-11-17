import requests
import os

twId = []
grId = []
GRAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"

with open(GRAccounts) as fp:
   line = fp.readline().strip()
   temp = line.split(" ")
   twId.append(temp[0])
   grId.append(temp[1])
   while line:
       line = fp.readline().strip()
       if(line == ""):
       	break
       temp = line.split(" ")
       twId.append(temp[0])
       grId.append(temp[1])
      
       twId.append(temp[0])
       grId.append(temp[1])
       print(line)


print(grId)
N = len(grId)


for i in range(N):
	fname = str(os.getcwd())+"/UserRawData/RawGRData/"+ twId[i]+'_'+grId[i]+".xml"
	if(os.path.isfile(fname)==True):
		print("Already processed")
		continue
	requestURL = 'https://www.goodreads.com/review/list?key=IzTRndFKRignOkxxlNn0ng&v=2&id='+grId[i]+'&per_page=200&shelf=read&sort=date_added'
	res = requests.get(requestURL)
	print(res)
	print(fname)
	writer = open(fname, "w")
	cur = res.text
	#print(type(cur))
	writer.write(str(cur))

exit(0)


#

