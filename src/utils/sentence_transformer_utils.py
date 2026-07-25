import gc
import glob
import os
import time

import torch
import torch.nn.functional as F
from PIL import Image
from sentence_transformers import SentenceTransformer, util

from src.config import config
from src.config.config import config_instance
from src.constants.layout_constant import MAX_RESULT_COUNT
from src.exception.no_feature_file_exception import NoFeatureFileException
from src.exception.no_feature_path_exception import NoFeaturePathException

# 限制为物理核心数的一半或固定值
cpu_count = os.cpu_count()
torch.set_num_threads(max(4, min(cpu_count // 2, 8)))

try:
    import faiss
    _FAISS_AVAILABLE = True
except ImportError:
    _FAISS_AVAILABLE = False

_model_name_or_path = ""
if os.path.exists(config.model_path):
    _model_name_or_path = config.model_path
else:
    _model_name_or_path = "clip-ViT-B-32"

_model = None


class ModelLoadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


_FEATURE_FILE = "features.pt"
_FAISS_INDEX_FILE = "faiss.index"

_feature_cache = {
    "img_names": [],
    "img_emb": None,
    "index": None, # FAISS 索引（懒构建）
    "file_mtime": 0, # 文件修改时间， 初始为 0，表示"缓存未命中"
}


def _get_model():
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer(_model_name_or_path)
        except Exception as e:
            raise ModelLoadError(
                "模型加载失败: {}\n请检查模型文件是否完整，或网络连接是否正常。".format(str(e))
            )
    return _model


def _get_feature_file_path():
    return os.path.join(config_instance.get_feature_path(), _FEATURE_FILE)


def _get_faiss_index_path():
    return os.path.join(config_instance.get_feature_path(), _FAISS_INDEX_FILE)

# 存储张量
def dump(img_names, img_emb):
    if not os.path.exists(config_instance.get_feature_path()):
        os.makedirs(config_instance.get_feature_path())
    with open(config_instance.get_feature_path() + str(int(time.time())) + ".pt", 'wb') as fOut:
        torch.save({"img_names": img_names, "img_emb": img_emb}, fOut)


def merge_features():
    feature_dir = config_instance.get_feature_path()
    batch_files = sorted(glob.glob(os.path.join(feature_dir, "*.pt")))
    batch_files = [f for f in batch_files if os.path.basename(f) != _FEATURE_FILE]
    if not batch_files:
        return
    all_names = []
    all_emb = None
    for f in batch_files:
        data = torch.load(f)
        all_names.extend(data["img_names"])
        if all_emb is None:
            all_emb = data["img_emb"]
        else:
            all_emb = torch.concat((all_emb, data["img_emb"]), dim=0)
    merged_path = _get_feature_file_path()
    torch.save({"img_names": all_names, "img_emb": all_emb}, merged_path)
    for f in batch_files:
        os.remove(f)
    _feature_cache["file_mtime"] = 0
    if _FAISS_AVAILABLE and all_emb is not None:
        _save_faiss_index(all_emb)


# 提取特征方法
def extract(img_path):
    img = Image.open(img_path)
    emb = _get_model().encode([img], batch_size=1, convert_to_tensor=True, show_progress_bar=False)
    img.close()
    return emb


def extract_batch(img_paths):
    images = []
    valid_paths = []
    error_details = []
    for path in img_paths:
        try:
            img = Image.open(path)
            images.append(img)
            valid_paths.append(path)
        except Exception as e:
            error_details.append((path, str(e)))
    if not images:
        return [], None, error_details
    embs = _get_model().encode(images, batch_size=len(images), convert_to_tensor=True, show_progress_bar=False)
    for img in images:
        img.close()
    return valid_paths, embs, error_details


# 加载特征
def _load_features(load_emb=True):
    merged_path = _get_feature_file_path()
    if os.path.exists(merged_path):
        file_mtime = os.path.getmtime(merged_path) # 读取 features.pt 的最后修改时间
        if _feature_cache["file_mtime"] == file_mtime:
            if load_emb and _feature_cache["img_emb"] is not None:
                return
            if not load_emb and _feature_cache["img_names"]:
                return
        try:
            data = torch.load(merged_path)
        except Exception as e:
            raise NoFeatureFileException(
                "特征文件损坏，无法加载: {}\n请重新提取特征。".format(str(e))
            )
        _feature_cache["img_names"] = data["img_names"]
        if load_emb:
            _feature_cache["img_emb"] = data["img_emb"]
        else:
            _feature_cache["img_emb"] = None
            del data
            gc.collect()
        _feature_cache["file_mtime"] = file_mtime
        _feature_cache["index"] = None
        return
    else:
        raise NoFeatureFileException("没有找到特征文件，请先提取特征。")


def _save_faiss_index(emb):
    index_path = _get_faiss_index_path()
    emb = F.normalize(emb, p=2, dim=1)
    emb_np = emb.cpu().numpy().astype("float32")
    d = emb_np.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(emb_np)
    faiss.write_index(index, index_path)
    _feature_cache["index"] = index


def _get_faiss_index():
    if _feature_cache["index"] is not None:
        return _feature_cache["index"]
    index_path = _get_faiss_index_path()
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        _feature_cache["index"] = index
        return index
    emb = _feature_cache["img_emb"]
    if emb is None:
        _load_features(load_emb=True)
        emb = _feature_cache["img_emb"]
    if emb is None:
        return None
    _save_faiss_index(emb)
    return _feature_cache["index"]


def search(query, k=None):
    if k is None:
        k = int(config_instance.get_result_count())
    k = min(k, MAX_RESULT_COUNT)
    if not os.path.exists(config_instance.get_feature_path()):
        raise NoFeaturePathException

    _load_features()

    img = Image.open(query)
    query_emb = _get_model().encode([img], batch_size=1, convert_to_tensor=True, show_progress_bar=False)
    img.close()

    if _FAISS_AVAILABLE:
        _load_features(load_emb=False)
        index = _get_faiss_index()
        query_emb = F.normalize(query_emb, p=2, dim=1)
        query_np = query_emb.cpu().numpy().astype("float32")
        _, indices = index.search(query_np, k)
        return [_feature_cache["img_names"][i] for i in indices[0]]
    else:
        _load_features(load_emb=True)
        hits = util.semantic_search(query_emb, _feature_cache["img_emb"], top_k=k)[0]
        return [_feature_cache["img_names"][hit["corpus_id"]] for hit in hits]
