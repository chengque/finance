# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import sys
import numpy
import talib
from talib import MA_Type
import pandas as pd
import json
import datetime
import time
import os
import traceback  

def updatestock(code,start,end):
	df=readstock(code)
	dfe=(pd.to_datetime(df.index.values[-1])).to_pydatetime()
	dfs=(pd.to_datetime(df.index.values[0])).to_pydatetime()
	dee=dfe-end
	dss=dfs-start
	dse=dfs-end
	des=dfe-start
	md1=datetime.timedelta(days=-1)
	print dfe
	print dfs
	print dee.days
	print dss.days
	if(dee.days>=0):
		end=dfs+md1
	if(dss.days<=0):
		start=dfe-md1
	if(dse.days>0):
		return
	if(des.days<0):
		return
	dd=end-start
	if(dd.days<=0):
		return
	quotes = ts.get_h_data(code,start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
	quotes.sort_index(inplace=True)
	quotes.to_json('data/'+code+'.json')

def readstock(code):
	df=pd.read_json('data/'+code+'.json')
	return df

def storestock(code,start,end):
	if existlocal(code):
		return;
	quotes = ts.get_h_data(code,start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
	quotes.sort_index(inplace=True)
	quotes.to_json('data/'+code+'.json')

def localfile(code):
	return 'data/'+code+'.json';

def existlocal(code):
	return (os.path.exists(localfile(code)))

def getstocknum():
    return ts.get_stock_basics()

def getstockbasic():
	df=pd.read_json('data/index.json')
	return df

def storeall(start,end):
    lstock=getstocknum()
    lstock.to_json('data/index.json')
    lnum=lstock.index.values
    lname=lstock.name
    num=len(lnum)
    for i in range(0,num):
        try:
	        print "Processing:"+str(lnum[i])+"-"+lname[i]+" "+str(i)+"/"+str(num)
	        storestock(lnum[i],start,end)
        except:
            print 'Exception'
            traceback.print_exc() 

if __name__ == '__main__':
	storeall(datetime.datetime(2002,1,1,0,0),datetime.datetime.now())

