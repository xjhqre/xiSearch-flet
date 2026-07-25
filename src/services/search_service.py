import os
import traceback

from src.config.config import config_instance
from src.exception.no_feature_file_exception import NoFeatureFileException
from src.exception.no_feature_path_exception import NoFeaturePathException
from src.utils import sentence_transformer_utils


class SearchError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# 搜索相似图片
def run_search(query: str) -> list:
    if len(query) == 0:
        raise SearchError("请先选择查询图片")
    if not os.path.exists(query):
        raise SearchError("不存在对应的文件路径")
    try:
        return sentence_transformer_utils.search(query)
    except NoFeaturePathException:
        raise SearchError("请先设置特征文件保存地址")
    except NoFeatureFileException:
        raise SearchError("没有找到特征文件")
    except Exception as e:
        traceback.print_exc()
        raise SearchError("未知错误")