import glob
import os
import time

import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 提取结束，提取成功图片: 165 张 总耗时: 26.309924364089966 秒

model = CLIPModel.from_pretrained("G:\\临时\\model")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    inputs = processor(text=None, images=Image.open(img_path), return_tensors="pt", padding=True)
    # 嵌入图像
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    print(np.array(image_features).flatten().size)
    print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
    cnt += 1

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
