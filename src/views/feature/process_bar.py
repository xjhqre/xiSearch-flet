"""
提取日志显示框
"""

from flet_core import UserControl, Container, padding, margin, border, colors, Text, Column, ScrollMode, Ref, \
    OnScrollEvent, Row, ProgressBar, MainAxisAlignment

from src.constants import color_constant


class ExtractProcessBar(UserControl):

    def __init__(self, page, app_layout, ref):
        super().__init__(ref=ref)
        self.expand = True
        self.app_layout = app_layout
        self.view = None
        self.page = page
        self.container = Ref[Container]()
        self.process_bar = Ref[ProgressBar]()
        self.progress_percentage = Ref[Text]()

    def build(self):
        self.view = Container(
            width=950,
            ref=self.container,
            margin=margin.only(top=20),
            # border=border.all(1, colors.BLACK),
            border_radius=5,
            padding=padding.symmetric(20, 0),
            expand=True,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.START,
                controls=[
                    Text(
                        value="提取进度: ",
                        size=18
                    ),
                    ProgressBar(
                        ref=self.process_bar,
                        value=0,
                        width=750,
                        height=20,
                        color=colors.INDIGO,
                        bgcolor=color_constant.process_bar_bg_color
                    ),
                    Text(
                        ref=self.progress_percentage,
                        value="0%",
                        size=18
                    ),

                ]
            )
        )
        return self.view

    def reset_process_bar(self):
        self.process_bar.current.value = 0
        self.progress_percentage.current.value = "0%"
