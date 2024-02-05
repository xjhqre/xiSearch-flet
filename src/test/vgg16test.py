import glob
import os
import time

import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image

# 加载VGG16模型，去掉顶部的全连接层
model = VGG16(weights='imagenet', include_top=False)

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    img = image.load_img(img_path, target_size=(224, 224))  # 调整图像大小
    x = image.img_to_array(img)  # 图像转换为numpy数组
    x = np.expand_dims(x, axis=0)  # 扩展维度以匹配模型输入
    x = preprocess_input(x)  # 预处理图像，使其与VGG模型的预处理一致
    # 获取图像嵌入
    embeddings = model.predict(x)
    print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
    cnt += 1

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
