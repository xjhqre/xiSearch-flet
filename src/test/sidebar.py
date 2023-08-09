"""
左侧边栏
"""
import flet
import flet_core
from flet import (
    UserControl,
    Column,
    Container,
    Text,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    colors,
    icons,
)
from flet_core import alignment, Page, ElevatedButton, theme


def main(page: Page):
    page.title = "xiSearch-flet"
    page.padding = 0
    # page.scroll = True,
    page.theme = theme.Theme(font_family="微软雅黑")
    page.theme.page_transitions.windows = "cupertino"
    page.bgcolor = colors.WHITE
    page.update()


flet.app(target=main, assets_dir="../assets")
