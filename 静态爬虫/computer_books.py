#!/usr/bin/env python3
# -*- coding : utf-8 -*-
#computer_books.py
# <世界著名计算机教材精选> 豆瓣

import urllib.request
from bs4 import BeautifulSoup
import time

num = 1  #用来计数，计算爬取的书一共有多少本
start_time = time.time()  #计算爬虫爬取过程时间

url = 'https://book.douban.com/series/32479?page=1'  
html = urllib.request.urlopen('https://book.douban.com/series/32479?page=1')    
bsObj = BeautifulSoup(html,'lxml')

for i in range(1,14):  #这里的  range（初始，结束，间隔）
    #urllib.request库用来向该网服务器发送请求，请求打开该网址链接
    html = urllib.request.urlopen('https://book.douban.com/series/32479?page=%d' % i)    
    #BeautifulSoup库解析获得的网页，第二个参数一定记住要写上‘lxml’，记住就行
    bsObj = BeautifulSoup(html,'lxml')  

    print('==============' + '第%d页'%i + '==============')
    #分析网页发现，每页有10本书，而<h2>标签正好只有10个。
    h2_node_list = bsObj.find_all('h2')  # 这里返回的是h2标签的list列表
    for h2_node in h2_node_list:  #遍历列表
        a_node = h2_node.a 
        title = a_node.attrs["title"]
        title = '<<' + title + '>>'
        print('第%d本书'%num, title)
        num = num + 1
    #设置抓数据停顿时间为1秒，防止过于频繁访问该网站，被封
    time.sleep(1)  


end_time = time.time()
duration_time = end_time - start_time
print('运行时间共：%.2f'  % duration_time + '秒')
print('共抓到%d本书名'%num)