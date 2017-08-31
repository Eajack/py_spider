# -*- coding : utf-8 -*-
#!/usr/bin/env python3
# ===============================================================================
# Author: Eajack
# date:2017/8/27 - 2017/8/31
# ===============================================================================
# Function：歌词文本分析
#   1- jieba分词，去单字
#   2- 根据词频生成词云
#   3- 词频统计，做柱形图 & 饼状图
#   4- 歌词情绪分析简易版demo (饼状图 & 曲线图)
# ===============================================================================
# keyPoints:
#   1- 多百度，google & github
# ===============================================================================

import jieba
import os
from wordcloud import WordCloud,ImageColorGenerator
from scipy.misc import imread
from os import path
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from snownlp import SnowNLP

# 遍历读取歌词文件，jieba分词
def jieba_split():
    '''
    遍历读取歌词文件，jieba分词
    :return: 
    '''
    global wordList
    ## 文件目录
    lyricsPath = r'D:\STUDYING\MyProjects\pycharm\music163_EasonLyrics\Lyrics'
    os.chdir(lyricsPath)
    lyricstxtList = [txtfile for txtfile in os.listdir('.')]
    ## print(lyricstxtList)

    for fileName in lyricstxtList:
        txtFile = open(fileName,'r',encoding='utf-8')
        for line in txtFile:
            flag = ("作曲" in line) or ("作词" in line) or ("编曲" in line)
            if (flag):
                continue
            else:
                ## 判断是否为英文
                lineBuffer = line.replace(" ","")
                if lineBuffer.isalpha():
                    ## 英文直接按照空格分词
                    Engseg_list = line.split()
                    for seg in Engseg_list:
                        wordList.append(seg)

                Chiseg_list = jieba.cut(line)
                for seg in Chiseg_list:
                    ## 判断是否为中文
                    if (u'\u4e00' <= seg <= u'\u9fff'):
                        ### 去单字
                        code = str(seg.encode('UTF-8'))
                        isOnehanzi = ( code.count("\\x") == 3 )
                        if isOnehanzi:
                            continue
                    ## 判断是否为英文
                    isEngwords = (seg.isalpha())

                    ## 1-中文非单字 & 2- 英文单词
                    if ( not isOnehanzi and isEngwords ):
                        wordList.append(seg)
        txtFile.close()

# 绘制词云图
def draw_wordCloud():
    '''
    画出词云图
    :return: 
    '''
    ## 读取wordList，转化为str
    global wordList
    cut_text = ""
    for word in wordList:
        cut_text = cut_text + word + " "

    ## 生成词云
    os.chdir(r"D:\STUDYING\MyProjects\pycharm\music163_EasonLyrics")
    d = path.dirname(__file__)  # 当前文件文件夹所在目录
    color_mask = imread("Eason.jpg")  # 读取背景图片
    plt.imshow(color_mask)

    cloud = WordCloud(
        font_path=path.join(d, 'simsun.ttc'),
        background_color='white',
        mask=color_mask,
        max_words=2000,
        max_font_size=40,
    )
    word_cloud = cloud.generate(cut_text)  # 产生词云

    ## show
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

# 统计词频，画柱形图、饼状图
def caculateWordFrequency():
    '''
    统计词频，画柱形图、饼状图
    :return: 
    '''
    global wordList,wordFrequency
    ## 统计词频，储存在wordFrequency dict里面
    for word in wordList:
        if word in wordFrequency.keys():
            wordFrequency[word] += 1
        else:
            wordFrequency[word] = 1
    ## 按value值排序
    items = wordFrequency.items()
    sortedItems = [ [item[1],item[0]] for item in items ]
    sortedItems.sort()  ## 顺序
    sortedItems.reverse()      ## 降序

    ## 取前30个，画柱形图
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)    ##字体设置
    X_labels = [ sortedItems[i][1] for i in range(0,30) ]
    Y = [ sortedItems[i][0] for i in range(0,30) ]
    X = range(len(X_labels))
    fig = plt.figure()
    plt.bar(X, Y, color="green")
    plt.xticks(X, X_labels,fontproperties=font)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("TOP 30th words")
    plt.show()

    ## 取前30个，画饼状图
    labels = [ sortedItems[i][1] for i in range(0,len(sortedItems)) ]
    ### 求比例
    totalNum = 0
    rates = []
    for sortedItem in sortedItems:
        totalNum += sortedItem[0]
    for i in range(0,len(sortedItems)):
        rate = sortedItems[i][0] / totalNum * 100
        rate = round(rate,10)
        rates.append(rate)
    ### 取前30个词语
    labels = labels[0:30]
    rates = rates[0:30]
    ### 作图
    explode = [0] * 30
    explode[0] = explode[1] = 0.1   ## 突出第一、二个
    fig = plt.figure()
    plt.axes(aspect=1)
    patches,l_text,p_text = plt.pie(
        x=rates,
        labels=labels,
        explode=explode,
        autopct='%3.1f %%',
        shadow=True,
        labeldistance=1.1,
        startangle=90,
        pctdistance=0.8
    )
    ### 中文显示问题
    for font in l_text:
        font.set_fontproperties(FontProperties(fname=r"c:\windows\fonts\simsun.ttc"))
    plt.show()

