"""
单个设置选项
"""

from flet_core import UserControl, Row, padding, \
    Text, TextField, InputBorder, CrossAxisAlignment, ControlEvent, KeyboardType, AlertDialog, TextButton, \
    MainAxisAlignment

from src.config.config import config_instance
from src.enum.setting_type import SettingType


class SettingItem(UserControl):

    def __init__(self, label, value, setting_type, keyboard_type=KeyboardType.TEXT, width=None, isExpand=True):
        super().__init__()
        self.view = None
        self.expand = True
        self.label = label  # 设置名称
        self.value = value  # 设置值
        self.setting_type = setting_type  # 设置类型
        self.keyboard_type = keyboard_type  # 输入类型
        self.width = width  # 宽度
        self.isExpend = isExpand  # 是否可扩展

        # 提示对话框
        self.dialog = AlertDialog(
            title=Text("提示"),
            content=Text(""),
            actions=[
                TextButton("是", on_click=self.close_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

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
                TextField(
                    width=self.width,
                    expand=self.isExpend,
                    content_padding=padding.only(left=20),
                    keyboard_type=self.keyboard_type,
                    border=InputBorder.OUTLINE,
                    height=40,
                    value=self.value,
                    on_change=self.update_setting
                )
            ]
        )
        return self.view

    def update_setting(self, e: ControlEvent):
        self.value = e.control.value
        if self.setting_type == SettingType.FEATURE_PATH:
            if e.control.value[-1] != '/' and e.control.value[-1] != '\\':
                e.control.value += '\\'
            config_instance.set_feature_path(e.control.value)
        elif self.setting_type == SettingType.RESULT_COUNT:
            # 校验输入文本类型
            if not e.control.value.isdigit():
                self.dialog.content = Text("请输入1~100的整数")
                self.open_dialog()
                return
            if not (1 <= int(e.control.value) <= 100):
                self.dialog.content = Text("请输入1~100的整数")
                self.open_dialog()
                return
            config_instance.set_result_count(e.control.value)

    # 打开提示对话框
    def open_dialog(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    # 关闭提示对话框
    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()
