import glob
import os
import time

from PIL import Image
from torchvision.transforms import ToTensor, Resize
from transformers import ViTFeatureExtractor, ViTModel

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
model = ViTModel.from_pretrained('google/vit-base-patch16-224')

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    image = Image.open(img_path)
    # 将图像转换为 RGB 格式
    image = image.convert("RGB")
    # 对图像进行转换以将其转换为三维张量
    image = Resize((224, 224))(image)
    image = ToTensor()(image)

    inputs = feature_extractor(images=image.unsqueeze(0), return_tensors="pt")
    # 提取图像特征
    outputs = model(**inputs)
    features = outputs.last_hidden_state.squeeze(0)

    print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
    cnt += 1

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
