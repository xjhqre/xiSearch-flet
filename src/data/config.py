"""
存储视图数据，防止切换视图时数据重置
"""
import configparser
import os

configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
# 创建配置文件对象
config = configparser.ConfigParser()
# 读取文件
config.read(configFile, encoding='utf-8')

# 项目目录
project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..\\')


class Config:
    def __init__(self):
        self._file_path = ""  # 搜索图片路径
        self._img_path_list = []  # 搜索结果图片集合
        self._gallery_path = config.get("SETTINGS", "gallery_path")  # 图片库地址
        self._feature_path = config.get("SETTINGS", "feature_path") \
            if config.get("SETTINGS", "feature_path") \
            else os.path.join(project_path, 'feature\\')  # 特征向量存储目录，默认为feature目录
        self._allow_types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]  # 允许的图片类型
        self._batch_size = int(config.get("SETTINGS", "batch_size"))  # batch大小

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
        config.read(configFile, encoding='utf-8')
        if not config.has_section("SETTINGS"):
            config.add_section("SETTINGS")
        config.set("SETTINGS", "gallery_path", gallery_path)

    def get_feature_path(self):
        return self._feature_path

    def set_feature_path(self, feature_path):
        self._feature_path = feature_path
        # 修改配置文件
        config.read(configFile, encoding='utf-8')
        if not config.has_section("SETTINGS"):
            config.add_section("SETTINGS")
        config.set("SETTINGS", "feature_path", feature_path)

    def get_allow_types(self):
        return self._allow_types


config_instance = Config()
