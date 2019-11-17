import pickle
from nltk.cluster import KMeansClusterer
import nltk
import os
import numpy as np
 
fname = str(os.getcwd())+"/UserAccounts.txt"
accountlist = []
filelist_withGR = []
filelist_withoutGR = []
accountfull = []

with open(fname) as fp:
	line = fp.readline().strip()
	accountfull.append(line)
	temp = line.split(" ")
	accountlist.append(temp[0])
	line = str(os.getcwd())+"/UserData/UserProfiles_combined/withGR/"+temp[0]+".txt"
	filelist_withGR.append(line)
	line = str(os.getcwd())+"/UserData/UserProfiles_combined/withoutGR/"+temp[0]+".txt"
	filelist_withoutGR.append(line)
	while line:
		line = fp.readline().strip()
		if(line == ""):
			break
		accountfull.append(line)
		temp = line.split(" ")
		accountlist.append(temp[0])
		
		line = str(os.getcwd())+"/UserData/UserProfiles_withGR/"+temp[0]+".txt"
		filelist_withGR.append(line)
		line = str(os.getcwd())+"/UserData/UserProfiles_withoutGR/"+temp[0]+".txt"
		filelist_withoutGR.append(line)

# get vector data

for i in range(len(accountlist)):
	with open(filelist_withGR[i], "rb") as fp:
		UP_withGR = pickle.load(fp)
	with open(filelist_withoutGR[i], "rb") as fp:
		UP_withoutGR = pickle.load(fp)
	if(i == 0):
		X1 = np.array([UP_withGR])
		X2 = np.array([UP_withoutGR])
	else:
		X1 = np.append(X1,[UP_withGR], axis = 0)
		X2 = np.append(X2,[UP_withoutGR], axis = 0)
	

print(X1) 
NUM_CLUSTERS=10
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters_withGR = kclusterer.cluster(X1, assign_clusters=True)
assigned_clusters_withoutGR = kclusterer.cluster(X2, assign_clusters=True)
clusters = [0,0,0,0,0,0,0,0,0,0]
for i in range(len(assigned_clusters_withGR)):
	filename = str(os.getcwd())+"/Clusters/withGR/Cluster-"+str(assigned_clusters_withGR[i])+".txt"
	fp = open(filename, 'a+')
	fp.write(accountfull[i]+'\n')
	clusters[assigned_clusters_withGR[i]] +=1 

print(clusters)
clusters = [0,0,0,0,0,0,0,0,0,0]
for i in range(len(assigned_clusters_withoutGR)):
	filename = str(os.getcwd())+"/Clusters/withoutGR/Cluster-"+str(assigned_clusters_withoutGR[i])+".txt"
	fp = open(filename, 'a+')
	fp.write(accountfull[i]+'\n')
	clusters[assigned_clusters_withoutGR[i]] +=1 

print(clusters)
 
exit(0)
 






