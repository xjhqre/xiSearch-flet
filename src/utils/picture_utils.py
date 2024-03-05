import base64
import imghdr
import os

from PIL import Image

from src.config import config


def get_image_mime_type(file_path):
    return imghdr.what(file_path)


def generateBase64(img_path_list):
    base64_list = []
    for img_path in img_path_list:
        mime_type = get_image_mime_type(img_path)
        if mime_type == None:
            mime_type = "jpeg"
        # 打开图片文件
        with Image.open(img_path) as im:
            # 获取文件名
            file_name = os.path.basename(img_path)
            # 生成缩略图
            im.thumbnail((400, 400))

            # 保存缩略图
            im.save(config.project_path + 'img/' + file_name)

        with open(config.project_path + 'img/' + file_name, 'rb') as f:
            base64_data = "data:image/" + mime_type + ";base64," + base64.b64encode(f.read()).decode('utf-8')

        # 使用完后删除缩略图
        os.remove(config.project_path + 'img/' + file_name)

        # 打印Base64编码
        base64_list.append(base64_data)

    return base64_list


if __name__ == '__main__':
    list = ['F:\\ACG\\壁纸\\786785272_wps图片.jpg', 'F:\\ACG\\壁纸\\79fc99acaeb2757dab5a0f37e2510930b02844eb.jpg',
            'F:\\ACG\\壁纸\\wallhaven-6k1mo7.png', 'F:\\ACG\\壁纸\\IMG_2842_wps图片.jpeg',
            'F:\\ACG\\壁纸\\wallhaven-x88o53.jpg', 'F:\\ACG\\壁纸\\wallhaven-4vk37m.png',
            'F:\\ACG\\壁纸\\wallhaven-k9xzlq.jpg', 'F:\\ACG\\壁纸\\wallhaven-yje8ol.png',
            'F:\\ACG\\壁纸\\wallhaven-43g8e3.png', 'F:\\ACG\\壁纸\\wallhaven-ey75mw.png',
            'F:\\ACG\\壁纸\\28582b0c63675b4297c0f1c4c324964c-2.jpg', 'F:\\ACG\\壁纸\\63-1Z6261433432Y.jpg',
            'F:\\ACG\\壁纸\\wallhaven-7291j9.png', 'F:\\ACG\\壁纸\\wallhaven-73wyze.jpg',
            'F:\\ACG\\壁纸\\QQ图片20200121184324.jpg', 'F:\\ACG\\壁纸\\QQ图片20200202130318.jpg',
            'F:\\ACG\\壁纸\\yande.re 539058 feet g_scream heterochromia hololive kagura_mea loli pantsu project_paryi wallpaper.jpg',
            'F:\\ACG\\壁纸\\QQ图片20200201132607.png', 'F:\\ACG\\壁纸\\wallhaven-r7kyv7.jpg',
            'F:\\ACG\\壁纸\\wallhaven-ox8k65.png', 'F:\\ACG\\壁纸\\005z6tdJjw1ezz6phl8q9j31hc0u0jt7-1.jpg',
            'F:\\ACG\\壁纸\\wallhaven-6k382w.jpg', 'F:\\ACG\\壁纸\\wallhaven-g8zgx3 (1).png',
            'F:\\ACG\\壁纸\\wallhaven-5w7og3.png', 'F:\\ACG\\壁纸\\7686786_wps图片.png',
            'F:\\ACG\\壁纸\\wallhaven-xl7ykd.jpg', 'F:\\ACG\\壁纸\\wallhaven-vgdy35.png',
            'F:\\ACG\\壁纸\\wallhaven-2k6ve6.jpg', 'F:\\ACG\\壁纸\\wallhaven-0jqyjp.jpg',
            'F:\\ACG\\壁纸\\ͼƬ8_wps图片.jpeg']
    generateBase64(list)
