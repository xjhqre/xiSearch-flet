import glob
import os
import time

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from torchvision.models import ResNet50_Weights

# 提取结束，提取成功图片: 165 张 总耗时: 26.309924364089966 秒
# 加载预训练的ResNet-50模型
resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
# 设置模型为评估（推理）模式
resnet.eval()

# 图像预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    input_tensor = preprocess(Image.open(img_path).convert("RGB"))
    input_batch = input_tensor.unsqueeze(0)
    # 使用ResNet-50进行图像嵌入
    with torch.no_grad():
        embeddings = resnet(input_batch)

    print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
    cnt += 1

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
