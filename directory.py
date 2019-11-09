import os

twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []
with open(twitterAccounts) as fp:
   line = fp.readline().strip()
   account_list.append(line)
   while line:
       line = fp.readline().strip()
       if(line == ""):
       	break
       account_list.append(line)
      

for account in account_list:
	path = str(os.getcwd())+'/'+ "BookData2/"+account
	if not os.path.exists(path):
		os.mkdir(path)
