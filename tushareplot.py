# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import stocknum as sn
import certainstock as cs

snum=sn.getstocknum()
scode=snum.index.values
sname=snum['name']
i=1;
for i in range(0,4):
    cs.plotstock(scode[i])
    print scode[i]+":"+sname[i]
    
