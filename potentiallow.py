# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:12:33 2016

@author: chengque
"""
import matplotlib.pyplot as plt
import tushare as ts
import sys
import datetime
import numpy
import traceback  


def getstocknum():
    return ts.get_stock_basics()
    
def getstartdate():
    tday=datetime.datetime.now()
    startdate=tday+datetime.timedelta(days=-900);
    sdatestring=startdate.strftime('%Y-%m-%d')
    return sdatestring;

def plotstock(name,realname=u'代码'):
    sdatestring=getstartdate()
    quotes = ts.get_h_data(name,start=sdatestring)
    quotes.index = quotes.index.astype('datetime64[D]')
    sh = ts.get_h_data('sh',start=sdatestring)
    sh.index = sh.index.astype('datetime64[D]')
    quotes.sort_index(inplace=True)
    sh.sort_index(inplace=True)
    opens = quotes["close"]
    opensh=sh["close"]
    means=sum(opens)/len(opens)
    meansh=sum(opensh)/len(opensh)
    scale=meansh/means
    plt.figure()
    plt.subplot(211)
    quotes["close"].plot()
    sh["close"]=sh["close"]/scale
    sh["close"].plot()
    plt.legend([realname+':'+name,u'上证综指'])
    plt.subplot(212)
    qs=quotes["close"][-10:]
    qs.plot()
    shs=sh["close"][-10:]
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
    shcs = sh;
    return shcs
    
def getcloseprice(code):
    sdatestring=getstartdate()
    quotes = ts.get_hist_data(code,start=sdatestring)
    quotes.index = quotes.index.astype('datetime64[D]')
    quotes.sort_index(inplace=True)
    qcs = quotes;
    return qcs
    
def showstock(qs,shs,num,name):
    plt.figure()
    qs.plot()
    shs.plot()
    plt.legend([name+':'+num,u'上证综指'])
    plt.show()
    
def printstock(qs,shs,num,stdev,name):
    print '%10s%15s%15s%10.2f%10s'%(num,qs[-1],shs[-1],stdev,name)
    plt.show()
    
def stdDeviation(a):
    aa=[]
    for i in a:
        aa.append(i)
    narray=numpy.asarray(a)
    sum1=narray.sum()
    narray2=narray*narray
    sum2=narray2.sum()
    N=len(a)
    mean=sum1/N
    var=sum2/N/mean**2-1
    return var


def select():
    lstock=getstocknum()
    lnum=lstock.index.values
    lname=lstock.name
    sh=getshprice()
    shs=sh.close
    shv=sh.volume
    msh=sum(shs)/len(shs)
    mval=sum(shv[-5:])/sum(shv[-10:-5])
    num=len(lnum)
    ll02m=[];
    ll02p=[];
    ll0201m=[];
    ll0201p=[];
    llarge=[];
    print mval
    for i in range(0,num):
        try:
            if(i%100==99):
                print 'processing:'+str(i*100.0/num)+'%'
            qcs=getcloseprice(lnum[i])
            qs=qcs.close
            qsv=qcs.volume
            if len(qs)==0:
                continue;
            mq=sum(qs)/len(qs)
            scale=msh/mq
            mqv=sum(qsv[-5:])/sum(qsv[-10:-5])
            shsq=shs/scale
            r=(qs[-1]-shsq[-1])/shsq[-1]
            stdev=stdDeviation(qs.values[0:])
            if(r<-0.2):
                ll02m.append([qs,shsq,lnum[i],stdev,lname[i]]);
                #printstock(,'r<-0.2')
            if(r>0.2):
                ll02p.append([qs,shsq,lnum[i],stdev,lname[i]]);
                #printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'r>0.2')
            if(r>-0.2 and r<-0.1):
                ll0201m.append([qs,shsq,lnum[i],stdev,lname[i]]);
                #printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'-0.2<r<-0.1')
            if(r>0.2 and r<0.1):
                ll0201p.append([qs,shsq,lnum[i],stdev,lname[i]]);
                #printstock(qs,shsq,lnum[i],unicode(lname[i],'utf-8'),'-0.2<r<-0.1')
            if(mqv>2 and mqv>mval):
                llarge.append([mqv,mval,lnum[i],stdev,lname[i]]);
        except:
            print 'Exception'
            traceback.print_exc() 
    
    print 'r<-0.2:'        
    for l in ll02m:
         printstock(l[0],l[1],l[2],l[3],unicode(l[4],'utf-8'))
    print 'r>0.2:'        
    for l in ll02p:
         printstock(l[0],l[1],l[2],l[3],unicode(l[4],'utf-8'))
    print '-0.2<r<-0.1:'        
    for l in ll0201m:
         printstock(l[0],l[1],l[2],l[3],unicode(l[4],'utf-8'))
    print '0.1<r<0.2:'        
    for l in ll0201p:
         printstock(l[0],l[1],l[2],l[3],unicode(l[4],'utf-8'))
    print 'large volume:'        
    for l in llarge:
         printstock(l[0],l[1],l[2],l[3],unicode(l[4],'utf-8'))
        

if __name__ == "__main__":
    select();

