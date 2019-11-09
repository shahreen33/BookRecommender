import csv
import os

twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []
csv_list = []

with open(twitterAccounts) as fp:
   line = fp.readline().strip()
   account_list.append(line)
   line = str(os.getcwd())+'/UserRawData/'+line
   cnt = 1
   csv_list.append(line)
   while line:
       print(line)
       line = fp.readline().strip()
       if(line == ""):
       	break
       account_list.append(line)
       line = str(os.getcwd())+'/UserRawData/'+line
       csv_list.append(line)
       cnt += 1

    #open the spreadsheet we will write to
print(account_list)
print(csv_list)

for i in range(len(account_list)):
	fname = csv_list[i]+".csv"
	outputfile = str(os.getcwd())+'/UserData/'+account_list[i]+".txt"
	if(os.path.isfile(outputfile)==True):
		print("Already Processed")
		continue
	f = open(outputfile,'a+')

	with open(fname) as csv_file:
		csv_reader = csv.reader(csv_file)
		line_count = 0
		for row in csv_reader:
			if(line_count == 0):
				line_count +=1
				continue			
			else:
				f.write(" ")
				f.write(row[1])	
			line_count += 1
		
	print(f'Processed {line_count} lines.')
