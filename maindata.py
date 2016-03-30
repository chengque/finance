# -*- coding: utf-8 -*-
"""
Created on Thu May 01 22:43:26 2014
Last updated on 2014-6-19
@author: Shengzhou
"""

import time, urllib, sys
from HTMLParser import HTMLParser
import os;
import time;

class MyHTMLParser(HTMLParser):
    previous_data = ""
    text_before_amp = ""
    current_date = ""
    security_name = ""
    volume = ""
    open_price = ""
    high_price = ""
    low_price = ""
    close_price = ""
    previous_close_price = ""
    minus_sign = ""
    percentage_change = ""
    quote_date = ""
    info=""

    def __init__(self, t):
        HTMLParser.__init__(self)
        self.ticker = t

    def handle_starttag(self, tag, attrs):
        # get arrow diection: up/positive or down/negative
        for attr in attrs:
            if "up_g time_rtq_content"==attr[1]:
                self.minus_sign = ""
            if "down_r time_rtq_content"==attr[1]:
                self.minus_sign = "-"

    def handle_data(self, data):
        starttag_text = self.get_starttag_text()

        # get market time and print its date
        # pre market string "Tue, May 6, 2014, 9:02AM EDT - US Markets open in 28 mins" "Tue, May 6, 2014, 8:57AM EDT - U.S. Markets open in 33 mins."
        # in market string "Mon, May 5, 2014, 10:50AM EDT - US Markets close in 5 hrs and 10 mins"
        # after market string "Mon, May 5, 2014, 5:41pm EDT - US Markets are closed"
        if -1 != str(starttag_text).find("yfs_market_time") and -1 != data.find(","):
            s = data.split(",")
            t = time.strptime(s[0] + s[1] + s[2], "%a %b %d %Y")
            self.current_date = time.strftime("%d/%m/%Y", t)

        # get stock/fund name
        if -1 != data.find(("(%s)" % self.ticker).upper()) and -1 != str(starttag_text).find("<h2>"):
            prefix = ""
            if len(self.text_before_amp.strip()) > 0:
                prefix = self.text_before_amp
                self.text_before_amp = ""
            self.security_name = "\t" + prefix + data + "\t" + self.ticker

        # get current/closing price
        if -1 != str(starttag_text).find("yfs_l84_%s" % self.ticker.lower()) and len(data.strip()) > 0:
            self.close_price = "\t" + data

        # get percentage change. the tag id is "yfs_p43_%s" in or after trading hours, or "yfs_p20_%s" pre-market.
        if (-1 != str(starttag_text).find("yfs_p43_%s" % self.ticker.lower()) or -1 != str(starttag_text).find("yfs_p20_%s" % self.ticker.lower())) and len(data.strip()) > 0:
            self.percentage_change = "\t" + self.minus_sign + data.strip("()")

        # get date of quotes if it exists. the date only appears in pre-market sessions.
        # pre market string "May 5, 4:00PM EDT"
        # in market string "10:50AM EDT"
        # after market string "4:00PM EDT"
        if -1 != str(starttag_text).find("yfs_t53_%s" % self.ticker.lower()) and -1 != data.find(","):
            t = time.strptime(data.split(",")[0] + time.strftime(" %Y"), "%b %d %Y")
            self.quote_date = "\t" + time.strftime("%d/%m/%Y", t)

        if -1 != str(starttag_text).find("yfnc_tabledata1"):
            # get previous close price
            if -1 != self.previous_data.find("Prev Close:"):
                self.previous_close_price = "\t" + data
            # get opening price. open price is "N/A" in the beginning of trading hours
            if -1 != self.previous_data.find("Open:"):
                self.open_price = "\t" + data

        # get the day's range - low
        if -1 != str(starttag_text).find("yfs_g53_%s" % self.ticker.lower()) and len(data.strip(" -")) > 0:
            self.low_price = "\t" + data

        # get the day's range - high
        if -1 != str(starttag_text).find("yfs_h53_%s" % self.ticker.lower()):
            self.high_price = "\t" + data

        # get trading volume
        if -1 != str(starttag_text).find("yfs_v53_%s" % self.ticker.lower()):
            self.volume = "\t" + data

        self.previous_data = data

    def handle_entityref(self, name):
        # for stock names with the symbol &, save the part before & for later use
        if "amp" == name and -1 != str(self.get_starttag_text()).find("<h2>"):
            self.text_before_amp += self.previous_data + "&"

    def close(self):
        HTMLParser.close(self)
        # print as follows: date, name, ticker, volume, open, high, low, close, previous close, change, range and previous date (if the quote is not for today)
        print("%10s%50s%10s%10s%8s%8s%8s%8s%5s"%(self.current_date , self.security_name , self.volume , self.open_price , self.high_price ,self.low_price , self.close_price , self.previous_close_price , self.percentage_change ))

if __name__ == "__main__":
    # default values for testing names with symbols "&", "-", "+", "$", "/" and "™" (tm)
    ticker_list = ["qqq", "spy", "xme", "xop", "fxi", "veu", "tlt", "lqd", "shm", "schd", "sche", "schv"]

    # arguments can be passed through command line.
    # usage: python parser.py "qqq spy xme xop" > output.txt
    if len(sys.argv) > 1:
        ticker_list = sys.argv[1].split()
    print("%10s%50s%20s%12s%8s%8s%8s%8s%8s"%("Date" , "Name" ,"Vol" , "Open" , "High" ,"Low" , "Close" , "Prev" , "Change" ))
    for t in ticker_list:
        parser = MyHTMLParser(t)
        filehandle = urllib.urlopen("http://finance.yahoo.com/q?s=%s" % t)
        html_string = filehandle.read()
        parser.feed(html_string)
        parser.close()