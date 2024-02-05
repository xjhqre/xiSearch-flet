import glob
import os
import time

from src.utils import sentence_transformer_utils

# 提取结束，提取成功图片: 165 张 总耗时: 26.309924364089966 秒

img_path_list = list(glob.glob("F:\\ACG\\新建文件夹" + "/*"))
# 过滤掉非图片类型的文件
img_path_list = [name for name in img_path_list if
                 os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

totle_image_count = len(img_path_list)

cnt = 1  # 记录当前提取的图片索引
time_start = time.time()  # 记录结束时间

for img_path in img_path_list:
    try:
        img_emb = sentence_transformer_utils.extract(img_path)

        print("当前提取图片：" + img_path + " --> " + str(cnt) + "\n")
        cnt += 1
    except Exception as e:
        # 图片打开失败
        # traceback.print_exc()
        img_path_list.remove(img_path)

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start
print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
    len(img_path_list), time_sum))
