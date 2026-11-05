#!--*-- coding:utf-8 --*--

import os
import tarfile
import numpy as np
from PIL import Image
import tensorflow as tf
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"            # 设置日志显示等级，仅显示warn和error

class DeepLabModel(object):                         # 加载DeepLab模型
	INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):               # 输入模型路径，初始化模型设置
        self.graph = tf.Graph()
        graph_def = None
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.compat.v1.Session(graph=self.graph)

    def run(self, image):                     # 输入原始图像，返回语义分割结果，格式为数组
        batch_seg_map = self.sess.run(self.OUTPUT_TENSOR_NAME,
                                      feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(image)]})
        seg_map = batch_seg_map[0]
        return seg_map

if __name__ == '__main__':
    # 定义文件路径
    in_dir = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures"          # 街景照片原始数据存储文件夹
    out_dir = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures-fenge"        # 街景语义分割结果数据保存文件夹
    model_file = r"D:\miniconda\models\deeplabv3_mnv2_cityscapes_train_2018_02_05.tar.gz"   #小模型存储路径
    # model_file = r"D:\miniconda\models\deeplabv3_cityscapes_train_2018_02_06.tar.gz"  # 大模型存储路径

    start_time = int(time.time())       # 程序运行开始时间
    MODEL = DeepLabModel(model_file)    # 初始化模型

    for img_file in os.listdir(in_dir):         # 遍历输入文件夹中的所有图像，并进行语义分割
        try:
            st_seg = int(time.time())           # 语义分割开始运行时间
            original_img = Image.open(os.path.join(in_dir, img_file))               # 以Image的格式打开原始图像
            seg_map = MODEL.run(original_img)                                       # 对原始图像进行语义分割
			new_im = Image.fromarray(seg_map.astype('uint8'))                       # 将语义分割结果数组转换为Image
			new_im.save(os.path.join(out_dir, img_file))                            # 保存结果Image
			print("{} spend time {}s".format(img_file, int(time.time()) - st_seg))  # 输出图像文件名，和运行用时
        except:
			 print("{} FAIL!".format(img_file))                    # 如果运行出错输出文件名
	print('spend time %ds' % (int(time.time()) - start_time))      # 统计全部用时