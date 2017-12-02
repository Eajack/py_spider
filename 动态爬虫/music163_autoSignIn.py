#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# ==================================================================================================================
# Author: Eajack
# date:2017/12/2
# ==================================================================================================================
# Function：
#   1- 网易云自动签到
# ==================================================================================================================
# keyPoints:
#   1- 关掉微博登录保护
#   2- chromedriver 版本为2.33
#   3- Windows下代码自动化设置指南：http://blog.csdn.net/wwy11/article/details/51100432
# ==================================================================================================================

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json,os,re,time
import xlwt,xlrd


def autoSignIn(weiboNum,WeiboPassword):
    #global
    global music163,music163_loginUrl
    #1- 先打开网易云主页
    driver = webdriver.Chrome()
    time.sleep(5)
    driver.maximize_window()    #窗口最大化
    driver.implicitly_wait(10)  # 隐式等待
    driver.get(music163)

    #2- 打开新Tab
    js = r" window.open(' " + music163_loginUrl + r"')"  # 可以看到是打开新的标签页，不是窗口
    driver.execute_script(js)
    ## driver切换窗口对象
    handles = driver.window_handles # handle[1]为登录页面
    driver.switch_to_window(handles[1])

    ## 模拟登录
    driver.find_element_by_id('userId').clear()
    driver.find_element_by_id('userId').send_keys(weiboNum)
    driver.find_element_by_id('passwd').clear()
    driver.find_element_by_id('passwd').send_keys(WeiboPassword)
    time.sleep(5)
    driver.find_element_by_class_name('WB_btn_login').click()   #className不允许使用复合类名做参数
    time.sleep(5)

    #3- 签到
    handles = driver.window_handles
    driver.switch_to_window(handles[0])
    driver.refresh()
    time.sleep(5)
    ## 切换框架（关键）
    driver.switch_to_frame('contentFrame')
    driver.find_element_by_class_name('sign').click()  # className不允许使用复合类名做参数
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    # global
    ## 网易云请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie':'_ntes_nnid=7c54eed773126f0650dae5becf0abded,1512053591165; _ntes_nuid=7c54eed773126f0650dae5becf0abded; JSESSIONID-WYYY=P94BQwYtCVwjGcBkC%2FpSkryKMgh%2F9SOviaez0CE530QWPH1E6v9c7Ju0zl3BwZn7D6Wroyatha9vZkRlwPXvrpOcV1%2Foms8drMDlkGemtVJEWtyXei%2FbAPqs46Hia6GgI9E6XIykMZGKTPZDQzB5CgeVtIv2PWWDEnheEwMlXcK0FW7H%3A1512193719433; _iuqxldmzr_=32',
        'DNT': '1',
        'Host': 'music.163.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    ## 网易云链接
    music163 = r'http://music.163.com/'
    music163_loginUrl = r'https://api.weibo.com/oauth2/authorize?client_id=301575942&response_type=' +\
                    r'code&redirect_uri=http://music.163.com/back/weibo&forcelogin=true&scope=' +\
                    r'friendships_groups_read,statuses_to_me_read,follow_app_official_microblog&' +\
                    r'state=zHZaAMjuvv'
    ## 账号密码
    weiboNum = '15219721307'
    WeiboPassword = 'CGHLYJ30144?!'

    # 开始
    autoSignIn(weiboNum,WeiboPassword)