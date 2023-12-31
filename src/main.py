import os
import sys

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import flet
from flet_core import Page, colors, theme

from views.app_layout import AppLayout


def main(page: Page):
    page.title = "xiSearch-flet"
    page.padding = 0
    # page.scroll = True,
    page.theme = theme.Theme(font_family="微软雅黑")
    page.theme.page_transitions.windows = "cupertino"
    page.bgcolor = colors.WHITE
    page.add(AppLayout(
        # self,
        page,
        tight=True,
        expand=True,
        auto_scroll=True,
        vertical_alignment="start",
    ))
    page.update()


flet.app(target=main, assets_dir="../assets")
