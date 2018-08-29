#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Get the price rate of given date, only support CHY-HKD now.
@file:rate_scraper.py
@author: vincent cheung
"""

## Import modules
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys

# Currency and ID dicts
curNameDict={'HKD':'1315'}

# Main func
def get_rate(date,curName='HKD',isHighEstRate=True,print_info=True):
    """
    Return tuple of the exchange rate of the given currency on the specific date and the corresponding 
    info. The validation of input are not checked yet. Please be careful.
    
    Input:
    `date`: The specific date for search the rate, should be 'YYYY-MM-DD' format.
    `curName`: The currency name, like 'HKD'.
    `print_info`: Print debug info or not.

    Return:
    `rate`: The exchange rate from Bank of China,
        [webs](http://srh.bankofchina.com/search/whpj/search.jsp).
    `info_str`: The detail info of rate for further uses. 
    """
    ## Compose the post Requests
    url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
    body = {'erectDate':date, 'nothing':date, 'pjname':curNameDict[curName]}
    
    ## Post requests
    if sys.version_info < (3,2):
        import urllib2
        data = urllib.urlencode(body)
        req  = urllib2.Request(url, data)
        f = urllib2.urlopen(req)
    else:
        data = urllib.parse.urlencode(body).encode(encoding='UTF8')
        req  = urllib.request.Request(url, data)
        f = urllib.request.urlopen(req)
    response = f.read()
    f.close()

    ## Parse the response html with beautifulsoup
    soup = BeautifulSoup(response,'html.parser')
    ### Extract the exchange rate table
    res4 = soup.findAll("div", { "class" : "BOC_main publish" })[0]
    #print res4
    #print(res4.prettify())

    ## Convert the table into pandas dataframe format
    dfs = pd.read_html(str(res4.table),encoding='utf-8')
    df = dfs[0]# The first object of the dataframe lists
    

    if df[5][0] != u'中行折算价':
        print ('中行汇率接口已改变，请修改解析脚本')
        sys.exit(0)
    else:
        if isHighEstRate is True:
            ## Use the highest rate.
            max_idx = df[5][1:].astype('float').idxmax()
        else:
            max_idx = 1
        info_str = u'时间:{}, 货币名称:{}, {}:{}'.format(df[6][max_idx], 
                df[0][max_idx], df[5][0],df[5][max_idx])        
        
        if print_info is True:
            pd.set_option('display.max_rows',None)
            print (info_str)
        rate = df[5][max_idx]
        return [float(rate),info_str]

if __name__ == '__main__':
    ## Demo function
    get_rate(date=datetime.date.today())
    ## Test Function
    # It should be 87.27, 
    # as '时间:2018.08.27 23:52:04, 货币名称:港币, 中行折算价:87.27'.
    get_rate(date='2018-08-27')
