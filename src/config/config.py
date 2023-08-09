import configparser
import os

configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/config.ini')
# 创建配置文件对象
config = configparser.ConfigParser()
# 读取文件
config.read(configFile, encoding='utf-8')

# 图片库地址
gallery_path = config.get("SETTINGS", "gallery_path")

# 特征向量地址
feature_path = config.get("SETTINGS", "feature_path")
# feature_path = os.path.dirname(os.getcwd()) + "\\feature\\"
# if not os.path.exists(feature_path):  # 判断文件夹是否存在
#     os.mkdir(feature_path)  # 创建文件夹

# 搜索的图片地址
search_img_path = ""

# 允许的图片类型
allow_types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]

# batch大小
batch_size = int(config.get("SETTINGS", "batch_size"))


def set_gallery_path(value):
    config.read(configFile, encoding='utf-8')
    if not config.has_section("SETTINGS"):
        config.add_section("SETTINGS")
    config.set("SETTINGS", "gallery_path", value)
