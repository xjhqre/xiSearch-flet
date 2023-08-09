"""
搜索栏
"""
from flet_core import UserControl, Container, Row, MainAxisAlignment, CrossAxisAlignment, FilledButton, FilePicker, \
    FilePickerResultEvent, icons, RoundedRectangleBorder, ButtonStyle, Ref, TextField, padding, margin

from src.data.config import config_instance


class SearchBar(UserControl):

    def __init__(self, ref, page, app_layout):
        super().__init__(ref)
        self.app_layout = app_layout
        self.view = None
        self.page = page

        # 输入文本框引用
        self.file_path_text = Ref[TextField]()

        # 选择文件对话框
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        page.overlay.extend([self.pick_files_dialog])

        # 搜索按钮
        self.search_button = FilledButton(
            text="搜索",
            height=50,
            width=130,
            icon=icons.SEARCH,
            # 方形圆角样式
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            ),
        )
        # 文件选择按钮
        self.file_select_button = FilledButton(
            text="选择图片",
            height=50,
            width=130,
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.pick_files_dialog.pick_files(),
            # 方形圆角样式
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            ),
        )

    def build(self):
        # 搜索栏容器
        self.view = Container(
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
                            # value=config_instance.get_file_path(),
                            ref=self.file_path_text,
                            hint_text="请输入图片路径",
                            # width=700,
                            height=50,
                            expand=True,
                            # 保存输入数据
                            on_change=lambda e: config_instance.set_file_path(e.control.value)
                            # shift_enter=True,
                            # on_submit="asd",
                        ),

                    ),
                    Row(
                        controls=[
                            self.file_select_button,
                            self.search_button
                        ]
                    ),
                ]
            ),
        )
        return self.view

    # 文件选择结果回调
    def pick_files_result(self, e: FilePickerResultEvent):
        self.file_path_text.current.value = e.files[0].path
        # 保存路径数据
        config_instance.set_file_path(e.files[0].path)
        self.file_path_text.current.update()

# def main(page: Page):
#     page.add(
#         SearchBar(page, None)
#     )
#
#
# flet.app(target=main)
