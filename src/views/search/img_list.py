"""
图片展示列表
"""
from typing import List

from flet_core import UserControl, Row, Image, ImageFit, ImageRepeat, border_radius, Container, Ref, padding, \
    ScrollMode, border, colors, margin


class ImgList(UserControl):

    def __init__(self, ref, page, app_layout):
        super().__init__(ref)
        self.app_layout = app_layout
        self.view = None
        self.expand = True
        self.page = page
        self.img_list_container = Ref[Container]()

    def build(self):
        # 导航栏容器
        self.view = Container(
            width=950,
            height=500,
            # bgcolor="#FFCC0000",
            margin=margin.only(top=20),
            border=border.all(1, colors.BLACK),
            border_radius=5,
            ref=self.img_list_container,
            padding=padding.symmetric(20, 8),
            # padding=padding.only(20, right=20, top=20, bottom=20),
            expand=True,
            content=Row(
                wrap=True,
                # auto_scroll=True,  # 自动滑动到底部
                scroll=ScrollMode.AUTO,
                expand=True
            )
        )
        # img_path_list = list(glob.glob("C:\\Users\\xjhqre\\Desktop\\新建文件夹" + "/*"))
        # # 过滤掉其他文件
        # img_path_list = [name for name in img_path_list if os.path.splitext(name)[1] in config.allow_types]
        # self.render(img_path_list)
        return self.view

    # 渲染图片列表
    def render(self, img_path_list: List):
        for path in img_path_list:
            self.img_list_container.current.content.controls.append(
                Image(
                    src=path,
                    width=200,
                    height=200,
                    fit=ImageFit.CONTAIN,
                    repeat=ImageRepeat.NO_REPEAT,
                    border_radius=border_radius.all(10),
                )
            )
        # self.update()

# def main(page: Page):
#     list = Ref[ImgList]()
#     page.add(ImgList(list, page, None))
#
#
# flet.app(target=main, port=8550)
