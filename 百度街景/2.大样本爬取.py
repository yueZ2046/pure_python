# -*- coding:utf-8 -*-

import csv                 #用于读取处理csv文件（表格）
import urllib.request      #抓取url中的内容
import os                  #用于文件操作
import socket              #用于网络消息传送

file1 = 'E:/街景识别/Streetview_dot. dbf. csv'    #文件名称，将存有采样点坐标的文件名称存储在file1中
file2 = 'E:/街景识别/key. csv'                    #文件名称，将使用的有多个百度key的文件名称存储在file2中
outrootdir = r"pictures"                         #抓取图片保存文件夹位置
baidmap_key=[]                                   #存储申请的ak值，把csv中的key全部放在里面
i = 1
k = 0                                            #对应列表下标

with open（file2） as csvfile1:                #打开存有key的文件file2，并将文件对象存储在csvfile1中
    csvreader1 = csv.DictReader(csvfile1)     #接收文件对象，并创建一个与文件相关的DictReader对象
    for row in csvreader1:                    #遍历文件中各行
        baimap_key. append(row['key'])        #将文件中的一行数据追加到列表baimap_key尾部

with open(file1) as csvfile:                        #打开file1，并将文件对象存储在csvfile中，创建相应的DictReader对象
    csvreader=csv.DictReader(csvfile)
    for row in csvreader:
        colume1=row['lng']
        colume2=row['lat']
        position = [str(colume1), str(colume2)]     #遍历文件中各行，将经纬度坐标存入变量position中

        if i%1000==0:        #i%1000看余数，看等不等于0，只有1000/2000/3000余数才会为0
            k=k+1
        key=baimap_key       #完成一个key的当日额度，转换为下一个key

        name = str(i) + ". bmp"
        i=i+1                       #更新保存的文件名

        if os.path. exists(outputDir) is False:     #如果文件夹不存在，则创造新的文件夹
            os.mkdir(outputDir)

        try:                                        #获取每个采样点的图片
            url = "http://api.map.baidu.com/panorama/v2?ak=" + key\
            +"&width=600&height=300&location=" + str(position[0]) + "," + str(position[1])\
            +"&fov=120"+"&coordtype=wgs8411"
            print(url)
            socket. setdefaulttimeout(10)
            urllib. request. urlretrieve(url. os.path. join(outputDir.name))

        except Exception as e:
            print(str(e))
           






