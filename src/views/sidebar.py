"""
左侧边栏
"""
import flet_core
from flet import (
    UserControl,
    Column,
    Container,
    Text,
    NavigationRail,
    NavigationRailDestination,
    icons,
)
from flet_core import alignment

from src.constants import color_constant


class Sidebar(UserControl):

    def __init__(self, page, app_layout):
        super().__init__()
        self.app_layout = app_layout
        self.view = None
        self.page = page

        # 导航栏选项
        self.nav_items = [
            NavigationRailDestination(
                label_content=Text(
                    "图片搜索",
                ),
                label="图片搜索",
                icon=icons.IMAGE_SEARCH,
                selected_icon=icons.IMAGE_SEARCH,

            ),
            NavigationRailDestination(
                label_content=Text(
                    "特征提取",
                ),
                label="特征提取",
                icon=icons.FEATURED_PLAY_LIST,
                selected_icon=icons.FEATURED_PLAY_LIST,
            ),
            NavigationRailDestination(
                label_content=Text(
                    "设置",
                ),
                label="设置",
                icon=icons.SETTINGS,
                selected_icon=icons.SETTINGS
            ),

        ]

        # 导航栏
        self.nav_rail = NavigationRail(
            selected_index=None,  # 默认选中索引
            label_type=flet_core.NavigationRailLabelType.ALL,
            on_change=self.nav_change,  # 导航栏选项改变
            destinations=self.nav_items,  # 导航栏选项
            extended=True,  # 设置内容横向扩展
            expand=True,  # 设置伸展，填充满父容器
            bgcolor=color_constant.side_bar_color
        )

    def build(self):
        # 导航栏容器
        self.view = Container(
            content=Column(
                [
                    self.nav_rail,
                ],
                # 指定垂直方向应占用多少空间。默认值为 False - 将所有空间分配给子级。
                tight=False),
            width=200,
            expand=True,
            alignment=alignment.center
        )
        return self.view

    # 导航点击事件
    def nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            self.app_layout.set_search_view()
        elif index == 1:
            self.app_layout.set_feature_view()
        elif index == 2:
            self.app_layout.set_setting_view()
        self.page.update()
