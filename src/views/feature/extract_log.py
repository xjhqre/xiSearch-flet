"""
提取日志显示框
"""

from flet_core import UserControl, Container, padding, margin, border, colors, Text, Column, ScrollMode, Ref


class ExtractLog(UserControl):

    def __init__(self, page, app_layout, ref):
        super().__init__(ref=ref)
        self.expand = True
        self.app_layout = app_layout
        self.view = None
        self.page = page
        self.log_text = Ref[Text]()

    def build(self):
        self.view = Container(
            width=950,
            height=500,
            margin=margin.only(top=20),
            border=border.all(1, colors.BLACK),
            border_radius=5,
            padding=padding.symmetric(20, 20),
            expand=True,
            content=Column(
                scroll=ScrollMode.AUTO,
                auto_scroll=True,
                controls=[
                    Text(
                        ref=self.log_text
                    )
                ]
            )
        )
        return self.view
