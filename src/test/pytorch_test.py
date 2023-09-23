import glob
import os
import time

import torch
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

from src.config.config import config_instance

# Load the ResNet-50 model
model = models.resnet50(weights=torchvision.models.ResNet50_Weights.DEFAULT)
model.eval()
# print(model)

# Create a transformation pipeline to preprocess the image
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

time_start = time.time()
# Load and preprocess the image
img_path_list = list(glob.glob("F:\\ACG\\壁纸" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in config_instance.get_allow_types()]
for img_path in img_path_list:
    # image_path = "C:\\Users\\xjhqre\Desktop\\2.png"
    image = Image.open(img_path).convert("RGB")
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # Use a CUDA device if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_batch = input_batch.to(device)
    model.to(device)

    # Extract the features
    with torch.no_grad():
        features = model(input_batch)

    # Convert the features to a 1D tensor
    feature_vector = torch.flatten(features, start_dim=1)

    # Print the feature vector
    array = feature_vector.numpy()
    # print(len(array[0]))

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束， 总耗时: {} 秒\n".format(time_sum))
