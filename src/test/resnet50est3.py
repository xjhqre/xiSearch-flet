import glob
import os
import time

import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
x = base_model.output
x = Dense(1024, activation='relu')(x)  # 添加一个全连接层，将图片维度映射为1024
model = Model(inputs=base_model.input, outputs=x)

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

batch_size = 32  # 定义批量处理的大小

# 创建一个空的数组用于存储图像数据
batch_images = np.zeros((batch_size, 224, 224, 3))

for i, img_path in enumerate(img_path_list):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    batch_images[i % batch_size] = x  # 将图像添加到批次数组中
    if (i + 1) % batch_size == 0 or i == len(img_path_list) - 1:
        # 当达到批量处理大小时或者是最后一张图像时进行处理
        embeddings = model.predict(batch_images)  # 执行特征提取
        print(embeddings.shape)
        # 处理批次结果...
        # 可在此处保存结果或进行其他操作
        # 处理批次结果...
        for j in range(embeddings.shape[0]):
            img_features = embeddings[j]
            # print(img_features)
            # print("*****")

        # 重置批次数组
        batch_images = np.zeros((batch_size, 224, 224, 3))

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
