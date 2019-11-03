import xlrd 
import os


# Give the location of the file 
loc =  str(os.getcwd())+"/BookRawData/BookData.xlsx" 
BookMetaDataLoc = str(os.getcwd())+"/BookData/BookMetaData/" 
BookDescDataLoc = str(os.getcwd())+"/BookData/BookDescData/" 
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
for i in range(sheet.nrows): 
   if i == 0:
        continue
   desc = str(sheet.cell_value(i, 4))
   #print(desc)
   if(desc==""):
        continue
   bookId = str(sheet.cell_value(i, 0))
   print(bookId)
   f1 = open(BookMetaDataLoc+bookId+".txt","a+")
   f2 = open(BookDescDataLoc+bookId+".txt","w")
   name = str(sheet.cell_value(i, 1))
   print(name)
   auth = str(sheet.cell_value(i,2))
   genre1 = str(sheet.cell_value(i,5))
   genre2 = str(sheet.cell_value(i,6))
   avgrating = str(sheet.cell_value(i,3))
   f1.write(name+" by "+ auth+'\n'+"Average rating: "+avgrating+'\n'+"Genre: "+ genre1+" "+ genre2) 
   f2.write(desc) 

