# -*- coding: utf-8 -*-
__author__ = '47217_000'
from time import *
from datetime import *
import urllib2
from pandas import DataFrame
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
Fmat="%Y%m%d"

def Get_Date(start_date='20160101',end_date='20160301'):
    st_date=datetime.strptime(start_date,Fmat)
    ed_date=datetime.strptime(end_date,Fmat)
    delta=ed_date-st_date
    DateList=[]
    num=delta.days
    for x in range(0,num):
        date_=st_date+timedelta(days=x)
        DateList.append(date_.strftime(Fmat))
    return DateList
# Get Url
def Get_Url(date):
    root_url='http://www.shfe.com.cn/data/dailydata/kx/kx'
    url=root_url+date+'.dat'
    return url
#analyze the content
def Get_Content(date_st,date_end):
    DateList=Get_Date(date_st,date_end)
    # print DateList
    E_FG_writer=pd.ExcelWriter('FG.xlsx')
    E_FG_total_writer=pd.ExcelWriter('E_FG_total.xlsx')
    FG_index_dict={"LASTPRICE":[],"OPENPRICE":[],"HIGHESTPRICE":[],"LOWESTPRICE":[],"LOWESTPRICE":[],\
                   "CLOSEPRICE":[],"PRECLOSEPRICE":[],"UPDOWN1":[],"UPDOWN2":[],"SETTLEMENTPRICE":[]}
    index_temp=[]
    for date in DateList:
        url=Get_Url(date)
        print url
        request=urllib2.Request(url)
        try:
            response=urllib2.urlopen(url)
        except urllib2.URLError, e:
            continue
        Content=response.read()
        Content=eval(Content)
        #print Content.keys()
        if Content['o_curinstrument']==[]:
            continue

        # All_Future_Goods
        detail=Content['o_curinstrument']
        Product={"DELIVERYMONTH":[],"PRESETTLEMENTPRICE":[],"OPENPRICE":[],"HIGHESTPRICE":[],"LOWESTPRICE":[],\
                 "CLOSEPRICE":[],"ZD1_CHG":[],"ZD2_CHG":[],"VOLUME":[],"OPENINTEREST":[],"OPENINTERESTCHG":[]}
        column_name=["DELIVERYMONTH","PRESETTLEMENTPRICE","OPENPRICE","HIGHESTPRICE","LOWESTPRICE",\
                    "CLOSEPRICE","ZD1_CHG","ZD2_CHG","VOLUME","OPENINTEREST","OPENINTERESTCHG" ]
        Product_index=[]
        for item in detail:
            for name in column_name:
                Product[name].append(item[name])
            Product_index.append(item['PRODUCTID'])

        # Each_Future_Goods_total
        total_FG={"HIGHESTPRICE":[],"LOWESTPRICE":[],"AVGPRICE":[],"VOLUME":[],"TURNOVER":[],\
                  "YEARVOLUME":[],"YEARTURNOVER":[]}
        total_FG_index=[]
        E_FG_total=Content['o_curproduct']
        for item in E_FG_total:
            total_FG_index.append(item['PRODUCTID'])
            for key,value in total_FG.iteritems():
                value.append(item[key])
        total_FG_df=DataFrame(total_FG,index=total_FG_index)
        total_FG_df.to_excel(E_FG_total_writer,sheet_name=date,encoding='utf-8')

        # Future_Goods_index
        FG_index=Content['o_curmetalindex'][0]
        for key,value in FG_index_dict.iteritems():
            value.append(FG_index[key])
        index_temp.append(date)
        E_FG_df=DataFrame(Product,index=Product_index)
        E_FG_df.to_excel(E_FG_writer,sheet_name=date,encoding='utf-8')
    E_FG_writer.save()
    E_FG_total_writer.save()
    FG_index_df=DataFrame(FG_index_dict,index=index_temp)
    FG_index_df.to_excel('FG_index_dict.xlsx',encoding='utf-8')
if __name__=="__main__":
    Get_Content('20150101','20160718')