"""
左侧边栏
"""
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
from flet_core import alignment


class Sidebar(UserControl):

    def __init__(self, page, app_layout):
        super().__init__()
        self.app_layout = app_layout
        self.view = None
        self.page = page

        # 导航栏选项
        self.nav_items = [
            NavigationRailDestination(
                # 目的地的标签 Control。
                # 与 NavigationRail 一起使用时必须提供标签。当label_type='none'时，标签仍然用于语义，并且如果extended为True，则仍然可以使用。
                label_content=Text(
                    "图片搜索",
                    font_family='微软雅黑'
                ),
                # 同上
                label="图片搜索",
                icon=icons.IMAGE_SEARCH,
                selected_icon=icons.IMAGE_SEARCH,

            ),
            NavigationRailDestination(
                label_content=Text(
                    "特征提取",
                    font_family='微软雅黑'
                ),
                label="特征提取",
                icon=icons.FEATURED_PLAY_LIST,
                selected_icon=icons.FEATURED_PLAY_LIST
            ),
            NavigationRailDestination(
                label_content=Text(
                    "设置",
                    font_family='微软雅黑'
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
            # bgcolor=colors.BLUE_GREY,
            extended=True,  # 设置内容横向扩展
            expand=True,  # 设置伸展，填充满父容器
            # group_alignment=-1.0  # 垂直方向上的对齐，-1.0：顶部  0.0：中间  1.0：底部  默认-1.0
            # height=110
        )
        self.toggle_nav_rail_button = IconButton(icons.ARROW_BACK)

    def build(self):
        # 导航栏容器
        self.view = Container(
            content=Column(
                [
                    self.nav_rail,
                ],
                # 指定垂直方向应占用多少空间。默认值为 False - 将所有空间分配给子级。
                tight=False),
            # padding=padding.all(30),  # 导航容器内边距
            # margin=margin.all(0),
            width=200,
            expand=True,
            bgcolor=colors.WHITE,
            alignment=alignment.center
        )
        return self.view

    def toggle_nav_rail(self, e):
        self.view.visible = not self.view.visible
        self.view.update()
        self.page.update()

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
        # print(self.page.route)
        self.page.update()

# def main(page: Page):
#     page.title = "Flet Trello clone"
#     page.padding = 0
#     # page.theme = theme.Theme(font_family="Verdana")
#     # page.theme.page_transitions.windows = "cupertino"
#     page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
#     page.bgcolor = colors.BLUE_GREY_200
#     app = Sidebar(page)
#     page.add(app)
#     page.update()
#     # app.initialize()
#
#
# flet.app(target=main, assets_dir="../assets")
