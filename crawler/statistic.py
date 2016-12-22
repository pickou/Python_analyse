__author__ = '47217_000'
import xlwt
import xlrd
from xlutils.copy import copy
import matplotlib.pyplot as plt
from math import log
book=xlrd.open_workbook(r'C:\Users\47217_000\Desktop\critical_word.xlsx')
wrt=copy(book)
for k in range(0,30):
    table=book.sheet_by_index(k)
    temp=table.col_values(9,0)
    date1=[]
    for it in temp:
        if it!='':
            date1.append(it)
    date2=[]
    temp=table.col_values(4,0)
    for it in temp:
        if it!='':
            date2.append(it)
    temp=table.col_values(6,0)
    price=[]
    vol=[]
    for it in temp:
        if it!='':
            price.append(it)
    temp=table.col_values(7,0)
    for it in temp:
        if it!='':
            vol.append(it)
    freq=[]
    data=table.col_values(3,0)
    print date1
    print date2
    len1=len(date1)
    len2=len(date2)
    for i in range(0,len1):
        sum=0;
        for j in range(0,len2):
            if(date2[j]>=date1[i-1]):
                if(date2[j]>=date1[i]):
                    break
                else:
                    sum+=data[j];
        freq.append(sum)
    print sum
    w_sheet=wrt.get_sheet(k)
    for i in range(0,len1):
        w_sheet.write(i,8,freq[i])
    for i in range(0,len1-1):
        w_sheet.write(i+1,10,log(price[i+1]/price[i]))
        w_sheet.write(i+1,11,log(vol[i+1])/log(vol[i]))
    wrt.save(r'C:\Users\47217_000\Desktop\critical_word.xlsx')

    print freq

