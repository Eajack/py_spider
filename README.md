
# Eajack's python爬虫项目汇总

## 1、运行环境

> * Windows or Linux
> * Python3.5.2(Python 3.x.x)

## 2、内置库汇总

> * urllib
> * re,os,time
> * json

## 3、第三方库汇总

> * bs4(BeautifulSoup)
> * requests
> * selenium
> * jieba
> * wordcloud
> * matplotlib
> * scipy
> * snownlp
> * xlwt
> * xlrd
> * [updating...]

## 4、爬虫说明

> * [computer_books.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/computer_books.py)：豆瓣"世界著名计算机教材节选"爬虫
> * [Eason_Film.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/Eason_Film.py)：豆瓣"Eason电影"爬虫
> * [emojiCrawler.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/emojiCrawler.py)：[emoji官网](http://emojipedia.org/)爬虫，按官网分类爬取所有不同版本的emoji.png图片（eg:Apple,Samsung.Google etc.)
> * [wiki_6DegreeSeperation.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/wiki_6DegreeSeperation.py)：wiki爬虫，广度优先遍历，为证明“六度分割理论”，暂时只能尝试，并非完全证明
> * [music163_EasonLyrics](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics)：网易云Eason所有歌词爬虫 + 文本分析，详见[EasonLyrics_README](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/EasonLyrics_README.md)
> * [getCity.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/getCity.py)：基于谷歌地图API简单爬虫，通过经纬度查询该地点所属城市
> * [music163_EasonComments](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments)：网易云Eason所有单曲评论数排行、最新10条评论抓取 & 热门评论文本分析，详见[EasonComments_README](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/EasonComments_README.md)
> * [music163_autoSignIn.py](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_autoSignIn.py)：网易云音乐网页端，每天定时自动签到（windows）
> * [updating...]

## 5、留坑

> * 多线程/进程（解决爬虫太慢）
> * Python编程技巧
> * [updating...]
