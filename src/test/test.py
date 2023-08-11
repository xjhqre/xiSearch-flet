import glob
import os
import time
import traceback

import torch

from src.test import utils_test


def main():
    time_start = time.time()  # 记录提取开始时间
    error_img = []  # 错误图片列表
    extract_log_text = ""  # 记录日志

    img_path_list = list(glob.glob("F:/ACG/壁纸" + "/*"))
    # 过滤掉非图片类型的文件
    img_path_list = [name for name in img_path_list if
                     os.path.splitext(name)[1] in [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]]

    img_emb_list = None  # 特征向量
    img_path_list_batch = []  # 记录一部分图片路径，和 img_emb_list 一一对应
    cnt = 1  # 记录当前提取的图片索引
    extract_log_text += "开始提取！\n"
    for img_path in img_path_list:
        try:
            img_emb = utils_test.extract(img_path)

            img_path_list_batch.append(img_path)
            if img_emb_list is None:
                img_emb_list = img_emb
            else:
                img_emb_list = torch.concat((img_emb_list, img_emb), dim=0)

            # 每 1024 个维度存储一次
            if cnt % 1024 == 0:
                img_path_list_batch.clear()
                img_emb_list = None

            print("当前提取图片：" + img_path + " --> " + str(cnt))
            cnt += 1
        except Exception as e:
            # 图片打开失败
            traceback.print_exc()
            error_img.append(img_path)
            img_path_list.remove(img_path)

    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start
    extract_log_text += "提取结束，总共耗时：" + str(time_sum) + "秒\n"

    if error_img:
        extract_log_text += "提取失败图片:\n"
        for path in error_img:
            extract_log_text += path + "\n"


main()
