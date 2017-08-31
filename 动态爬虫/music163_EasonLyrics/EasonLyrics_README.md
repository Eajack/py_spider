## music163_EasonLyrics项目

### 1、intro
> 1)-[EasonLyrics.py](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/EasonLyrics.py)：Eason网易云歌词爬虫

> 2)-[wordsAnalysis.py](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/wordsAnalysis.py):

>* 歌词文本分析，包括jieba分词统计词汇（去单字）
>* 根据词频生成词云
>* 词频统计，做柱形图 & 饼状图
>* 歌词情绪分析简易版demo (饼状图 & 曲线图)

> 3)-[Lyrics](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/Lyrics):下载的歌词txt文档

> 4)-[resultsPNGs](https://github.com/Eajack/py_spider/tree/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/resultsPNGs):所有分析结果图片汇总

> 5)-[Eason](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/Eason.jpg):Eason图片词云背景图

### 2、思路
#### 1）EasonLyrics思路
获取所有Eason专辑ID => 遍历专辑得到单曲ID并过滤同名歌曲 => 通过api`http://music.163.com/api/song/lyric?id=[IDNUM]`获得歌词，并储存为txt文件
#### 2）文本分析思路
jieba库、wordcloud库、matplotlib库、snownlp库的使用。多百度、google&github。

### 3、遇到的问题以及解决思路
#### 1）爬取歌词思路选择
1. **bs+urllib**：一开始的时候，原本想通过网站`http://music.163.com/#/search/m/?s=陈奕迅`翻页遍历。但是发现用bs无法爬取，因为翻页网址没变，但在chrome里面的检查源码变了，但直接用bs+urllib爬不了html源码，只可以得到首页源码（而且后来发现bs爬的源码和chrome端不一样，因为html里面嵌入了frame，需要selenium库转换frame）
2. **selenium模拟翻页**：转变思路后，但我还是想通过搜索页翻页爬取。百度发现说，可能是`Ajax`、js渲染或者的问题（还没学过前端，又不懂），说selenium库可以渲染js，用了下还是想模拟翻页，然而发现`set_to_iframe`（转换html框架）后还是不行（find到“下一页”的key，但模拟按键`click()`报错“该地方unclickable”）。因此,又放弃selenium模拟翻页思路。
3. **破解params&encSecKey**：随后在chrome端的Neteworks发现XHR有该页歌曲的歌名、ID等所有信息，因此觉得只要爬取这个XHR就行了。然而，之后在百度时发现说网易云api参数param有ASE加密，看一下这个XHR的Headers下部果然有
Form data请求参数params&encSecKey，不过明显看出是加密的动态密码。搜了知乎有人破解过，github上也有人破解。不过想了下感觉好难就放弃了。
4. **专辑ID => 单曲ID => api获取歌词**：最后，还是选择了另一种思路，就是现在的思路，结合了selenium库的`set_to_iframe`。
#### 2）其余
1. 文本分析方面，多google、github、看文档等就行了。有常见的歌词文本分析方向可以搜索。
2. 经典的 utf-8(unicode) => gbk 编码问题（代码里有注释笔记）
3. 其余剩下就是Python编程的一些技巧了。主要耗时在爬虫思路的确定以及实现。