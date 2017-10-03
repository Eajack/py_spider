#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# ==================================================================================================================
# Author: Eajack
# date:2017/10/2
# ==================================================================================================================
# Function：
#   1- 歌曲ID => 爬取所有评论数 & 前10的评论
#   2- 歌曲ID => 爬取当前精彩评论
# ==================================================================================================================
# keyPoints:
#   1- 加密信息的使用（来源知乎，百度等）
#   2- xlwt,xlrd使用
# ==================================================================================================================

import requests
import json,os,time
import xlwt,xlrd
from xlutils.copy import copy
from xlwt import Style


def getCommentsNum():
    '''
        获取所有单曲评论数 & 最新10条评论
    :return: 
    '''
    # 遍历excel表格
    os.chdir(r'D:\STUDYING\MyProjects\pycharm\music163_EasonComments')
    xlsFile = xlrd.open_workbook('songName2ID.xls',formatting_info=True)
    sheet = xlsFile.sheets()[0]
    rowNum = sheet.nrows
    colNum = sheet.ncols

    totalFailCount = 0
    for row in range(0, rowNum):
        time.sleep(5)
        # 1- 获取songName & songID
        songName = sheet.cell(row, 0).value
        songID = sheet.cell(row, 1).value

        # 2- 爬取comment
        headers = {
            'Cookie': 'appver=1.5.0.75771',
            'Referer': 'http://music.163.com',
        }
        user_data = {
            'params': 'vRlMDmFsdQgApSPW3Fuh93jGTi/ZN2hZ2MhdqMB503TZaIWYWujKWM4hAJnKoPdV7vMXi5GZX6iOa1aljfQwxnKsNT+5/uJKuxosmdhdBQxvX/uwXSOVdT+0RFcnSPtv',
            'encSecKey': '46fddcef9ca665289ff5a8888aa2d3b0490e94ccffe48332eca2d2a775ee932624afea7e95f321d8565fd9101a8fbc5a9cadbe07daa61a27d18e4eb214ff83ad301255722b154f3c1dd1364570c60e3f003e15515de7c6ede0ca6ca255e8e39788c2f72877f64bc68d29fac51d33103c181cad6b0a297fe13cd55aa67333e3e5'
        }

        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % (songID,)
        r = requests.post(url, headers=headers, data=user_data)
        if r.status_code == 200 and r.text.find('comments') != -1:
            commentsNum = json.loads(r.text)['total']
            print(songName,commentsNum)

            # 储存commentsList
            commentsList = []
            last_comments = json.loads(r.text)['comments']
            for count in range(0, len(last_comments)):
                commentBuffer = last_comments[count]['content']
                commentsList.append(commentBuffer)
            print(commentsList)

        # 3- 储存songName => 评论数
        os.chdir(r'D:\STUDYING\MyProjects\pycharm\music163_EasonComments')
        if os.path.exists('songName2commentsNum.xls'):
            # 文件存在即可写入数据
            commentxlsFile = xlrd.open_workbook('songName2commentsNum.xls',formatting_info=True)
            sheet0 = commentxlsFile.sheets()[0]
            rowNum = sheet0.nrows

            writeFile = copy(commentxlsFile)
            ws = writeFile.get_sheet(0)
            style = Style.default_style
            ws.write(rowNum, 0, songName, style)
            ws.write(rowNum, 1, commentsNum, style)
            writeFile.save('songName2commentsNum.xls')
        else:
            # 文件不存在则创建excel文件，之后写入songName & songID
            commentxlsFile = xlwt.Workbook()
            sheet1 = commentxlsFile.add_sheet('songName2commentsNum')
            sheet1.write(0, 0, songName)
            sheet1.write(0, 1, commentsNum)
            commentxlsFile.save("songName2commentsNum.xls")

        # 4- 储存最新评论
        os.chdir(r'D:\STUDYING\MyProjects\pycharm\music163_EasonComments')
        if os.path.exists('Newcomments.xls'):
            # 文件存在即可写入数据
            commentxlsFile = xlrd.open_workbook('Newcomments.xls',formatting_info=True)
            sheet2 = commentxlsFile.sheets()[0]
            rowNum = sheet2.nrows

            writeFile = copy(commentxlsFile)
            ws = writeFile.get_sheet(0)
            style = Style.default_style
            rowIndex = rowNum
            for comment in commentsList:
                ws.write(rowIndex, 0, comment, style)
                rowIndex += 1

            writeFile.save('Newcomments.xls')
        else:
            # 文件不存在则创建excel文件，之后写入评论
            commentxlsFile = xlwt.Workbook()
            sheet3 = commentxlsFile.add_sheet('Newcomments')
            for commentCount in range(0,len(commentsList)):
                sheet3.write(commentCount, 0, commentsList[commentCount])
            commentxlsFile.save("Newcomments.xls")

