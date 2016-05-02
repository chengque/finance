# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import sys
import numpy
import talib
from talib import MA_Type
import pandas as pd;
import localize as ll;
    
def plotstock(name,realname=u'代码'):
    quotes = ll.readstock(name)
    quotes.sort_index(inplace=True)
    close = quotes["close"]
    upper,middle,lower=talib.BBANDS(close.values,20,2,2)
    boll=pd.DataFrame({"upper":upper,"middle":middle,"lower":lower},index=close.index);

    plt.figure()
    plt.subplot(211)
    quotes["close"].plot()
    boll["upper"].plot()
    boll["middle"].plot()
    boll["lower"].plot()
    
    stockbasis=ll.getstockbasic()
    plt.subplot(212)
    qs=quotes["close"][-20:]
    qs.plot()
    plt.show()


if __name__ == "__main__":
    plotstock('600338')