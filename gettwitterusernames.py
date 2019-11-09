import xlrd 
import os


# Give the location of the file 
loc =  str(os.getcwd())+"/Twitter_GR_List.xlsx" 
accounts = str(os.getcwd())+"/UserAccounts.txt"
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
f1 = open(accounts,"a+") 
# For row 0 and column 0 
for i in range(sheet.nrows): 
   username = str(sheet.cell_value(i, 0))
   gr = str(sheet.cell_value(i, 1))
   temp = float(gr)
   tmp = int(temp)
   gr = str(tmp)
   f1.write(username+' '+gr+'\n') 

