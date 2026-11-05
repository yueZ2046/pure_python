# -*- coding:utf-8 -*-

import os
import csv
from PIL import Image
import numpy as np

in_rootdir = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures-fenge"       # 街景分割结果保存文件夹
out_file = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures-tongji.csv"     # 汇总统计结果保存路径

# 初始值为0，记录当前处理图像数量
count = 0

# 创建csv文件
writer = csv.writer(open(out_file, "w", newline=""), dialect=("excel"))

# 创建表头
writer.writerow(["pid", "road", "sidewalk", "building", "wall", "fence",
                 "pole", "traffic_light", "traffic_sign", "vegetation", "terrain",
                 "sky", "person", "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle"])

for file in os.listdir(in_rootdir):
	# 获取分割后图像
    img = Image.open(os.path.join(in_rootdir, file))     
	# 记录当前处理的图像数量
    count += 1
    # 初始化每个灰度值的像素数量为0
    count_dic = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, -1: 0, 255: 0}
    # 将图像转为矩阵，对灰度值进行统计
    ar = np.array(img).flatten().tolist()
	# 计算灰度值在0-18之间的像素数量，并存储到字典中
    for item in count_dic:
        count_dic[item] = ar.count(item)
    # 获得图像中的像素数量
    sumcount = len(ar)
	# 计算每个灰度的百分比，并写入CSV中
    writer.writerow([file.split(".")[0], count_dic[0]*1.0/sumcount, count_dic[1]*1.0/sumcount, count_dic[2]*1.0/sumcount,
                     count_dic[3]*1.0/sumcount, count_dic[4] * 1.0 / sumcount, count_dic[5]*1.0/sumcount,
                     count_dic[6]*1.0/sumcount, count_dic[7]*1.0/sumcount, count_dic[8] * 1.0 / sumcount,
                     count_dic[9]*1.0/sumcount, count_dic[10]*1.0/sumcount, count_dic[11]*1.0/sumcount,
                     count_dic[12]*1.0/sumcount, count_dic[13] * 1.0 / sumcount, count_dic[14]*1.0/sumcount,
                     count_dic[15]*1.0/sumcount, count_dic[16]*1.0/sumcount, count_dic[17]*1.0/sumcount,
                     count_dic[18]*1.0/sumcount])
	# 在输出窗口提示统计图像文件名称和当前处理图像数量
    print(file, count)


