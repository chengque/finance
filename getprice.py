# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 20:36:57 2016

@author: chengque
"""

import tushare as ts
import sys
import os
import string
import time

def rtprice(code,clear=False):
    qt=ts.get_realtime_quotes(code)
    codes=qt["code"]
    names=qt["name"]
    time=qt["time"]
    price=qt["price"]
    amount=qt["amount"]
    pre=qt["pre_close"]
    if(clear):
        os.system("clear")
    print ("%-12s%-15s%-15s%-12s%-30s"%("代码","现价","涨跌","交易量","名称"))
    for i in range(0,len(time)):
        print ("%-8s %-10s %-8.2f %-15s"%(codes[i],price[i],(string.atof(price[i])-string.atof(pre[i]))*100/string.atof(pre[i]),amount[i]))+names[i].ljust(10)
#print "{:8s} {:10s} {:10s} {:8.2f} {:30s}".format(codes[i],names[i],price[i],(string.atof(price[i])-string.atof(pre[i]))*100/string.atof(pre[i]),amount[i])

if __name__ == "__main__":
    code=sys.argv[1:]
    while(True):
        rtprice(code,True)
        time.sleep(5)