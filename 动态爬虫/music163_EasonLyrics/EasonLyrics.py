#!/usr/bin/env python3
# -*- coding : utf-8 -*-
#==================================================================================================================
# Author: Eajack
# date:2017/8/23 - 2017/8/26
#==================================================================================================================
# Function：
#   1- 爬取网易云Eason所有歌曲歌词储存为txt
#==================================================================================================================
# keyPoints:
#   1- 网易云音乐的html中frame套frame，需要用selenium转换frame才能找到元素，bs不行
#       driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))
#   2- 经典的 utf-8(unicode) => gbk 编码问题，有两个问题
#       1)- windows下文件标题不能有 “/ ” “\”等标点符号
#       解决:fileName = fileName.replace("\xa0", " ")
#            fileName = fileName.replace("/", " ")
#            fileName = fileName.replace(" ", "")。记得加上 “ fileName = ”
#       2)- windows下txt文件内容编码默认为gbk
#       解决：txtFile = open(fileName,'w',encoding='utf-8')。改编码方式为utf-8
#             也可以顺便lyric = lyric.replace(u"\xa0",u" ")以备以后读取编码问题
#==================================================================================================================
# Console:
# 没有歌词的歌曲：
#      ['L.I.F.E.Overture.txt', '那一夜没有雪.txt', '孤儿仔.txt', '想哭.txt', 'MusicOnly.txt', '黎喇.txt',
#       'EasonsAngel.txt', '27Seconds.txt']
# 下载失败的歌曲: []
# 总共大约用时30分钟
#==================================================================================================================
# Attention：
#   Medley文件需删去
#==================================================================================================================

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
import os
import re
import time
# selenium库
from selenium import webdriver

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
## 下载失败歌名
downloadFailedSong = []
## 没有歌词的歌名
noLyricsSong = []

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

# 获取Eason所有专辑内单曲歌曲ID以及所有歌名，过滤同样歌名歌曲
def getSongIDandsongNameList():
    '''
    Function:
        1- 获取Eason所有专辑内单曲歌曲ID以及所有歌名
        2- 过滤同一首歌
    :return: songName2ID_dict[songName] = songID
    '''
    global albumIDList,songName2ID_dict

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

            ## songName 去重处理 & 字符串处理
            index1 = songName.find("-")
            index2 = songName.find("(")
            if (index1 != -1):
                songName = songName[0:index1]
            if (index2 != -1 and index2 != 0):
                songName = songName[0:index2]
            elif(index2 == 0):
                index3 = songName.find("(",index2+1)
                songName = songName[0:index3]
            songName = songName.strip()

            ## 空列表处理，直接赋值
            if(len(songName2ID_dict) == 0):
                songName2ID_dict[songName] = songID

                #debug use
                print(songID, songName)

                continue

            ## 判断songNameList中是否有同一首歌曲
            for currentsongName in songName2ID_dict.keys():
              ## 存在歌曲了，包括剔除live版本等其它版本，因为歌词一样
              if (currentsongName == songName):
                haveName = True
                break
              else:
                haveName = False

            ## 判断有无歌曲后操作
            if (haveName):
              continue
            else:
              if (songID not in songName2ID_dict.values()):
                songName2ID_dict[songName] = songID
                ##debug use
                print(songID,songName)

        # 浏览器关闭
        driver.quit()

# 获取歌词，储存为txt文件
def getLyric():
    '''
    Function:
        1- 获取歌词
        2- 并储存为txt文件
    :param:
        songName2ID_dict => dict
            songName2ID_dict[songName] = songID
    :return: txt歌词文档
    '''
    global headers,songName2ID_dict,downloadFailedSong,noLyricsSong

    for songName,songID in songName2ID_dict.items():
        ## 0- 判断文件是否存在
        ## 转移目录
        lyricPath = r"D:\STUDYING\MyProjects\pycharm\music163_EasonLyrics\Lyrics"
        os.chdir(lyricPath)
        ## 文件名
        fileName = songName + ".txt"
        ## 关键点:\xa0 编码问题，记得除了“fileName.replace("\xa0", " ")”，还有 “fileName =”
        fileName = fileName.replace("\xa0", " ")
        fileName = fileName.replace("/", " ")
        fileName = fileName.replace(" ", "")
        ## 判断文件是否存在
        if os.path.exists(fileName):
            continue

        # 1-爬取歌词
        ## 网页解析，关键在于songID
        lyricUrl = r'http://music.163.com/api/song/lyric?' + 'id=' + str(songID) + r'&lv=1&kv=1&tv=-1'
        request = requests.get(lyricUrl, headers=headers)
        request.encoding = 'utf-8'
        lyric_json = request.text
        ## 读取JSON文件
        lyric_dict = json.loads(lyric_json)

        try:# 歌曲没有歌词
            lyric = lyric_dict["lrc"]["lyric"]
            ## 正则去掉 [00:00.00] 类似
            extra = re.compile("\[.*\]")
            lyric = re.sub(extra, "", lyric)
            lyric = lyric.strip()
        except KeyError as e:
            noLyricsSong.append(fileName)
            continue

        # 2-储存为txt文件
        ## 储存为txt文件
        try:
            txtFile = open(fileName,'w',encoding='utf-8')
            lyric = lyric.replace(u"\xa0",u" ")
            txtFile.write(lyric)
            txtFile.close()
            print(songName + "\t已经下载完歌词啦")
        except UnicodeEncodeError:
            downloadFailedSong.append(songName)

        # # debug use
        # print(lyric)

if __name__ == '__main__':
    start = time.time()

    # 1- 先获取Eason所有专辑ID
    singerID = 2116
    limit = 12
    getAlbumIDList(singerID, limit)
    # 2- 遍历所有专辑ID获取所有歌曲ID & 所有歌名
    getSongIDandsongNameList()
    # 3- 遍历所有歌曲ID获取歌词
    getLyric()
    ## 没歌词的歌以及下载失败的歌
    print("没有歌词的歌曲：")
    print(noLyricsSong)
    print("下载失败的歌曲:")
    print(downloadFailedSong)

    end = time.time()
    print("总共大约用时%d分钟"%((end - start) // 60) )