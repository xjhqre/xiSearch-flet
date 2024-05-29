"""
单个设置选项
"""

from flet_core import UserControl, Row, padding, \
    Text, TextField, InputBorder, CrossAxisAlignment, ControlEvent, KeyboardType, AlertDialog, TextButton, \
    MainAxisAlignment, RadioGroup, Column, Radio

from src.config.config import config_instance
from src.enum.setting_type import SettingType


class RadioItem(UserControl):

    def __init__(self, label, value, width=None, isExpand=True):
        super().__init__()
        self.view = None
        self.expand = True
        self.label = label  # 设置名称
        self.value = value  # 设置值
        self.width = width  # 宽度
        self.isExpend = isExpand  # 是否可扩展

    def build(self):
        # 导航栏容器
        self.view = Row(
            spacing=10,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text(
                    size=18,
                    value=self.label
                ),
                RadioGroup(
                    value=self.value,
                    on_change=self.update_setting,
                    content=Row(
                        controls=[
                            Radio(value="Y", label="是"),
                            Radio(value="N", label="否"),
                        ]
                    )
                )
            ]
        )
        return self.view

    def update_setting(self, e: ControlEvent):
        config_instance.set_contains_sub_directories(e.control.value)