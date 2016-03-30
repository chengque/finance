# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:15:23 2016

@author: chengque
"""

def rtprofit(year,month):
    df=ts.get_profit_data(year,month)
    print df.dtypes
    df.net_profit_ratio=df.net_profit_ratio.fillna(0)
    print df.dtypes
    df.sort('net_profit_ratio',ascending=False,inplace=True)
    print ("\n\r%-12s%-15s%-15s%-30s"%("代码","利润率","利润","名称"))
    for i in range(1,20):
        print ("%-8s %-8.2f %10s "%(df.code.values[i],df.net_profit_ratio.values[i],df.net_profits.values[i]))+df.name.values[i].ljust(10)

    
if __name__ == "__main__":
    rtprofit(2015,4)
    