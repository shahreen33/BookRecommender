from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import csv
import os

consumer_key = "E1LzGWAStrYQ1hNjUBNRziDAb"
consumer_secret = "AF7hqvrdufBFtTiGog55hJ4AIYwNP4y144ZkXlirR9ZrmceAMY"
access_token = "1181492495412125696-fmaoPMwyI5nKEe6S0mEQ3aVfHwxYn8"
access_token_secret = "85cGYR1WORBpdFPxVmyrbRjdHAw3j8mBd2sUHYmdn9kmr"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth,wait_on_rate_limit=True)

twitterAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
account_list = []
csv_list = []
with open(twitterAccounts) as fp:
   line = fp.readline().strip()
   temp = line.split(" ")
   account_list.append(temp[0])
   x = str(os.getcwd())+'/UserRawData/'+temp[0]
   cnt = 1
   csv_list.append(x)
   while line:
       line = fp.readline().strip()
       if(line == ""):
       	break
       temp = line.split(" ")
       account_list.append(temp[0])
       x = str(os.getcwd())+'/UserRawData/'+temp[0]
       csv_list.append(x)
       cnt += 1

    #open the spreadsheet we will write to
print(account_list)
print(csv_list)
forbidden = "goodreads.com"

for i in range(len(account_list)):
	x = csv_list[i]+"_withGR.csv"
	y = csv_list[i]+"_withoutGR.csv"
	print(x)
	if(os.path.isfile(x)==True):
		print("Already done")
		continue
	f1 = open(x, 'w')
	w1 = csv.writer(f1)
	f2 = open(y, 'w')
	w2 = csv.writer(f2)	
	w1.writerow(['timestamp', 'tweet_text'])
	w2.writerow(['timestamp', 'tweet_text'])


	target = account_list[i]
	print("Getting data for " + target)
	item = auth_api.get_user(target)
	print("name: " + item.name)
	print("screen_name: " + item.screen_name)
	#print("description: " + item.description)
	print("statuses_count: " + str(item.statuses_count))
	#print("friends_count: " + str(item.friends_count))
	#print("followers_count: " + str(item.followers_count))
	  
	w1.writerow(['', str(item.description),''])
	w2.writerow(['', str(item.description),''])
	tweet_count = 0
	for tweet in Cursor(auth_api.user_timeline, id=target).items():
		if(forbidden not in tweet.text):
			w2.writerow([tweet.created_at, tweet.text.replace('\n',' ')])
		w1.writerow([tweet.created_at, tweet.text.replace('\n',' ')])
#print("All done. Processed " + str(tweet_count) + " tweets.")
