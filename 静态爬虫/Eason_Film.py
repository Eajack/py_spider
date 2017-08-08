#!/usr/bin/env python3
# -*- coding : utf-8 -*-
#spider.py

import urllib.request
from bs4 import BeautifulSoup
import time

num = 1  #用来计数
start_time = time.time()  #计算爬虫爬取过程时间

#第一页网页网址"https://movie.douban.com/subject_search?start=0&search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1002"
#第二页网页网址"https://movie.douban.com/subject_search?start=15&search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1002"
#第三页网页网址"https://movie.douban.com/subject_search?start=30&search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1002"

url = "https://movie.douban.com/subject_search?start=%d&search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1002"  


for i in range(0,80,15): #range（初始，结束，间隔）
	html = urllib.request.urlopen("https://movie.douban.com/subject_search?start=%d&search_text=" %i + 
		"%E9%99%88%E5%A5%95%E8%BF%85&cat=1002" )
	bsObj = BeautifulSoup(html,'lxml')  
	a_node_list = bsObj.findAll("a",class_="nbg")
	print('==============' + '第%d页'%(i/10 + 1) + '==============')

	for a_node in a_node_list[1:]:
		#print(table_node)
		title = a_node.attrs["title"]
		title = '<<' + title + '>>'
		print('Eason的第%d部电影哦'%num, title)
		num += 1
	
	time.sleep(2)

end_time = time.time()
duration_time = end_time - start_time
print('运行时间共：%.2f'  % duration_time + '秒')
print('Eason总共拍了%d部电影!!!'%(num-1) )