"""
提取日志显示框
"""

from flet_core import UserControl, Container, padding, margin, border, colors, Text, Column, ScrollMode, Ref, \
    OnScrollEvent


class ExtractLog(UserControl):

    def __init__(self, page, app_layout, ref):
        super().__init__(ref=ref)
        self.expand = True
        self.app_layout = app_layout
        self.view = None
        self.page = page
        self.container = Ref[Container]()
        self.column = Ref[Column]()
        self.log_text = Ref[Text]()
        self.is_scroll_to_bottom = True  # 是否自动滚动到最底下

    def build(self):
        self.view = Container(
            width=950,
            height=500,
            ref=self.container,
            margin=margin.only(top=20),
            border=border.all(1, colors.BLACK),
            border_radius=5,
            padding=padding.symmetric(20, 20),
            expand=True,
            content=Column(
                scroll=ScrollMode.AUTO,
                ref=self.column,
                auto_scroll=False,
                on_scroll=self.scroll_handler,
                controls=[
                    Text(
                        ref=self.log_text
                    )
                ]
            )
        )
        return self.view

    # 滚动到底部时自动下拉
    def scroll_handler(self, e: OnScrollEvent):
        if e.max_scroll_extent - e.pixels <= 100:
            self.is_scroll_to_bottom = True
        else:
            self.is_scroll_to_bottom = False
