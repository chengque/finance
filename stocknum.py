# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import sys

def getstocknum():
    return ts.get_stock_basics()
