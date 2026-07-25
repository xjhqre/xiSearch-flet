"""
设置视图
"""

from flet_core import Row, Container, padding, Column, MainAxisAlignment, KeyboardType

from src.config.config import config_instance
from src.enums.setting_type import SettingType
from src.views.setting.radio_item import RadioItem
from src.views.setting.setting_item import SettingItem


class SettingView(Container):

    def __init__(self, page, app_layout):
        self.app_layout = app_layout
        self.page = page

        super().__init__(
            padding=padding.symmetric(20, 50),
            expand=True,
            content=Column(
                spacing=30,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            SettingItem("特征文件保存地址: ", config_instance.get_feature_path(),
                                        SettingType.FEATURE_PATH, self.page),
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            SettingItem("搜索相似图片数量: ", config_instance.get_result_count(),
                                        SettingType.RESULT_COUNT, self.page, KeyboardType.NUMBER, 80, False)
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            RadioItem("提取特征是否包含子目录: ", config_instance.get_contains_sub_directories(), 80, False)
                        ]
                    )
                ]
            )
        )
