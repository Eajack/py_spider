#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# ==================================================================================================================
# Author: Eajack
# date:2018/1/28
# ==================================================================================================================
# Function：
#   1- 爬取http://quotes.money.163.com网站股票数据
#   2- 无防IP被封措施，没有设置代理IP、多进程
# ==================================================================================================================

from bs4 import BeautifulSoup
import requests
import json,os,re,time
from selenium import webdriver
import xlwt,xlrd,openpyxl
from xlutils.copy import copy
from xlwt import Style

# 导入所有公司股票代码
def importCodes():
    global Company2Codes
    # 读取 "公司代码.xls"
    CodeXlsFileName = "公司代码.xls"
    commentxlsFile = xlrd.open_workbook(CodeXlsFileName, formatting_info=True)
    sheet0 = commentxlsFile.sheets()[0]
    rowNum = sheet0.nrows

    for row in range(0,rowNum):
        company = sheet0.cell(row, 0).value
        code = sheet0.cell(row, 1).value
        Company2Codes[company] = code

# 爬虫股票数据
def getSharesHtml(allCompanys2Links):
    global years, seasons

    for company,link in allCompanys2Links.items():
        time.sleep(2)
        xlsFileName = company + '.xls'
        print("===================" + company + "===================")
        for year in years:
            for season in seasons:
                dataSheet = []
                print("==========" + str(year) + "年,第" + str(season) + "季度" + "==========")
                ShareLink = link + r'?year=' + str(year) + r'&' + r'season=' + str(season)
                #2- html解析
                headers["Referer"] = ShareLink
                request = requests.get(ShareLink, headers=headers)
                request.encoding = 'utf-8'
                html = request.text
                Html = BeautifulSoup(html,'lxml')
                #print(Html.prettify())
                if (Html == None):
                    print("IP被封了！！！")
                    exit(1)

                #3- 获取注释
                for comments in Html.find("table",class_="table_bg001 border_box limit_sale").find_all("thead"):
                    comments = comments.get_text().split()
                    for comment in comments:
                        comment = comment.replace("[", "")
                        comment = comment.replace("]", "")
                        dataSheet.append(comment)

                #4- 获取数据
                for data in Html.find("table",class_="table_bg001 border_box limit_sale").find_all("td"):
                    data = data.get_text()
                    data = data.replace("[","")
                    data = data.replace("]","")
                    dataSheet.append(data)
                if (len(dataSheet) == 11):
                    continue
                #print(dataSheet)

                # 5- 写入Excel
                if os.path.exists(xlsFileName):
                    # 文件存在,则新建sheet，可写入数据
                    ShareXlsFile = xlrd.open_workbook(xlsFileName, formatting_info=True)
                    writeFile = copy(ShareXlsFile)
                    sheetName = str(year) + '年第' + str(season) + '季度'
                    print(sheetName)
                    newSheet = writeFile.add_sheet(sheetName)
                    style = Style.default_style
                    dataCount = 0

                    for row in range(0,len(dataSheet)//11):
                        for col in range(0,11):
                            newSheet.write(row, col, dataSheet[dataCount], style)
                            dataCount = dataCount + 1
                    writeFile.save(xlsFileName)

                else:
                    sheetName = str(year) + '年第' + str(season) + '季度'
                    print(sheetName)
                    # 文件未存在，则新建xls文件，之后写入
                    xlsFile = xlwt.Workbook()

                    sheet = xlsFile.add_sheet(sheetName)
                    dataCount = 0

                    for row in range(0, len(dataSheet)//11):
                        for col in range(0, 11):
                            sheet.write(row, col, dataSheet[dataCount])
                            dataCount = dataCount + 1
                    xlsFile.save(xlsFileName)

if __name__ == '__main__':
    startTime = time.time()
    # global
    ## 请求头
    headers = {
	    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    "Accept-Encoding":'gzip, deflate',
	    "Accept-Language":'zh-CN,zh;q=0.9',
	    "Cache-Control":'max-age=0',
	    "Connection":'keep-alive',
	    "Cookie":'usertrack=ezq0pVpZdXcigr4cFc+bAg==; _ntes_nnid=b610a7114d9ef1256a7a501a2cc30eb7,1515915838724; _ntes_nuid=b610a7114d9ef1256a7a501a2cc30eb7; nts_mail_user=Mxueshu2016@163.com:-1:1; mail_psc_fingerprint=a4eb1d8c9fa5b2d146f61cfe877c5079; P_INFO=mxueshu2016@163.com|1516199601|0|mail163|00&99|gud&1516186545&mail163#gud&440100#10#0#0|137482&0|mail163|mxueshu2016@163.com; vjuids=-9a20cea6.16136ae9924.0.9722b9a95a248; vjlast=1517040868.1517105984.13; cm_newmsg=user%3Dmxueshu2016%40163.com%26new%3D-1%26total%3D-1; ne_analysis_trace_id=1517106136715; s_n_f_l_n3=dc583099efd3eae41517106136720; vinfo_n_f_l_n3=dc583099efd3eae4.1.0.1517106136719.0.1517106170571',
	    "Host":'quotes.money.163.com',
	    #"Referer":'http://quotes.money.163.com/trade/lsjysj_600050.html?year=2018&season=2',
	    "Upgrade-Insecure-Requests":'1',
	    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    testLink = 'http://quotes.money.163.com/trade/lsjysj_600050.html?year=2018&season=1'
    years = list(range(2002,2019))
    seasons = list(range(1,5))
    Company2Codes = {}
    allCompanys2Links = {}

    # game start Here
    # 1- 导入所有股票代码以及链接
    importCodes()

    # 2- 公司对应链接
    for company,code in Company2Codes.items():
        tempLink = r'http://quotes.money.163.com/trade/lsjysj_' + code + r'.html'
        # ?year=2018&season=1
        allCompanys2Links[company] = tempLink
    #print(allCompanys2Links)

    #3- 爬取数据
    getSharesHtml(allCompanys2Links)

    endTime = time.time()
    print("用时：",str((endTime-startTime)//60),"分钟")