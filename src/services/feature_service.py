import glob
import os
import time

import torch

from src.config.config import config_instance
from src.utils import sentence_transformer_utils

MODEL_BATCH_SIZE = 64
FEATURE_BATCH_SIZE = 1024
UI_THROTTLE_INTERVAL = 50


# 收集所有图片路径
def collect_image_paths():
    img_path_list = []
    if config_instance.get_contains_sub_directories() == 'Y':
        for root, dirs, files in os.walk(config_instance.get_gallery_path()):
            for file in files:
                img_path_list.append(os.path.join(root, file))
    else:
        img_path_list = list(glob.glob(config_instance.get_gallery_path() + "/*"))
    img_path_list = [name for name in img_path_list if
                     os.path.splitext(name)[1] in config_instance.get_allow_types()]
    return img_path_list


# 执行图片特征提取
def run_extraction(on_progress, on_complete, cancel_event=None):
    time_start = time.time()
    img_path_list = collect_image_paths()
    total_count = len(img_path_list)

    img_emb_list = None
    img_path_list_batch = []
    error_img_list = []
    success_img_list = []
    cnt = 0
    last_ui_update = 0
    cancelled = False

    for i in range(0, total_count, MODEL_BATCH_SIZE):
        if cancel_event and cancel_event.is_set():
            cancelled = True
            break

        batch_paths = img_path_list[i:i + MODEL_BATCH_SIZE]
        valid_paths, batch_embs, batch_error_details = sentence_transformer_utils.extract_batch(batch_paths)

        error_img_list.extend(batch_error_details)
        success_img_list.extend(valid_paths)

        img_path_list_batch.extend(valid_paths)
        if batch_embs is not None:
            if img_emb_list is None:
                img_emb_list = batch_embs
            else:
                img_emb_list = torch.concat((img_emb_list, batch_embs), dim=0)

        cnt += len(batch_paths)

        if len(img_path_list_batch) >= FEATURE_BATCH_SIZE:
            sentence_transformer_utils.dump(img_path_list_batch, img_emb_list)
            img_path_list_batch.clear()
            img_emb_list = None

        if cnt - last_ui_update >= UI_THROTTLE_INTERVAL or cnt >= total_count:
            last_ui_update = cnt
            last_path = batch_paths[-1] if batch_paths else ""
            on_progress(cnt, total_count, last_path)

    if img_path_list_batch:
        sentence_transformer_utils.dump(img_path_list_batch, img_emb_list)
    sentence_transformer_utils.merge_features()

    time_sum = time.time() - time_start
    on_complete(len(success_img_list), len(error_img_list), time_sum, error_img_list, cancelled)