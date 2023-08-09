"""
存储视图数据，防止切换视图时数据重置
"""
import configparser
import os

configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
print(configFile)
# 创建配置文件对象
config = configparser.ConfigParser()
# 读取文件
config.read(configFile, encoding='utf-8')

# 项目目录
project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..\\')


def _update_config(option: str, value: str):
    config.read(configFile, encoding='utf-8')
    if not config.has_section("SETTINGS"):
        config.add_section("SETTINGS")
    config.set("SETTINGS", option, value)
    with open(configFile, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


class Config:
    def __init__(self):
        self._file_path: str = ""  # 搜索图片路径
        self._img_path_list: list = []  # 搜索结果图片集合
        self._gallery_path = config.get("SETTINGS", "gallery_path")  # 图片库地址

        self._feature_path = config.get("SETTINGS", "feature_path") \
            if (config.get("SETTINGS", "feature_path") is not None
                and len(config.get("SETTINGS", "feature_path")) != 0) \
            else os.path.join(project_path, 'feature\\')  # 特征向量存储目录，默认为feature目录
        self._allow_types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]  # 允许的图片类型

        self._result_count: int = 30 \
            if (config.get("SETTINGS", "result_count") is None
                or config.get("SETTINGS",
                              "result_count") != "") \
            else int(config.get("SETTINGS", "result_count"))  # 搜索相似图片数量，默认30张

    def get_file_path(self):
        return self._file_path

    def set_file_path(self, value):
        self._file_path = value

    def get_img_path_list(self):
        return self._img_path_list

    def set_img_path_list(self, img_path_list):
        self._img_path_list = img_path_list

    def get_gallery_path(self):
        return self._gallery_path

    def set_gallery_path(self, gallery_path):
        self._gallery_path = gallery_path
        # 修改配置文件
        _update_config("gallery_path", gallery_path)

    def get_feature_path(self):
        return self._feature_path

    def set_feature_path(self, feature_path):
        self._feature_path = feature_path
        # 修改配置文件
        _update_config("feature_path", self._feature_path)

    def get_allow_types(self):
        return self._allow_types

    def get_result_count(self):
        return self._result_count

    def set_result_count(self, value):
        self._result_count = value
        _update_config("result_count", str(self._result_count))


config_instance = Config()
