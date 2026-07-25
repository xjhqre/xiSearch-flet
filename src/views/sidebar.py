"""
左侧边栏
"""
import flet_core
from flet import (
    Column,
    Container,
    Text,
    NavigationRail,
    NavigationRailDestination,
    icons,
)
from flet_core import alignment

from src.constants import color_constant


class Sidebar(Container):

    def __init__(self, page, app_layout):
        self.app_layout = app_layout
        self.page = page

        self.nav_rail = NavigationRail(
            selected_index=None,
            label_type=flet_core.NavigationRailLabelType.ALL,
            on_change=self.nav_change,
            destinations=[
                NavigationRailDestination(
                    label_content=Text("图片搜索"),
                    label="图片搜索",
                    icon=icons.IMAGE_SEARCH,
                    selected_icon=icons.IMAGE_SEARCH,
                ),
                NavigationRailDestination(
                    label_content=Text("特征提取"),
                    label="特征提取",
                    icon=icons.FEATURED_PLAY_LIST,
                    selected_icon=icons.FEATURED_PLAY_LIST,
                ),
                NavigationRailDestination(
                    label_content=Text("设置"),
                    label="设置",
                    icon=icons.SETTINGS,
                    selected_icon=icons.SETTINGS,
                ),
            ],
            extended=True,
            expand=True,
            bgcolor=color_constant.side_bar_color
        )

        super().__init__(
            content=Column([self.nav_rail], tight=False),
            width=200,
            expand=True,
            alignment=alignment.center
        )

    # 导航点击事件
    def nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.nav_rail.selected_index = index
        self.update()
        if index == 0:
            self.app_layout.set_search_view()
        elif index == 1:
            self.app_layout.set_feature_view()
        elif index == 2:
            self.app_layout.set_setting_view()
        self.page.update()
