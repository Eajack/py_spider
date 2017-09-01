#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Author: Eajack
# date:2017/9/1
# Function：
#   爬取煎蛋网http://jandan.net/ooxx 前n页图片

from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlretrieve
import requests
import os
import re
import random

def jiandan(pageNum):
  global headers,imgcount
  path = r"D:\STUDYING\MyProjects\pycharm\jandan\girls"
  os.chdir(path)

  starturl = r"http://jandan.net/ooxx"
  for pagecount in range(0,pageNum):
    req = requests.get(starturl,headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html,'lxml')

    for imgNode in soup.findAll("a",{"class":"view_img_link"}):
      imgUrl = imgNode["href"]
      imgUrl = "http:" + imgUrl
      urlretrieve(imgUrl,str(imgcount) + ".jpg")
      imgcount += 1

    print(starturl + "已经爬取完毕")
    starturl = soup.find("a",{"class":"previous-comment-page"})["href"]


if __name__ == '__main__':
  # globals
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/60.0.3112.113 Safari/537.36",
             "Accept": "text/html,application/xhtml+xml,"
                       "application/xml;q=0.9,image/webp,"
                       "image/apng,*/*;q=0.8",
             "Accept - Encoding": "gzip, deflate",
             "Accept - Language": "zh - CN, zh;q = 0.8",
             "referer": "http://jandan.net/",
             "Connection": "keep-alive",
             }
  imgcount = 0

  # game start
  jiandan(5)  #爬取5页