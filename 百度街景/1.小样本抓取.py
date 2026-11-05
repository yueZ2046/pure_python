# -*- coding:utf-8 -*-

import urllib.request   #用来获得抓取URL中的内容
import os		        #操作系统接口模块，是对操作系统进行操作，在这里用于文件操作
import socket		    #用于网络消息的传送

outputDir = r"pictures"                            #结果存储位置，相对路径
baidmap_key = "XmKmiBaTNkHlcAprTQBqU90MdKPpkLI9"   #百度地图的key（申请的）
position = [118.919093, 32.106064]				   #输入全景位置点坐标

if os.path.exists(outputDir) is False:             #如果上一步骤中的outputDir（用于存储图片）路径不存在，则建立相应目录。
    os.mkdir(outputDir)

try:
#开始构建url，调用对应的API
#url是形式参数，后面是具体参数
#根据API文档，API分为以下部分，1 域名：api.map.baidu.com。2 服务名：panorama。3 版本号：v2。4 ak，为自己申请的百度地图KEY。5 服务参数
#在本实验中，服务参数包括 1 图片宽度：width。2 图像高度：height。3 全景位置点坐标：location。 4 水平方向范围：fov。使用者可以根据自己的需求构建url请求。

    url = "http://api.map.baidu.com/panorama/v2?ak=" + baidmap_key \
          + "&width=600&height=300&location=" + str(position[0]) + "," + str(position[1]) \
          + "&fov=120"
    socket.setdefaulttimeout(10)  #设置超时时间
    urllib.request.urlretrieve(url, os.path.join(outputDir, "temp_1.bmp"))  #发送url请求，并设置返回路径和返回图像名称。
except Exception as e:
    print(str(e))





