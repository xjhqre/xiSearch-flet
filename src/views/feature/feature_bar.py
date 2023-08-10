"""
特征向量存储地址栏，设置存储向量的保存地址
"""
from flet_core import UserControl, Container, padding, Row, MainAxisAlignment, CrossAxisAlignment, TextField, margin, \
    FilledButton, icons, ButtonStyle, RoundedRectangleBorder, ElevatedButton

from src.config.config import config_instance


class FeatureBar(UserControl):

    def __init__(self, ref, page, app_layout):
        super().__init__(ref=ref)
        self.app_layout = app_layout
        self.view = None
        self.page = page

    def build(self):
        self.view = Container(
            expand=True,
            padding=padding.symmetric(0, 50),
            content=Row(
                # 水平居中对齐
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                # 垂直居中对齐
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        expand=True,
                        # 输入框距 按钮 间隔50
                        margin=margin.only(right=50),
                        content=TextField(
                            content_padding=10,
                            value=config_instance.get_gallery_path(),
                            hint_text="请输入图片库地址",
                            # width=700,
                            # height=50,
                            expand=True,
                            # 保存输入数据
                            on_change=lambda e: config_instance.set_gallery_path(e.control.value),
                        )
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="提取特征",
                                height=50,
                                width=130,
                                icon=icons.START,
                                on_click=self.app_layout.extract_feature,
                                # 方形圆角样式
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                            )
                        ]
                    ),
                ]
            )
        )
        return self.view
