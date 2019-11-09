import xml.etree.ElementTree as ET
import re
import os

twId = []
grId = []
GRAccounts = str(os.getcwd())+'/'+ "UserAccounts.txt"
xmlsrc = str(os.getcwd())+"/UserRawData/RawGRData/"
bookDB = str(os.getcwd())+'/BookData/BookDatabase.txt'

DB = {}
maxi = 0
with open(bookDB) as fp:
	b = fp.readline().strip()
	val = fp.readline().strip()
	if(b not in DB):
		DB[b] = val
	if(maxi<int(val)):
		maxi = int(val)        
	while True:
		b = fp.readline().strip()
		val = fp.readline().strip()
		if(b==""):
			break	
		if(b not in DB):
			DB[b] = val
		if(maxi<int(val)):
			maxi = int(val)   

print((DB))
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

addDB = open(bookDB,'a+')
N = len(grId)

for user in range(N):

	path = str(os.getcwd())+"/UserData/"+twId[user]
	if( not os.path.exists(path)):
		os.mkdir(path)
	

	TAG_RE = re.compile(r'<[^>]+>')

	def remove_tags(text):
	    return TAG_RE.sub('', text)

	fname = xmlsrc+twId[user]+"_"+grId[user]+".xml"
	print(fname)
	tree = ET.parse(fname)
	root = tree.getroot()

	

	read_books = []
	i = 0
	print(len(read_books))
	for review in root.iter('review'):
		temp = []
		for child in review:
			if child.tag == 'book':
				for gchild in child:
					if gchild.tag == 'id':
						temp.append(gchild.text)
					elif gchild.tag == 'title':
						txt = gchild.text.split(" (")
						temp.append(txt[0])
					elif gchild.tag == 'average_rating':
						temp.append(gchild.text)
					elif gchild.tag == 'description':
						temp.append(str(gchild.text))
					elif gchild.tag == 'authors':
						for author in gchild:
							for att in author:
								if(att.tag == 'name'):
									temp.append(att.text)
									break	
						
			elif child.tag == 'rating':
					temp.append(child.text)
			elif child.tag == 'date_added':
					temp.append(child.text)
			
		read_books.append(temp)

	print(len(read_books))
	c = 0
	for book in read_books:
		#print(book)
		meta = book[1]+" by "+book[4]+'\n'+"Average Rating: " + book[2]
		desc = remove_tags(book[3])
		rating = book[5]
		date = book[6]
		key = book[1]+" by "+book[4]
		
		if(key not in DB):
			c +=1
			print(key)
			maxi +=1
			DB[key] = maxi
			
			
			
			metadata = str(os.getcwd())+"/BookData/BookMetaData/Book"+str(DB[key])+".txt"
			descdata = str(os.getcwd())+"/BookData/BookDescData/Book"+str(DB[key])+".txt"
			
			
			writer1 = open(metadata, "w")
			writer2 = open(descdata, "w")
			
			addDB.write(key+'\n')
			addDB.write(str(DB[key])+'\n')

			writer1.write(meta)
			writer2.write(desc)
			
		data = path+"/BookRatingData.txt"
		writer3 = open(data,'a+')
		writer3.write(str(DB[key])+" "+rating+" "+date+'\n')
	print("new book added: "+str(c)+ "for user "+twId[user])



print(len(DB))
'''
print(bookId)
print(title)
print(avg_rating)
print(desc)	
'''
