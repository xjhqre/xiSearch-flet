import flet
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
from flet_core import UserControl, Ref, FilledButton, ButtonStyle, RoundedRectangleBorder, Container


class Picket(UserControl):
    def __init__(self, page):
        super().__init__()
        self.view = None
        self.page = page

        # 输入文本框引用
        self.file_path_text = Ref[Text]()

        # 选择文件对话框
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        page.overlay.extend([self.pick_files_dialog])

        # 文件选择按钮
        self.file_select_button = FilledButton(
            text="选择图片",
            height=50,
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.pick_files_dialog.pick_files(),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            ),
        )

    def build(self):
        # 导航栏容器
        self.view = Container(
            content=Row(
                controls=[
                    Text(
                        value="test",
                        ref=self.file_path_text,
                    ),
                    self.file_select_button,
                ]
            ),
        )
        return self.view

    # 选择文件对话框
    def pick_files_result(self, e: FilePickerResultEvent):
        print(e.files)
        self.file_path_text.current.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.file_path_text.current.update()


def main(page: Page):
    page.add(
        Picket(page)
    )


flet.app(target=main)
