"""
设置视图
"""

from flet_core import UserControl, Row, Image, ImageFit, ImageRepeat, border_radius, Container, Ref, padding, \
    ScrollMode, border, colors, margin, Column, MainAxisAlignment, KeyboardType

from src.config.config import config_instance
from src.enum.setting_type import SettingType
from src.views.setting.setting_item import SettingItem


class SettingView(UserControl):

    def __init__(self, page, app_layout):
        super().__init__()
        self.app_layout = app_layout
        self.view = None
        self.expand = True
        self.page = page

    def build(self):
        # 导航栏容器
        self.view = Container(
            # width=950,
            # height=500,
            padding=padding.symmetric(20, 50),
            expand=True,
            content=Column(
                spacing=30,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            SettingItem("特征文件保存地址: ", config_instance.get_feature_path(),
                                        SettingType.FEATURE_PATH),
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            SettingItem("搜索相似图片数量: ", config_instance.get_result_count(),
                                        SettingType.RESULT_COUNT, KeyboardType.NUMBER, 80, False)
                        ]
                    )
                ]
            )
        )
        return self.view
