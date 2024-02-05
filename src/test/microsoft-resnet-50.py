import glob
import os
import time

import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageClassification, AutoFeatureExtractor

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

model_name = "microsoft/resnet-50"
model = AutoModelForImageClassification.from_pretrained(model_name)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)

# 预处理图像
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    image = Image.open(img_path).resize((224, 224)).convert('RGB')
    # image = transform(image).unsqueeze(0)
    # 图片预处理
    inputs = feature_extractor(images=image, return_tensors="pt")

    # 提取特征
    with torch.no_grad():
        outputs = model(**inputs)

    # 获取特征向量
    features = outputs.logits  # 你可能需要根据你的需求调整这一行

    print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
    cnt += 1

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