# 歌词情绪分析
def motionAnalyze():
    '''
    思路：
        1- 遍历读取所有歌词文本，储存每一首歌歌词文档为lyricsList
        2- 利用 SnowNLP给当前文档评分
        3- 统计所有文档评分dict形式储存
        4- 可视化
    :return: 
    '''
    motionGrade = {}
    ## 文件目录
    lyricsPath = r'D:\STUDYING\MyProjects\pycharm\music163_EasonLyrics\Lyrics'
    os.chdir(lyricsPath)
    lyricstxtList = [txtfile for txtfile in os.listdir('.')]

    for fileName in lyricstxtList:
        ## 读取本文档，储存在currentLyrics字符串
        txtFile = open(fileName, 'r', encoding='utf-8')
        currentLyrics = ""
        for line in txtFile:
            currentLyrics = currentLyrics + line

        ## SnowNLP使用
        ### 先对每个歌词文本分句，评价每句的情感值，求平均
        currentLyrics = currentLyrics.replace("\n", "。")
        currentLyrics = currentLyrics.replace(" ", "")
        text = SnowNLP(currentLyrics)
        grade = 0;
        ### 获得所有句子评分总和以及平均值
        for sentence in text.sentences:
            sentenceSNOW = SnowNLP(sentence)
            grade += sentenceSNOW.sentiments
        grade = grade / len(text.sentences)     ### 求均值

        ## 储存情感值
        fileName = fileName.replace(".txt","")
        motionGrade[fileName] = round(grade,5)
        print(fileName,"已经读取完")

    ## 情感分布饼状图
    ### 定义 grade >= 0.6 属于正面情绪，<= 0.6为负面情绪
    positiveNum = 0
    negativeNum = 0
    totalNum = 0
    for grade in motionGrade.values():
        if (grade >= 0.6):
            positiveNum += 1
        else:
            negativeNum += 1
        totalNum += 1
    print(positiveNum,negativeNum,totalNum)
    ### 画饼状图
    rates = [ round( ((float)(positiveNum / totalNum)),2 ),
              round(((float)(negativeNum / totalNum)), 2)]
    labels = [u"正面情绪",u"负面情绪"]
    explode = [0] * 2
    fig = plt.figure()
    plt.axes(aspect=1)
    patches, l_text, p_text = plt.pie(
        x=rates,
        labels=labels,
        explode=explode,
        autopct='%3.1f %%',
        labeldistance=1.1,
        startangle=90,
        pctdistance=0.8
    )
    ### 中文显示问题
    for font in l_text:
        font.set_fontproperties(FontProperties(fname=r"c:\windows\fonts\simsun.ttc"))
    plt.show()

    ## 情感分布折线图
    ## X-得分区间  Y- 该区间歌曲个数
    ### 确定区间，统计区间歌曲数量
    X = range(1,11,1)     ### 1 => 0~0.1区间，2 => 0.1~0.2区间 ……
    Y = [0] * 10
    for grade in motionGrade.values():
        ### 暴力简单分区……
        if ( 0 <= grade < 0.1 ):
            Y[0] += 1
        elif ( 0.1 <= grade < 0.2 ):
            Y[1] += 1
        elif ( 0.2 <= grade < 0.3 ):
            Y[2] += 1
        elif ( 0.3 <= grade < 0.4 ):
            Y[3] += 1
        elif ( 0.4 <= grade < 0.5 ):
            Y[4] += 1
        elif ( 0.5 <= grade < 0.6 ):
            Y[5] += 1
        elif ( 0.6 <= grade < 0.7 ):
            Y[6] += 1
        elif ( 0.7 <= grade < 0.8 ):
            Y[7] += 1
        elif ( 0.8 <= grade < 0.9 ):
            Y[8] += 1
        elif ( 0.9 <= grade < 1.0 ):
            Y[9] += 1

    ### 画折线图
    fonts = {'fontname': 'SimHei', 'size': '20'}
    fig1 = plt.figure()
    plt.plot(X, Y,\
             linewidth=3,\
             color='r',\
             marker='o',\
             markerfacecolor='blue',\
             markersize=5\
    )
    plt.axis([0,11,0,250])
    plt.title(u'情感指数曲线',**fonts)
    plt.xlabel(u'情感指数区间',**fonts)
    plt.ylabel(u'歌曲数量',**fonts)
    plt.text(1, 100, "PS:横坐标中，1 => 0.1-0.2区间，2 => 0.2-0.3区间etc.。", \
                size=15, alpha=1.0,family='SimHei')
    plt.grid(X)
    plt.show()

if __name__ == "__main__":
    # global
    ## 所有分词list
    wordList = []
    ## 词频dict,wordFrequency[word] = num
    wordFrequency = {}

    # game start
    jieba_split()
    draw_wordCloud()
    caculateWordFrequency()
    motionAnalyze()