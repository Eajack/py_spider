#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Author: Eajack
# date:2017/8/19
# Function：
#   利用爬虫证明 “wiki六度分割理论”
# 思路：
#   设限制层数是 6 层，利用广度优先遍历
#   由于Breadth_First_Search只能打印出target url 以及倒数第二个链接
#   因此，需要多次循环利用该函数
# 缺点（留坑）：
#   1- 还是太慢了 2- 暂时不能达到证明的层度，只是尝试判断6层内是否可以达到目标URL
#   3- 目前尝试都是可以的，只是太慢了。若尝试证明，则需要爬取wiki所有词条数据
#      需要数据库、多线程、IP代理等知识


from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import requests


def getInnerLinks(currentUrl):
    '''
    获取currentUrl链接的所有内链innerLink ,list形式
    :param currentUrl: 
    :return: innerLink
    '''
    # 请求头与request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                             "AppleWebKit/537.36 (KHTML, like Gecko)"
                             "Chrome/59.0.3071.115 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;"
                         "q=0.9,image/webp,image/apng,image/*,*/*;q=0.8",
               "Connection": "keep-alive"
               }
    request = requests.get(currentUrl, headers=headers)
    request.encoding = 'utf-8'
    html = request.text
    bsObj = soup(html, 'lxml')

    # 变量声明
    # print('------------------------------------------------')
    innerLinks = []
    hrefs = []
    originUrl = 'https://en.wikipedia.org'
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in hrefs:
                # new page FOUND
                newHref = link.attrs['href']
                hrefs.append(newHref)
                newPage = originUrl + newHref
                innerLinks.append(newPage)

                # debug use
                # print(newPage)

                # 深度优先搜索：get all links in WIKI
                # getLinks(newPage)
    # debug use
    # print(len(innerLinks),len(hrefs))
    # print('------------------------------------------------')

    return innerLinks

def Breadth_First_Search(startUrl, targetUrl, layers):
    '''
    return foundFlag: 1 => 找到了targetUrl
                    : 0 => 没找到targetUrl
    打印 target Url & 倒数第二个url，并储存在linkPath中
    '''
    global nowInnerLinks_List
    global nextInnerLinks_List
    global linkpath
    global reachLayer

    foundFlag = 0
    for layer in range(1,layers+1):
        print("已经找到第" + str(layer) + "层")
        reachLayer = layer
        # 第一层指的是startUrl的所有内链
        if (layer == 1):
            firstInnerLinks_List = getInnerLinks(startUrl)
            nowInnerLinks_List = firstInnerLinks_List[:]
            if targetUrl in nowInnerLinks_List:
                print("\nTARGET URL FOUND:", targetUrl)
                print("START URL:", startUrl)

                if startUrl not in linkPath:
                    linkPath.append(startUrl)
                if targetUrl not in linkPath:
                    linkPath.append(targetUrl)

                foundFlag = 1
                return foundFlag
        else:
            for nowInnerLink in nowInnerLinks_List:
                nextInnerLinks_List = getInnerLinks(nowInnerLink)
                if targetUrl in nextInnerLinks_List:
                    # 当前页面为nowInnerLink
                    currentUrl = nowInnerLink
                    print("\nTARGET URL FOUND:", targetUrl)
                    print("PAGE:", currentUrl)

                    if targetUrl not in linkPath:
                        linkPath.append(targetUrl)
                    if currentUrl not in linkPath:
                        linkPath.append(currentUrl)

                    foundFlag = 1
                    return foundFlag

            nowInnerLinks_ListBuffer = []
            for nowInnerLink in nowInnerLinks_List:
                for nextInnerLink in nextInnerLinks_List:
                    nowInnerLinks_ListBuffer.append(nextInnerLink)
            nowInnerLinks_List = nowInnerLinks_ListBuffer[:]

    return foundFlag


if __name__ == '__main__':
    # url声明
    originUrl = 'https://en.wikipedia.org'
    startUrl = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    targetUrl = 'https://en.wikipedia.org/wiki/Case_Closed'

    # 广度优先遍历
    ## Breadth_First_Search全局变量声明
    layers = 6
    nowInnerLinks_List = []
    nextInnerLinks_List = []
    linkPath = [targetUrl]
    reachLayer = 0

    ## 循环体变量声明
    count = 0
    firstUrl = startUrl
    endUrl = targetUrl
    while( (count != layers) or ( linkPath[0] != targetUrl ) ):
        if firstUrl != endUrl:
            Breadth_First_Search(firstUrl, endUrl, layers-count)
        count += 1
        endUrl = linkPath[-1]

    # 结果输出
    linkPath.reverse()
    print("\n六度分割链接顺序如下：")
    for link in linkPath:
        extraSymbol = (" =>" if (link != linkPath[-1]) else " ")
        print(link,extraSymbol,end='')