#!coding=utf-8
import requests
import os
import re
import json
import datetime
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import win32api,win32con
from cookie import headers

import time
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)
 
def raw(text):  # 转化URL字符串
 
    escape_dict = {
            '/': '%252F',
            '?': '%253F',
            '=': '%253D',
            ':': '%253A',
            '&': '%26',
 
                   }
    new_string = ''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    return new_string
 
 
def mmm(item):
    item=raw(item)
    url='https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'
    s=requests.session()
    postdata='c_devid=2C5039AF-99D0-4800-BC36-DEB3654D202C&username=&qs=true&c_engver=1.2.35&c_devtoken=&c_devmodel=iPhone%20SE&c_contype=wifi&' \
         't=1537348981671&c_win=w_320_h_568&p_url={}&' \
         'c_ostype=ios&jsoncallback=%3F&c_ctrl=w_search_trend0_f_content&methodName=getBiJiaInfo_wxsmall&c_devtype=phone&' \
         'jgzspic=no&c_operator=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8&c_appver=2.9.0&bj=false&c_dp=2&c_osver=10.3.3'.format(item)
    s.headers.update(headers)
    req=s.get(url=url,data=postdata,verify=False).text
 
    try:
        js=json.loads(req)
        title = js['single']['title']  ##名称
        jiagequshi=js['single']['jiagequshi']  ##价格趋势
        date_list=[]   ##日期
        price_list=[]  ##价格
        datalist=jiagequshi.replace('[Date.UTC(','').replace(')','').replace(']','').split(',')
        for i in range(0,len(datalist),5):
            year,month,day=datalist[i],datalist[i+1],datalist[i+2]
            date = datetime.date(year=int(year), month=int(month), day=int(day))
            price = float(datalist[i+3])
            date_list.append(date)
            price_list.append(price)
    except Exception as e:
        print(e)
        return
    

    data={'date':date_list,'price':price_list}
    df = pd.DataFrame(data)
    df.loc[:, "title"] = title
 
    df.to_csv('price.csv',index=False,mode='a',encoding="utf-8")  ##保存数据
    #print(df)
    #return df
 
 
if __name__ == '__main__':
    import pandas
    df=pandas.read_csv("mask.csv")
    for i in df.iloc[:,4]:
        mmm(i)