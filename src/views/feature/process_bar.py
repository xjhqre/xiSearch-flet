"""
提取日志显示框
"""

from flet_core import Container, padding, margin, colors, Text, Ref, Row, ProgressBar, MainAxisAlignment

from src.constants import color_constant


class ExtractProcessBar(Container):

    def __init__(self, page, app_layout, ref):
        self.app_layout = app_layout
        self.page = page
        self.process_bar = Ref[ProgressBar]()
        self.progress_percentage = Ref[Text]()

        super().__init__(
            ref=ref,
            width=950,
            margin=margin.only(top=20),
            border_radius=5,
            padding=padding.symmetric(20, 0),
            expand=True,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.START,
                controls=[
                    Text(value="提取进度: ", size=18),
                    ProgressBar(
                        ref=self.process_bar,
                        value=0,
                        width=750,
                        height=20,
                        color=colors.INDIGO,
                        bgcolor=color_constant.process_bar_bg_color
                    ),
                    Text(ref=self.progress_percentage, value="0%", size=18),
                ]
            )
        )

    def reset_process_bar(self):
        self.process_bar.current.value = 0
        self.progress_percentage.current.value = "0%"
