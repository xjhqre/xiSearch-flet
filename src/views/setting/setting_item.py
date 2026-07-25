"""
单个设置选项
"""

from flet_core import Row, padding, Text, TextField, InputBorder, CrossAxisAlignment, ControlEvent, KeyboardType, \
    MainAxisAlignment, AlertDialog, TextButton

import os

from src.config.config import config_instance
from src.constants.layout_constant import MIN_RESULT_COUNT, MAX_RESULT_COUNT
from src.enums.setting_type import SettingType


class SettingItem(Row):

    def __init__(self, label, value, setting_type, page, keyboard_type=KeyboardType.TEXT, width=None, isExpand=True):
        self.setting_type = setting_type
        self.page = page

        super().__init__(
            spacing=10,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text(size=18, value=label),
                TextField(
                    width=width,
                    expand=isExpand,
                    content_padding=padding.only(left=20),
                    keyboard_type=keyboard_type,
                    border=InputBorder.OUTLINE,
                    height=40,
                    value=value,
                    on_change=self.update_setting
                )
            ]
        )

    def update_setting(self, e: ControlEvent):
        if self.setting_type == SettingType.FEATURE_PATH:
            if not e.control.value.endswith(os.sep):
                e.control.value += os.sep
            config_instance.set_feature_path(e.control.value)
        elif self.setting_type == SettingType.RESULT_COUNT:
            # 校验输入文本类型
            if not e.control.value.isdigit():
                self._show_error("请输入{}~{}的整数".format(MIN_RESULT_COUNT, MAX_RESULT_COUNT))
                return
            if not (MIN_RESULT_COUNT <= int(e.control.value) <= MAX_RESULT_COUNT):
                self._show_error("请输入{}~{}的整数".format(MIN_RESULT_COUNT, MAX_RESULT_COUNT))
                return
            config_instance.set_result_count(e.control.value)

    def _show_error(self, message):
        dialog = AlertDialog(
            title=Text("提示"),
            content=Text(message),
            actions=[TextButton("确定", on_click=lambda e: self._close_dialog(dialog))],
            actions_alignment=MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _close_dialog(self, dialog):
        dialog.open = False
        self.page.update()
