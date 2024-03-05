import base64
import glob
import imghdr
import os

from PIL import Image

from src.config.config import config_instance


def get_image_mime_type(file_path):
    return imghdr.what(file_path)


def generateBase64(img_folder_path):
    base64_list = []
    img_path_list = glob.glob(os.path.join(img_folder_path, "*"))
    # 过滤掉非图片类型的文件
    img_path_list = [name for name in img_path_list if
                     os.path.splitext(name)[1] in config_instance.get_allow_types()]

    for i, img_path in enumerate(img_path_list):
        mime_type = get_image_mime_type(img_path)
        # 打开图片文件
        with Image.open(img_path) as im:
            # 获取文件名
            file_name = os.path.basename(img_path)
            # 生成缩略图
            im.thumbnail((400, 400))

            # 保存缩略图
            im.save("../../img/" + file_name)

        with open("../../img/" + file_name, 'rb') as f:
            base64_data = "data:image/" + mime_type + ";base64," + base64.b64encode(f.read()).decode('utf-8')

        # 使用完后删除缩略图
        os.remove("../../img/" + file_name)

        # 打印Base64编码
        print(base64_data)


if __name__ == '__main__':
    generateBase64(r"C:\Users\xjhqre\Desktop\新建文件夹")
