import flet as ft
from flet_core import Container, Column, Row, Page, Ref, Text

from src.views.feature.extract_log import ExtractLog


class AppLayout(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.text_ref = Ref[Text]()
        self.extract_log = Ref[ExtractLog]()

        self.feature_view = Container(
            content=Column(
                controls=[
                    Text(ref=self.text_ref),
                    ExtractLog(ref=self.extract_log, page=self.page, app_layout=self)
                ]
            )
        )

        self.controls = [self.feature_view]
        print(self.text_ref.current)
        print(self.extract_log.current)


def main(page):
    page.add(AppLayout(page))


ft.app(target=main)
