import os
import pickle
import numpy as np

fname = str(os.getcwd())+"/UserAccounts.txt"
accountlist = []
filelist1_withGR = []
filelist1_withoutGR = []
filelist2 = []
with open(fname) as fp:
	line = fp.readline().strip()
	temp = line.split(" ")
	accountlist.append(temp[0])
	line = str(os.getcwd())+"/UserData/UserProfilesT2/"+temp[0]+".txt"
	filelist2.append(line)
	line = str(os.getcwd())+"/UserData/UserProfiles_withGR/"+temp[0]+".txt"
	filelist1_withGR.append(line)
	line = str(os.getcwd())+"/UserData/UserProfiles_withoutGR/"+temp[0]+".txt"
	filelist1_withoutGR.append(line)
	while line:
		line = fp.readline().strip()
		if(line == ""):
			break
		temp = line.split(" ")
		accountlist.append(temp[0])
		line = str(os.getcwd())+"/UserData/UserProfilesT2/"+temp[0]+".txt"
		filelist2.append(line)
		line = str(os.getcwd())+"/UserData/UserProfiles_withGR/"+temp[0]+".txt"
		filelist1_withGR.append(line)
		line = str(os.getcwd())+"/UserData/UserProfiles_withoutGR/"+temp[0]+".txt"
		filelist1_withoutGR.append(line)

path1 = str(os.getcwd())+"/UserData/UserProfileT2/"


			
alpha = 0.7

for i in range(len(accountlist)):
	with open(filelist2[i], "rb") as fp:
		UP2 = pickle.load(fp)
	with open(filelist1_withGR[i], "rb") as fp:
		UP1_withGR = pickle.load(fp)
	with open(filelist1_withoutGR[i], "rb") as fp:
		UP1_withoutGR = pickle.load(fp)
	x1 = np.array(UP1_withGR)
	x2 = np.array(UP1_withoutGR)
	y = np.array(UP2)
	result1 = np.add(alpha * x1, (1-alpha)*y)
	result2 = np.add(alpha * x2, (1-alpha)*y)
	fileName =str(os.getcwd())+"/UserData/UserProfiles_combined/withGR/"+accountlist[i]+".txt"	
	with open(fileName, "wb") as fp:   #Pickling
		pickle.dump(result1, fp)
	fileName =str(os.getcwd())+"/UserData/UserProfiles_combined/withoutGR/"+accountlist[i]+".txt"
	with open(fileName, "wb") as fp:   #Pickling
		pickle.dump(result2, fp)
				
