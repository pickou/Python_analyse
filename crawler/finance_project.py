#-*- coding:utf-8 -*-
import urllib
import urllib2
import requests
import sys
import re
from bs4 import BeautifulSoup
import xlrd
import xlwt
import chardet
from xlutils.copy import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
stock='600570'
stock_list=['300178','002095','600570','002024','600186','000540','300085',\
            '300287','300384','002410','300380','300166','600588','002197',\
            '002104','002657','600571','300377','000776','600109','600837',\
            '601901','000728','002012','600747','002600','300002','600599',\
            '002487','002072'];
critcal_word=[u'互联网金融',u'p2p',u'网贷',u'第三方支付',u'移动支付',u'互联网',u'金融',u'匹凸匹',u'P2P',u'供应链金融',u'互联网保险'];
word_sp=[u'电子支付'];
#建立xls工作簿
filename=xlwt.Workbook();
for stock in stock_list:
    sheet=filename.add_sheet(stock);
filename.save('critical_word.xlsx')

#打开xls文件
data=xlrd.open_workbook('critical_word.xlsx')
wb=copy(data)
for i in range(0,30):
    sheet=wb.get_sheet(i);
    stock=stock_list[i];
    num=0;
    row=0;
    #页数循环
    for page in range(1,800):
        url='http://guba.eastmoney.com/list,%s_%d.html'%(stock,page)
        request=urllib2.Request(url);
        try:
            response=urllib2.urlopen(request);
        except urllib2.URLError, e:  
            break;
        soup=BeautifulSoup(response);
        spans=soup.findAll('span');
        #取一次初值
        if page==1:
            for span in spans:
                if(span.attrs.has_key('class')):
                    #取出评论日期
                    if(span['class']==['l5']):
                        comment_date=''.join(span.contents).split(' ')[0];  
                        if(comment_date!=u'最后更新'):
                            break;
        for span in spans:
            if(span.attrs.has_key('class')):
                #取出评论title
                #num=0;            
                if(span['class']==['l3']):
                    comment=unicode(span.contents[-1:][0].string);
                    if(comment!=u'标题'):
                        print comment                 
                        #匹配关键词
                        if(re.search(critcal_word[0],comment)!=None or re.search(critcal_word[9],comment)!=None):
                            num=num+1;
                        elif(re.search(critcal_word[5],comment)!=None and re.search(critcal_word[6],comment)!=None):
                            num=num+1; 
                        if(re.search(critcal_word[1],comment)!=None or re.search(critcal_word[2],comment)!=None\
                            or re.search(critcal_word[7],comment)!=None or re.search(critcal_word[8],comment)!=None):
                            num=num+1;            
                        if(re.search(critcal_word[3],comment)!=None or re.search(critcal_word[4],comment)!=None\
                           or re.search(word_sp[0],comment)!=None):
                            num=num+1; 
                        if(re.search(critcal_word[10],comment)!=None):
                            num=num+1;
                #取出评论日期
                if(span['class']==['l5']):
                    last_comment_date=comment_date;
                    comment_date=''.join(span.contents).split(' ')[0];
                    if(comment_date==u'最后更新'):
                        comment_date=last_comment_date;                   
                    if(comment_date!=last_comment_date):
                        #写入日期和关键词词频
                        print num
                        if(num!=0):
                            sheet.write(row,0,last_comment_date);
                            sheet.write(row,1,num);
                            row+=1;
                            num=0;

wb.save('critical_word.xlsx')

        
    

