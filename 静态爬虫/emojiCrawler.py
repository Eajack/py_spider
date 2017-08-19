#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Author: Eajack
# date:2017/8/7
# Function：
#   爬取emoji官网 http://emojipedia.org/ 所有emoji表情包图片
# 缺点(补坑）：1- 缺少多线程，下载速度慢
#			  2- 缺少IP代理,要解决被封危险
#			  3- 缺少try-except 异常处理

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import urlretrieve
import requests
import os
import re
import time

def makeFolder(folderName):
	'''
	在当前路径，创建文件夹
	'''
	failed = 0
	if os.path.exists(folderName):
		pass
	else:
		try:
			os.mkdir(folderName)
		except NotADirectoryError:
			# print(folderName + "failed")
			failed = 1
	return failed

def downloadImg(imgUrl,fileName):
	'''
    下载图片imgUrl，到路径fileName
	'''
	if os.path.exists(fileName):
		pass
	else:
		urlretrieve(emojisrcs[index],fileName)

# 构造请求头，解析起始页面
headers = {"User-Agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
						 "AppleWebKit/537.36 (KHTML, like Gecko)"
						 "Chrome/59.0.3071.115 Safari/537.36",
		   "Accept":"text/html,application/xhtml+xml,application/xml;"
					"q=0.9,image/webp,image/apng,image/*,*/*;q=0.8",
		   "Connection":"keep-alive"
}
url = "http://emojipedia.org/"
request = requests.get(url,headers = headers)
request.encoding = 'utf-8'
html = request.text
bsObj = soup(html,'lxml')

# 路径初始化
currentPath = os.getcwd()
makeFolder("emojiImage")
ImgPath = currentPath + '\emojiImage'
os.chdir(ImgPath)

# 获得所有子分类的链接
subLinks = []
categoriesFolderNames = []
for subLink in bsObj.find("ul").findAll("a"):
	subLinks.append(subLink.attrs['href'])
	#二级文件夹命名
	categoriesFolderName = subLink.get_text()
	categoriesFolderNames.append(categoriesFolderName)
	trashNum = makeFolder(categoriesFolderName)

# 遍历所有子分类页面爬取所有emoji图片
count = 0   #计数，以便路径管理便于文件夹命名
for subLink in subLinks:
	#路径转移为当前emoji子分类目录下
	os.chdir(ImgPath + "\\" + categoriesFolderNames[count])

	#判断当前文件夹是否已经下载完图片，为了爬虫中断后能快速继续下载
	# 后期补充
	# folderName = categoriesFolderNames[count]
	# if (folderName == "😃 Smileys & People" or folderName == "🐻 Animals & Nature" or
	#			folderName == "🍔 Food & Drink" or folderName == "⚽ Activity"):
	#	count += 1
	#	continue

	# imgCount = len([x for x in os.listdir(os.path.dirname(__file__)) if os.path.isfile(x)])

	# if (imgCount == 12 or imgCount == 8):
	#	continue

	#获取当前页面所有表情子链接
	subUrl = url + subLink
	request2 = requests.get(subUrl, headers=headers)
	request2.encoding = 'utf-8'
	html2 = request2.text
	bsObj2 = soup(html2, 'lxml')

	# minFolderNames = []
	failnum = 0
	for emojiHref in bsObj2.find("ul",{"class":"emoji-list"}).findAll("a"):
		# emojiHrefs.append(emojiHref.attrs['href'])
		emojiHrefValue = emojiHref.attrs['href']
		emojiLink = url + emojiHrefValue
		# 三级文件夹命名
		minFolderName = emojiHrefValue[1:-1]
		# minFolderNames.append(minFolderName)
		failnum += makeFolder(minFolderName)


		#下载emojiLink图片，并放在minFolderName文件夹下
		os.chdir(minFolderName)
		request3 = requests.get(emojiLink, headers=headers)
		request3.encoding = 'utf-8'
		html3 = request3.text
		bsObj3 = soup(html3, 'lxml')

		emojiTypes = []
		emojisrcs = []
		for emojiType in bsObj3.find("section",{"class":"vendor-list"}).find("ul").findAll("h2"):
			emojiTypes.append(emojiType.get_text())

		for emojisrc in bsObj3.find("section",{"class":"vendor-list"}).findAll("img",{"src":re.compile("^(http)")}):
			emojisrcs.append(emojisrc.attrs['src'])

		if (len(emojiTypes) == len(emojisrcs)):
			for index in range(0,len(emojiTypes)):
				fileName = os.path.join(os.getcwd(), (emojiTypes[index] + ".png"))
				downloadImg(emojisrcs[index],fileName)
				time.sleep(2)
				# print("Finish!!")
				index += 1
		else:
			print("名字数量与链接数量不一致")

		os.chdir(ImgPath + "\\" + categoriesFolderNames[count])

	#文件夹完成时
	print("---------------------------------------------------------")
	print(categoriesFolderNames[count] + "已经下载完成")
	# 输出创建失败文件夹个数
	print("%s has %d failed"%(categoriesFolderNames[count],failnum) )

	count += 1