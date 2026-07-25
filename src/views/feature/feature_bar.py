"""
特征向量存储地址栏，设置存储向量的保存地址
"""
from flet_core import Container, padding, Row, MainAxisAlignment, CrossAxisAlignment, TextField, margin, \
    icons, ButtonStyle, RoundedRectangleBorder, ElevatedButton, Ref, colors

from src.config.config import config_instance
from src.constants.layout_constant import (
    CONTENT_HORIZONTAL_PADDING,
    BUTTON_HEIGHT,
    EXTRACT_BUTTON_WIDTH,
    BUTTON_BORDER_RADIUS,
    FEATURE_BAR_MARGIN_RIGHT,
)


class FeatureBar(Container):

    def __init__(self, ref, page, app_layout):
        self.app_layout = app_layout
        self.page = page
        self.cancel_extract_button = Ref[ElevatedButton]()

        super().__init__(
            ref=ref,
            expand=True,
            padding=padding.symmetric(0, CONTENT_HORIZONTAL_PADDING),
            content=Row(
                # 水平居中对齐
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                # 垂直居中对齐
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        expand=True,
                        # 输入框距 按钮 间隔50
                        margin=margin.only(right=FEATURE_BAR_MARGIN_RIGHT),
                        content=TextField(
                            content_padding=10,
                            value=config_instance.get_gallery_path(),
                            hint_text="请输入图片库地址",
                            expand=True,
                            on_change=lambda e: config_instance.set_gallery_path(e.control.value),
                        )
                    ),
                    Row(
                        spacing=10,
                        controls=[
                            ElevatedButton(
                                text="提取特征",
                                height=BUTTON_HEIGHT,
                                width=EXTRACT_BUTTON_WIDTH,
                                icon=icons.START,
                                on_click=self.app_layout.extract_feature,
                                # 方形圆角样式
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=BUTTON_BORDER_RADIUS),
                                ),
                            ),
                            ElevatedButton(
                                ref=self.cancel_extract_button,
                                text="取消",
                                height=BUTTON_HEIGHT,
                                width=EXTRACT_BUTTON_WIDTH,
                                visible=False,
                                icon=icons.CANCEL,
                                on_click=self.app_layout.cancel_extraction,
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=BUTTON_BORDER_RADIUS),
                                    color=colors.RED,
                                ),
                            ),
                        ]
                    ),
                ]
            )
        )
