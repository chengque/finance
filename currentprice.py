# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:41:53 2016

@author: chengque
"""

import tushare as ts
import sys
import os
import string
import time


def lowprice(uprice,lprice=0):
    df=ts.get_today_all()
    df.trade=df.trade.astype(float)
    qt=df[(df.trade>0.0) & (df.trade<uprice)]
    qt.sort('trade',ascending=True,inplace=True)
    print qt
    codes=qt["code"]
    names=qt["name"]
    price=qt["trade"]
    amount=qt["volume"]
    pre=qt["changepercent"]
    print codes
    print names
    print price
    print pre
    print ("\n\r%-12s%-15s%-15s%-30s"%("代码","现价","涨跌","名称"))
    for i in range(1,len(codes)):
        print ("%-8s %-8.2f %10s "%(codes.values[i],price.values[i],pre.values[i]))+names.values[i].ljust(10)
#print "{:8s} {:10s} {:10s} {:8.2f} {:30s}".format(codes[i],names[i],price[i],(string.atof(price[i])-string.atof(pre[i]))*100/string.atof(pre[i]),amount[i])

if __name__ == "__main__":
    lowprice(3.5,0)
    