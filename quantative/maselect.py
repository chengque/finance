# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import sys
import numpy as np
import talib
from talib import MA_Type
import pandas as pd;
import localize as ll;
import traceback  
import datetime;
    
def evalstock(name,date):
    res=[]; res.append(False)
    quotesr = ll.readstock(name)
    quotesr.sort_index(inplace=True)
    quotes=quotesr[quotesr.index.values<np.datetime64(date)]
    close = quotes["close"]
    ma5=talib.MA(close.values,5)
    ma12=talib.MA(close.values,12)
    ma30=talib.MA(close.values,24)
    ma90=talib.MA(close.values,40)
    mav=pd.DataFrame({"ma5":ma5,"ma15":ma12,"ma30":ma30,"ma90":ma90},index=close.index);
    r0=ma90[-1]/ma90[-20]
    r1=ma5[-1]/ma90[-1]
    r2=ma5[-1]/ma12[-1]
    r3=ma5[-1]/ma5[-5]
    r4=ma5[-1]/ma30[-1]
    r5=min(ma12[-10:-1])/ma12[-1]
    nd=datetime.datetime.now()
    delta=nd-date


    if(r0<0.98 and r1<0.95 and r2>0.95 and r3>0.95 and r4<0.95 and r5<1):
        res[0]=(True)
        res.append(name)
        res.append(close[-1])
        res.append(r1)
        res.append(r2)
        res.append(r3)
        pf1=0
        pf2=0
        pf3=0
        pf4=0
        pf5=0
        pf6=0
        if(delta.days>90):
            quotes5=priceafter(quotesr,date,5)
            quotes10=priceafter(quotesr,date,10)
            quotes15=priceafter(quotesr,date,15)
            quotes30=priceafter(quotesr,date,30)
            quotes60=priceafter(quotesr,date,60)
            quotes90=priceafter(quotesr,date,90)
            pf1=(quotes5-close[-1])/close[-1]
            pf2=(quotes10-close[-1])/close[-1]
            pf3=(quotes15-close[-1])/close[-1]
            pf4=(quotes30-close[-1])/close[-1]
            pf5=(quotes60-close[-1])/close[-1]
            pf6=(quotes90-close[-1])/close[-1]
        res.append(pf1)
        res.append(pf2)
        res.append(pf3)
        res.append(pf4)
        res.append(pf5)
        res.append(pf6)
    return res;

def priceafter(quotesr,date,delta):
    daydelta=datetime.timedelta(days=delta)
    date=date+daydelta
    quotes=quotesr[quotesr.index.values<np.datetime64(date)]
    return quotes.close[-1]
 

def scanall(date):
    lstock=ll.getstocknum()
    lstock.to_json('data/index.json')
    lnum=lstock.index.values
    lname=lstock.name
    lpe=lstock.pe
    num=len(lnum)
    mres=[];
    for i in range(0,1000):
        try:
            print "Processing:"+str(lnum[i])+"-"+lname[i]+" "+str(i)+"/"+str(num)
            res=evalstock(lnum[i],date)
            if(res[0]):
                res.append(lpe[i])
                res.append(lname[i])
                mres.append(res);
        except:
            print 'Exception'
            traceback.print_exc() 
    for m in mres:
        print ("%6s %6.2f %.2f %.2f %.2f %4.2f %4.2f %4.2f %4.2f %4.2f %4.2f %4.2f %10s"%(m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13]))

if __name__ == "__main__":
    print sys.argv[1]
    scanall(datetime.datetime(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),0,0))