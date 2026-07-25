"""
提取日志显示框
"""

from flet_core import Container, padding, margin, border, colors, Text, Column, ScrollMode, Ref, \
    OnScrollEvent


class ExtractLog(Container):

    def __init__(self, page, app_layout, ref):
        self.app_layout = app_layout
        self.page = page
        self.log_text = Ref[Text]()

        super().__init__(
            ref=ref,
            width=950,
            height=300,
            margin=margin.only(top=20),
            border=border.all(1, colors.BLACK),
            border_radius=5,
            padding=padding.symmetric(20, 20),
            expand=True,
            content=Column(
                scroll=ScrollMode.AUTO,
                auto_scroll=False,
                controls=[Text(ref=self.log_text)]
            )
        )
