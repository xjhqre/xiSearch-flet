"""
搜索栏
"""

from flet_core import Container, Row, MainAxisAlignment, CrossAxisAlignment, FilePicker, \
    FilePickerResultEvent, icons, RoundedRectangleBorder, ButtonStyle, Ref, TextField, padding, margin, ElevatedButton, \
    Alignment

from src.config.config import config_instance


class SearchBar(Container):

    def __init__(self, ref, page, app_layout):
        self.app_layout = app_layout
        self.page = page
        self.file_path_text = Ref[TextField]()

        # 选择文件对话框
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        page.overlay.extend([self.pick_files_dialog])
        self.search_button = Ref[ElevatedButton]()
        self.file_select_button = Ref[ElevatedButton]()

        super().__init__(
            ref=ref,
            content=Row(
                # 水平居中对齐
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                # 垂直居中对齐
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        alignment=Alignment(0, 0),
                        expand=True,
                        # 输入框距 按钮 间隔50
                        margin=margin.only(right=50),
                        content=TextField(
                            content_padding=10,
                            value=config_instance.get_file_path(),
                            ref=self.file_path_text,
                            hint_text="请输入图片路径",
                            multiline=False,
                            expand=True,
                            # 保存输入数据
                            on_change=lambda e: config_instance.set_file_path(e.control.value)
                        ),
                    ),
                    Row(
                        spacing=20,
                        controls=[
                            # 选择图片按钮
                            ElevatedButton(
                                ref=self.file_select_button,
                                text="选择图片",
                                height=50,
                                width=130,
                                icon=icons.FOLDER_OPEN,
                                on_click=lambda _: self.pick_files_dialog.pick_files(),
                                # 方形圆角样式
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            # 搜索按钮
                            ElevatedButton(
                                ref=self.search_button,
                                text="搜索",
                                height=50,
                                width=130,
                                icon=icons.SEARCH,
                                # 方形圆角样式
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                                on_click=lambda _: self.search_image(),
                            )
                        ]
                    ),
                ]
            ),
        )

    # 文件选择结果回调
    def pick_files_result(self, e: FilePickerResultEvent):
        if not e.files:
            return
        self.file_path_text.current.value = e.files[0].path
        # 保存路径数据
        config_instance.set_file_path(e.files[0].path)
        self.file_path_text.current.update()

    # 搜索图片
    def search_image(self):
        self.search_button.current.disabled = True
        self.update()

        def on_search_complete(success):
            self.search_button.current.disabled = False
            self.update()

        self.app_layout.search_image(
            self.file_path_text.current.value.strip('"'),
            on_complete=on_search_complete
        )
