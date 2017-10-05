---
title: Eason Projects
date: 2017-10-5 16:05:17
tags:
  - Python3
categories:
  - 爬虫
---
作为一个Eason Fan，连写代码、做项目也是喜欢在Eason上面花心思的……

### 1.intro
汇总目前我做过的关于Eason（陈奕迅）的项目，包括以下几个
>* [Eason_Film.py](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/Eason_Film.py)：爬取豆瓣所有Eason电影列表
>* [music163_EasonLyrics](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics)：网易云平台Eason所有单曲歌词爬虫，文本分析
>* [music163_EasonComments](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments)：网易云平台Eason所有单曲评论数、热门评论&最新10条评论爬虫，文本分析

### 2.结果分析
#### 2.1 Eason_Film
一共爬取到**67**部电影，详见[Eason电影.txt](https://github.com/Eajack/py_spider/blob/master/%E9%9D%99%E6%80%81%E7%88%AC%E8%99%AB/Eason%E7%94%B5%E5%BD%B1.txt)

#### 2.2 music163_EasonLyrics
##### 2.2.1 歌词
一共爬取到**536**首歌歌词（去重），歌词txt文件详见[Lyrics](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/Lyrics)

##### 2.2.2 结果图片
图片结果如下：

![Eason歌词词云图](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs/EasonLyricsCloud.png "Eason歌词词云图")

上图为歌词词云图

![TOP 30词频柱形图](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs/%E5%89%8D30%E8%AF%8D%E9%A2%91%E6%9F%B1%E5%BD%A2%E5%9B%BE.png "TOP 30词频柱形图")

![TOP 30词频饼状图](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs/%E5%89%8D30%E8%AF%8D%E9%A2%91%E9%A5%BC%E7%8A%B6%E5%9B%BE.png "TOP 30词频饼状图")

由上述二图分析可知，词频最高的词语为**“没有”**，其次为“一个”、“我们”等

![情绪分析折线图.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs/%E6%83%85%E7%BB%AA%E5%88%86%E6%9E%90%E6%8A%98%E7%BA%BF%E5%9B%BE.png "情绪分析折线图")

![情绪分析比例饼状图.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs/%E6%83%85%E7%BB%AA%E5%88%86%E6%9E%90%E6%AF%94%E4%BE%8B%E9%A5%BC%E7%8A%B6%E5%9B%BE.png "情绪分析比例饼状图.png")

上述二图为情绪分析指数结果图，由于运用的是snownlp库，但该库是主要针对商品评论做的情感分析库……未免与实际情况有所偏差。结果分析得知歌词情绪分析指数呈“两边低，中间高”分布，评分多集中在0.5~0.8，评分越高，说明歌曲的积极程度越高。同时，取情绪指数 >= 0.6的作为正面情绪，统计出比例，并做出饼状图，发现Eason的歌**正面情绪歌曲竟然占比67%**……看来Eason唱的歌还是挺积极的啊……

#### 2.3 music163_EasonComments
##### 2.3.1 评论数据分析
**截止2017.10.3凌晨**（具体忘了时间），一共爬取到**5451**条热门评论，详见[hotComments.xls](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultXLS/hotComments.xls)；爬取最新10条评论，共**8492**条，详见[Newcomments.xls](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultXLS/Newcomments.xls)；爬取到**858**首单曲以及对应的网易云单曲ID，详见[songName2ID.xls](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultXLS/songName2ID.xls)；爬取到所有单曲评论数，详见[songName2commentsNum.xls](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultXLS/songName2commentsNum.xls)取前10排行如下：

| 歌名 | 评论数 |
|--|--|
| 陪你度过漫长岁月 - (电影《陪安东尼度过漫长岁月》主题曲) | 79350 |
| 好久不见 | 67875 |
| 十年 | 60062 |
| 不要说话 | 56746 |
| 阴天快乐 | 50840 |
| 可以了 | 40998 |
| 让我留在你身边 - (电影《摆渡人》爱情版主题曲) | 38108 |
| 淘汰 | 36806 |
| 富士山下 | 36433 |
| 最佳损友 | 34811 |

**评论过1w的歌曲数量仅有38首**，**999+歌曲有241首**，感觉比周董的百万《晴天》以及很多的过万歌差别很远啊……最低评论（去除最新专辑《C’mon in~》的需收费，未公开的《未知track》0评论）歌曲是《美丽有罪 (James Ting Remix)》，仅**1**条评论（应该是版权也没了）

##### 2.3.2 评论文本分析

![热门评论词云.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultsPNGs/%E7%83%AD%E9%97%A8%E8%AF%84%E8%AE%BA%E8%AF%8D%E4%BA%91.png "热门评论词云.png")

上图为热门评论词云图

![TOP 30词频柱形图.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultsPNGs/%E5%89%8D30%E8%AF%8D%E9%A2%91%E6%9F%B1%E5%BD%A2%E5%9B%BE.png "TOP 30词频柱形图.png")

![TOP 30词频饼状图.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultsPNGs/%E5%89%8D30%E8%AF%8D%E9%A2%91%E9%A5%BC%E7%8A%B6%E5%9B%BE.png "TOP 30词频饼状图.png")

上述二图为热门评论词频分析图，可知词频最高的是“首歌”（这里jieba分词可能有点问题），之后是“一个”（其实该词属于常用词，照理可以剔除）。因此，在我心目中，词频最高的是“喜欢”，第二是“陈奕迅”，也符合常理啦~~

![情绪指数曲线.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultsPNGs/%E6%83%85%E7%BB%AA%E6%8C%87%E6%95%B0%E6%9B%B2%E7%BA%BF.png "情绪指数曲线.png")

![情绪分析饼状比例图.png](https://raw.githubusercontent.com/Eajack/py_spider/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonComments/resultsPNGs/%E6%83%85%E7%BB%AA%E5%88%86%E6%9E%90%E9%A5%BC%E7%8A%B6%E6%AF%94%E4%BE%8B%E5%9B%BE.png "情绪分析饼状比例图.png")

情绪分析套路与前面类似，只是在处理文本方面有些许不同。在这里，我们也可以看到snownlp库的不足了……（虽然也不知道是不是对的，但感觉上不是十分靠谱）。此处情感曲线呈类似指数函数趋势（这结果也是厉害……），正面情绪评论比重为76%，此处不多做分析。

### 3.New Ideas
以上是目前关于做过的关于Eason的项目，比较偏软件方面，均为Python爬虫。此外，作为Eason Fan，我是十分羡慕Eason的歌喉的。个人有一个长远Project：做一个DSP音频处理器（软件 or 硬件），将自己的声音处理变成Eason的声音。由于个人认为该项目难度相当大，所以作为一个长期Project，或许几年之后才能做出了，但希望自己能坚持做。具体项目细节、所需技术&目标等还没细想，之后开工后会继续慢慢想着

### 4.More
Python爬虫项目玩了有一阵子了，从暑假开始玩，现在也该不玩了。个人所有Py3爬虫项目以及思路、结果等在GitHub：[py_spider](https://github.com/Eajack/py_spider)，也不是很牛逼的东西，纯属娱乐~~

现在要开坑CV + 算法了……希望，如果有人看到这文章，有点子或者想讨论的可以多多评论留言~~