def getHotcomments():
    '''
        获取精彩评论，并储存为hotComments.xls
    :return: 
    '''
    # 加密信息
    payload = {
        'params': '4hmFbT9ZucQPTM8ly/UA60NYH1tpyzhHOx04qzjEh3hU1597xh7pBOjRILfbjNZHqzzGby5ExblBpOdDLJxOAk4hBVy5/XNwobA+JTFPiumSmVYBRFpizkWHgCGO+OWiuaNPVlmr9m8UI7tJv0+NJoLUy0D6jd+DnIgcVJlIQDmkvfHbQr/i9Sy+SNSt6Ltq',
        'encSecKey': 'a2c2e57baee7ca16598c9d027494f40fbd228f0288d48b304feec0c52497511e191f42dfc3e9040b9bb40a9857fa3f963c6a410b8a2a24eea02e66f3133fcb8dbfcb1d9a5d7ff1680c310a32f05db83ec920e64692a7803b2b5d7f99b14abf33cfa7edc3e57b1379648d25b3e4a9cab62c1b3a68a4d015abedcd1bb7e868b676'
    }

    # 遍历excel表格
    os.chdir(r'D:\STUDYING\MyProjects\pycharm\music163_EasonComments')
    xlsFile = xlrd.open_workbook('songName2ID.xls', formatting_info=True)
    sheet = xlsFile.sheets()[0]
    rowNum = sheet.nrows

    for row in range(0, rowNum):
        time.sleep(5)
        # 获取songID
        songName = sheet.cell(row,0).value
        songID = sheet.cell(row, 1).value
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=5594eaee83614ea8ca9017d85cd9d1b3'.format(songID)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            'Referer': 'http://music.163.com/song?id={}'.format(songID),
            'Host': 'music.163.com',
            'Origin': 'http://music.163.com'
        }

        response = requests.post(url=url, headers=headers, data=payload)
        data = json.loads(response.text)
        hotcomments = []
        for hotcomment in data['hotComments']:
            item = {
                'nickname': hotcomment['user']['nickname'],
                'content': hotcomment['content']
            }
            hotcomments.append(item)

        # 2- 储存热门评论
        commentsList = [content['content'] for content in hotcomments]
        print(songName)
        print(commentsList)
        os.chdir(r'D:\STUDYING\MyProjects\pycharm\music163_EasonComments')
        if os.path.exists('hotComments.xls'):
            # 文件存在即可写入数据
            commentxlsFile = xlrd.open_workbook('hotComments.xls',formatting_info=True)
            sheet2 = commentxlsFile.sheets()[0]
            rowNum = sheet2.nrows

            writeFile = copy(commentxlsFile)
            ws = writeFile.get_sheet(0)
            style = Style.default_style
            rowIndex = rowNum
            for comment in commentsList:
                ws.write(rowIndex, 0, comment, style)
                rowIndex += 1

            writeFile.save('hotComments.xls')
        else:
            # 文件不存在则创建excel文件，之后写入评论
            commentxlsFile = xlwt.Workbook()
            sheet3 = commentxlsFile.add_sheet('hotComments')
            for commentCount in range(0,len(commentsList)):
                sheet3.write(commentCount, 0, commentsList[commentCount])
            commentxlsFile.save("hotComments.xls")


if __name__ == '__main__':
    getCommentsNum()
    getHotcomments()
