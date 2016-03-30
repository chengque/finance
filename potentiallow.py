# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:12:33 2016

@author: chengque
"""
import matplotlib.pyplot as plt
import tushare as ts
import sys
import datetime


def getstocknum():
    return ts.get_stock_basics()
    
def getstartdate():
    tday=datetime.datetime.now()
    startdate=tday+datetime.timedelta(days=-30);
    sdatestring=startdate.strftime('%Y-%m-%d')
    return sdatestring;

def plotstock(name,realname=u'代码'):
    sdatestring=getstartdate()
    quotes = ts.get_hist_data(name,start=sdatestring)
    quotes.index = quotes.index.astype('datetime64[D]')
    sh = ts.get_hist_data('sh',start=sdatestring)
    sh.index = sh.index.astype('datetime64[D]')
    quotes.sort_index(inplace=True)
    sh.sort_index(inplace=True)
    opens = quotes["open"]
    opensh=sh["open"]
    means=sum(opens)/len(opens)
    meansh=sum(opensh)/len(opensh)
    scale=meansh/means
    plt.figure()
    plt.subplot(211)
    quotes["open"].plot()
    sh["open"]=sh["open"]/scale
    sh["open"].plot()
    plt.legend([realname+':'+name,u'上证综指'])
    plt.subplot(212)
    qs=quotes["open"][-10:]
    qs.plot()
    shs=sh["open"][-10:]
    means=sum(qs)/len(qs)
    meansh=sum(shs)/len(shs)
    shs=shs/meansh*means
    shs.plot()
    plt.show()
    
def getshprice():
    sdatestring=getstartdate()
    sh = ts.get_hist_data('sh',start=sdatestring)
    sh.index = sh.index.astype('datetime64[D]')
    sh.sort_index(inplace=True)
    shcs = sh["close"]
    return shcs
    
def getcloseprice(code):
    sdatestring=getstartdate()
    quotes = ts.get_hist_data(code,start=sdatestring)
    quotes.index = quotes.index.astype('datetime64[D]')
    quotes.sort_index(inplace=True)
    qcs = quotes["close"]
    return qcs
    
def showstock(qs,shs,num,name):
    plt.figure()
    qs.plot()
    shs.plot()
    plt.legend([name+':'+num,u'上证综指'])
    plt.show()
    
def printstock(qs,shs,num,name,note):
    print '%10s%15s%15s%10s%10s'%(num,qs[-1],shs[-1],note,name)
    plt.show()

def select():
    lstock=getstocknum()
    lnum=lstock.index.values
    lname=lstock.name
    shs=getshprice()
    msh=sum(shs)/len(shs)
    num=len(lnum)
    for i in range(0,num):
        try:
            if(i%100==99):
                print 'processing:'+str(i*100.0/num)+'%'
            qs=getcloseprice(lnum[i])
            if len(qs)==0:
                continue;
            mq=sum(qs)/len(qs)
            scale=msh/mq
            shsq=shs/scale
            r=(qs[-1]-shsq[-1])/shsq[-1]
            if(r<-0.2):
                printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'r<-0.2')
            if(r>0.2):
                printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'r>0.2')
            if(r>-0.2 and r<-0.1):
                printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'-0.2<r<-0.1')
        except:
            print 'Exception'
        

if __name__ == "__main__":
    select()

