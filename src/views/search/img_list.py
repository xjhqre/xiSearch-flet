"""
图片展示列表
"""
from typing import List

from flet_core import UserControl, Row, Image, ImageFit, ImageRepeat, border_radius, Container, Ref, padding, \
    ScrollMode, border, colors, margin

from src.data.config import config_instance


class ImgList(UserControl):

    def __init__(self, ref, page, app_layout):
        super().__init__(ref=ref)
        self.app_layout = app_layout
        self.view = None
        self.expand = True
        self.page = page
        self.img_list_Row = Ref[Row]()

    def build(self):
        # 导航栏容器
        self.view = Container(
            width=950,
            height=500,
            # bgcolor="#FFCC0000",
            margin=margin.only(top=20),
            border=border.all(1, colors.BLACK),
            border_radius=5,
            padding=padding.symmetric(20, 50),
            # padding=padding.only(20, right=20, top=20, bottom=20),
            expand=True,
            content=Row(
                ref=self.img_list_Row,
                wrap=True,
                # auto_scroll=True,  # 自动滑动到底部
                scroll=ScrollMode.AUTO,
                expand=True,
            )
        )
        return self.view

    # 展示图片列表
    def show_result_image(self, similar_img_list):
        if similar_img_list is None or similar_img_list == []:
            return
        # 清空上一次搜索结果
        self.img_list_Row.current.clean()
        # 滚动条移动到最上方
        self.img_list_Row.current.scroll_to(offset=0, duration=500)
        for path in similar_img_list:
            self.img_list_Row.current.controls.append(
                Image(
                    src=path,
                    width=200,
                    height=150,
                    fit=ImageFit.CONTAIN,
                    repeat=ImageRepeat.NO_REPEAT,
                    border_radius=border_radius.all(10),
                )
            )
            self.update()

# def main(page: Page):
#     list = Ref[ImgList]()
#     page.add(ImgList(list, page, None))
#
#
# flet.app(target=main, port=8550)
