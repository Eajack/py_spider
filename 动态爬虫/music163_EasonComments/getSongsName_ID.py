#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# ==================================================================================================================
# Author: Eajack
# date:2017/10/2
# ==================================================================================================================
# Function：
#   1- 爬取网易云Eason所有歌名 => 歌曲ID，并储存为excel文件
# ==================================================================================================================
# keyPoints:
#   1- xlrd,xlwt读写excel表格操作
# ==================================================================================================================


from bs4 import BeautifulSoup
import requests
import json,os,re,time
from selenium import webdriver
import xlwt,xlrd


# 获取Eason 所有专辑ID
def getAlbumIDList(singerID, limit):
    '''
    Function：
        1- 获取Eason 所有专辑ID
    :param singerID: 2116
    :param limit: 12

    :return: albumIDList => list
    '''
    global albumIDList

    subAlbumLink = r'https://music.163.com/#/artist/album'

    # 由于需要转移frame，需要selenium
    for offset in range(0, 108, 12):
        # selenium部分
        # albumLink eg: https://music.163.com/#/artist/album?id=2116&limit=12&offset=0
        albumLink = subAlbumLink + r"?id=" + str(singerID) + r"&limit=" + str(limit) + r"&offset=" + str(offset)
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # 隐式等待
        driver.get(albumLink)
        time.sleep(5)  # 等待
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))  # 关键，转换frame
        html = BeautifulSoup(driver.page_source, "lxml")

        # soup页面解析，获取当前页面所有歌曲ID
        for albumIDtag in html.findAll("a", {"href": re.compile("^\/album\?id\=.*")}):
            albumID = albumIDtag["href"].replace("/album?id=", "")
            if albumID not in albumIDList:
                albumIDList.append(albumID)

        # 浏览器关闭
        driver.quit()


# 获取Eason所有专辑内单曲歌曲ID以及所有歌名
def getSongIDandsongNameList():
    '''
    Function:
        1- 获取Eason所有专辑内单曲歌曲ID以及所有歌名
        2- 过滤同一首歌
    :return: songName2ID_dict[songName] = songID
    '''
    global albumIDList, songName2ID_dict

    subInnerAlbumLink = r'https://music.163.com/#/album'
    haveName = False

    # 由于需要转移frame，需要selenium
    for albumID in albumIDList:  # 根据网址总结规律
        # selenium部分
        # InnerAlbumLink eg: https://music.163.com/#/album?id=35835294
        albumLink = subInnerAlbumLink + r"?id=" + str(albumID)
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # 隐式等待
        driver.get(albumLink)
        time.sleep(5)  # 等待
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))  # 关键，转换frame
        html = BeautifulSoup(driver.page_source, "lxml")

        # soup页面解析，获取当前页面所有歌曲ID
        for songIDtag in html.findAll("a", {"href": re.compile("^\/song\?id\=.*")}):
            songID = songIDtag["href"].replace("/song?id=", "")
            songName = str(songIDtag.b["title"])
            songName2ID_dict[songName] = songID
            ##debug use
            print(songID, songName)

        # 浏览器关闭
        driver.quit()

    # excel文件储存songName2ID_dict
    xlsxFile = xlwt.Workbook()
    sheet = xlsxFile.add_sheet('songName2ID')

    songCount = 0
    for songName, songID in songName2ID_dict.items():
        # 填充名字
        sheet.write(songCount, 0, songName)
        # 填充链接
        sheet.write(songCount, 1, songID)
        songCount += 1

    xlsxFile.save("songName2ID.xls")

if __name__ == '__main__':
    # global
    ## 网易云请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ntes_nnid=e76639646686a8ddf4dbd9f865dbfe4e,1503039315399; _ntes_nuid=e76639646686a8ddf4dbd9f865dbfe4e; MUSIC_A=2ef1d1bf10e0970aa8ef2a400e11078ecfd091512723c7fb5f9d567371dac57a16f827d623128710018b9570d66b88bfb23ea72ab5261c23fb97b0129e36bdf9f546586f7bb9e6ae8328c980cd21a668; os=uwp; osver=10.0.14393.447; appver=1.3.3; deviceId=0d56743a3d5158a11f5a1fbf3a7dc746; FromPlatform=uwp; playerid=74378889; __csrf=87d059fd2c8ddc7e9cf4110cb944c364; JSESSIONID-WYYY=eXN26albKtQloWhh8EfQV77Qw519A%5Cl7vzcIjnvdMC%5CSufYdMklqQW%5C4vvSVi%5Cr0HWuK8hlb1g35D4IMcEC0h%5C6hl%5C14iF4XK5Wr%5CWflTCSH0p%2FbekQt4CuC%5CvXbN43GwErri0Brp%5CFipMllOCmfBZxiDq9qCJgkQOlsNGAkc%5CqRVGJu%3A1503483000489; _iuqxldmzr_=32',
        'DNT': '1',
        'Host': 'music.163.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    ## 专辑ID统计
    albumIDList = []
    ## key:歌名,value:ID
    songName2ID_dict = {}


    start = time.time()

    # 1- 先获取Eason所有专辑ID
    singerID = 2116
    limit = 12
    getAlbumIDList(singerID, limit)
    # 2- 遍历所有专辑ID获取所有歌曲ID & 所有歌名,并利用excel文件储存
    getSongIDandsongNameList()

    end = time.time()
    print("总共大约用时%d分钟" % ((end - start) // 60))