import os
import ast

fname = str(os.getcwd())+"/UserAccounts.txt"
grfiles = []
twfiles = []
with open(fname) as fp:
	line = fp.readline().strip()
	temp = line.split(" ")
	line = str(os.getcwd())+"/UserData/UserProfilesT2/gr/"+temp[1]+".txt"
	grfiles.append(line)
	line = str(os.getcwd())+"/UserData/UserProfilesT2/tw/"+temp[0]+".txt"
	twfiles.append(line)
	while line:
		line = fp.readline().strip()
		if(line == ""):
			break
		temp = line.split(" ")
		line = str(os.getcwd())+"/UserData/UserProfilesT2/gr/"+temp[1]+".txt"
		grfiles.append(line)
		line = str(os.getcwd())+"/UserData/UserProfilesT2/tw/"+temp[0]+".txt"
		twfiles.append(line)


for i in range(len(grfiles)):
	curg = grfiles[i]
	curgfp = open(curg, 'r')
	x = ast.literal_eval(curgfp.read())
	print(x['about'])
	curt = twfiles[i]
	curtfp = open(curt, 'r')
	y = ast.literal_eval(curtfp.read())
	print(y['description'])
	
	break

exit(0)
	
		
	
	


#ast.literal_eval(writer1.read())
