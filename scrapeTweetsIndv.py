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
auth_api = API(auth)

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
	x = csv_list[i]+".csv"
	print(x)
	if(os.path.isfile(x)==True):
		print("Already done")
		continue
	f = open('%s.csv' % (csv_list[i]), 'w')
	w = csv.writer(f)

	w.writerow(['timestamp', 'tweet_text', 'all_hashtags'])


	target = account_list[i]
	print("Getting data for " + target)
	item = auth_api.get_user(target)
	print("name: " + item.name)
	print("screen_name: " + item.screen_name)
	print("description: " + item.description)
	print("statuses_count: " + str(item.statuses_count))
	print("friends_count: " + str(item.friends_count))
	print("followers_count: " + str(item.followers_count))
	  
	w.writerow(['', str(item.description),''])
	tweet_count = 0
	for tweet in Cursor(auth_api.user_timeline, id=target).items():
		hashtags = []
		if hasattr(tweet, "entities"):
			entities = tweet.entities
		if "hashtags" in entities:
			for ent in entities["hashtags"]:
				if ent is not None:
					if "text" in ent:
						hashtag = ent["text"]
					if hashtag is not None:
		  				hashtags.append(hashtag)
		w.writerow([tweet.created_at, tweet.text.replace('\n',' '), hashtags])

	    
#print("All done. Processed " + str(tweet_count) + " tweets.")
