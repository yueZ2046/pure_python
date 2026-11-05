#!--*-- coding:utf-8 --*--

# Deeplab Demo

import os                    #文件操作
import tarfile               #读取写入tar文档/tar压缩包/训练集模型文件的读取
import numpy as np           #numpy处理数组的库（线性代数库）
from PIL import Image        #Python Image Library是py第三方图像处理库/目的为了后面图像灰度调整
import tensorflow as tf
import time                  #统计时间

os.environ["TF_CPP_MIN_LOG_LEVEL"] ="2"         # 设置日志显示等级，仅显示warn和error

#模型加载运行
class DeepLabModel(object):         # 加载DeepLab模型

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

#模型初始化
    def __init__(self, tarball_path):            # 输入模型路径，初始化模型设置
        self.graph = tf.Graph()
        graph_def = None
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.compat.v1.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.compat.v1.Session(graph=self.graph)

#模型运行
    def run(self, image):          # 输入原始图像，返回语义分割结果，格式为数组

        batch_seg_map = self.sess.run(self.OUTPUT_TENSOR_NAME,
                                      feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(image)]})
        seg_map = batch_seg_map[0]
        return seg_map

#开始主函数
if __name__ == '__main__':        #主函数的固定用法
    in_dir = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures"   #街景照片原始数据存储位置
    out_dir = r"E:\g. FOR LILIN\2020.8.31\py-daima\daima-lesson\pictures-fenge"    #街景语义分割结果数据保存位置
    model_file = r"D:\anaconda\models\deeplabv3_mnv2_cityscapes_train_2018_02_05.tar.gz"   #小模型，已训练完成模型位置
    #model_file = r"D:\anaconda\models\deeplabv3_cityscapes_train_2018_02_06.tar.gz"  # 大模型，已训练完成模型位置

    t=int(time.time())
    MODEL = DeepLabModel(model_file)
    for imgfile in os.listdir(in_dir):
        try:
            st=int(time.time())
            orignal_im = Image.open(os.path.join(in_dir,imgfile))
            seg_map = MODEL.run(orignal_im)
            new_im = Image.fromarray(seg_map.astype('uint8'))
            new_im.save(os.path.join(out_dir,imgfile))
            print(imgfile,"spend time",int(time.time())-st,"s")
        except:
            print(imgfile)
    print(int(time.time())-t)
    #一定要注意缩进要严格符合python的语法规则，否则一个字符的位置错误就会导致程序无法跑出