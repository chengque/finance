# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import sys
    
def plotstock(name,realname=u'代码'):
    quotes = ts.get_hist_data(name)
    quotes.index = quotes.index.astype('datetime64[D]')
    sh = ts.get_hist_data('sh')
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
    stockbasis=ts.get_stock_basics()
    realname=stockbasis[stockbasis.index==name].name[0]
    print realname
    plt.legend([unicode(realname,'utf-8')+':'+name,u'上证综指'])
    plt.subplot(212)
    qs=quotes["open"][-20:]
    qs.plot()
    shs=sh["open"][-20:]
    means=sum(qs)/len(qs)
    meansh=sum(shs)/len(shs)
    shs=shs/meansh*means
    shs.plot()
    plt.show()


if __name__ == "__main__":
    plotstock(sys.argv[1])