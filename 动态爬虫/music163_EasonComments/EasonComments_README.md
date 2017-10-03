## music163_EasonComments项目

### 1-[getSongsName_ID.py]()
获取Eason网易云单曲对应ID，代码重用于[EasonLyrics.py](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/EasonLyrics.py)

### 2-[getComments.py]()
获取对应ID单曲的评论数、热门评论文本数据以及最新10条评论文本数据

### 3-[commentAnalysis.py]()
代码重用于[wordsAnalysis.py](https://github.com/Eajack/py_spider/blob/master/%E5%8A%A8%E6%80%81%E7%88%AC%E8%99%AB/music163_EasonLyrics/wordsAnalysis.py)

>* 只分析热门评论 hotComments.xls，纯文字（Eng & Chi）分析，不包括emoji表情、颜文字、标点符号
>* jieba分词统计词汇（去单字）
>* 根据词频生成词云
>* 词频统计，做柱形图 & 饼状图
>* 歌词情绪分析简易版demo (饼状图 & 曲线图)

### 4-[resultXLS]()
获取爬虫数据储存的excel文件（updated on 2017.10.2）

>* [hotComments.xls]()：Eason所有歌曲的热门评论文本数据，共5451条评论，5451行
>* [Newcomments.xls]()：Eason所有歌曲最新10条评论，共8492条评论，8492行
>* [songName2commentsNum.xls]()：Eason所有歌曲以及对应的网易云单曲ID
>* [songName2commentsNum.xls]()：Eason所有歌曲对应的评论数

### 5-[resultsPNGs]():所有分析结果图片汇总

### 6-[Eason.jpg]():Eason图片词云背景图