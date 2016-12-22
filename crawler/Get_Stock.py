# -*- coding: utf-8 -*-
__author__ = 'yjc'
import urllib2
import re
import os
import xlwt
root=r'D:\\Stock_Data\\'
def Get_Industry():
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKHY&type=ct&st=(BalFlowMain)&sr=-1&p=2&ps=100&js=var%20iTpfGWqB={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=48964248'
    data=urllib2.urlopen(url).read()
    data_temp=re.findall(r'\[.*\]',data)
    #print data_temp[0]
    data=eval(data_temp[0])
    Industry_code=[]
    Industry_name=[]
    for item in data:
        temp_list=item.split(',')
        Industry_code.append(temp_list[1])
        Industry_name.append(temp_list[2])
    return Industry_name,Industry_code
# make a dir
def Make_Folder(Industry_name):
    for industry in Industry_name:
        #print industry
        Folder_name=industry.decode('utf-8')
        folder_path=root+Folder_name
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
# get every stock in each industry
def Get_Stock_CN(Industry_code,Industry_name):
    url_h='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.'
    url_t='1&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=300&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.4069450023615404'
    k=0
    for code in Industry_code:
        url=url_h+code+url_t
        data=urllib2.urlopen(url).read()
        data_temp=re.findall(r'\[.*\]',data)
        data=eval(data_temp[0])
        xls_file=xlwt.Workbook()
        filename=Industry_name[k].decode('utf-8')
        sheet=xls_file.add_sheet(filename)
        filename=root+filename+'\\\\'+filename+'.xls'
        row=0
        for item in data:
            item=item.split(',')
            sheet.write(row,0,item[1])
            sheet.write(row,1,item[2].decode('utf-8'))
            row+=1
        # save file
        xls_file.save(filename)
        k=k+1
if __name__=="__main__":
    Industry_name,Industry_code=Get_Industry()
    Make_Folder(Industry_name)
    Get_Stock_CN(Industry_code,Industry_name)