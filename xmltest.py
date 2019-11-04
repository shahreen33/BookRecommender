import xml.etree.ElementTree as ET
import re
import os

UserId = ['101556262', '57797254', '21937982', '6536286','14457130']
N = len(UserId)

for user in range(N):

	path = str(os.getcwd())+"/UserBookData/"+UserId[user]
	metadata = str(os.getcwd())+"/UserBookData/"+UserId[user]+"/BookMetaData"
	descdata = str(os.getcwd())+"/UserBookData/"+UserId[user]+"/BookDescData"
	ratingdata = str(os.getcwd())+"/UserBookData/"+UserId[user]+"/BookRatingData"
	datedata = str(os.getcwd())+"/UserBookData/"+UserId[user]+"/BookDateData"
	
	if not os.path.exists(path):
		os.mkdir(path)
	if not os.path.exists(metadata):
		os.mkdir(metadata)
	if not os.path.exists(descdata):
		os.mkdir(descdata)
	if not os.path.exists(ratingdata):
		os.mkdir(ratingdata)
	if not os.path.exists(datedata):
		os.mkdir(datedata)

	TAG_RE = re.compile(r'<[^>]+>')

	def remove_tags(text):
	    return TAG_RE.sub('', text)


	tree = ET.parse('bla1.xml')
	root = tree.getroot()

	print(root.tag)
	print(root.attrib)

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
						temp.append(gchild.text)
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
	
	for book in read_books:
		#print(book)
		f1 = metadata+'/' + book[0]+".txt"
		f2 = descdata+'/'+ book[0]+".txt"
		f3 = ratingdata+'/' + book[0]+".txt"
		f4 = datedata+'/' + book[0]+".txt"

		writer1 = open(f1, "a+")
		writer2 = open(f2, "w")
		writer3 = open(f3,"w")
		writer4 = open(f4, "w")

		meta = book[1]+" by "+book[4]+'\n'+"Average Rating: " + book[2]
		desc = remove_tags(book[3])
		rating = book[5]
		date = book[6]

		writer1.write(meta)
		writer2.write(desc)
		writer3.write(rating)
		writer4.write(date)
	break	



'''
print(bookId)
print(title)
print(avg_rating)
print(desc)	
'''
