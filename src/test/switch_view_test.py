import flet
import flet_core
from flet_core import Row, Page, TextField, border, colors, Ref, Container, Text, UserControl, \
    NavigationRailDestination, icons, NavigationRail, Column, alignment


class MyTestField(UserControl):
    def __init__(self):
        super().__init__()
        self.view = None

    def build(self):
        self.view = Container(
            content=TextField(border=border.all(1, colors.BLACK))
        )
        return self.view


class Sidebar(UserControl):

    def __init__(self, page, app_layout):
        super().__init__()
        self.app_layout = app_layout
        self.view = None
        self.page = page

        self.nav_items = [
            NavigationRailDestination(
                label_content=Text(
                    "index_1",
                ),
                label="index_1",
                icon=icons.IMAGE_SEARCH,
                selected_icon=icons.IMAGE_SEARCH,

            ),
            NavigationRailDestination(
                label_content=Text(
                    "index_2",
                ),
                label="index_2",
                icon=icons.FEATURED_PLAY_LIST,
                selected_icon=icons.FEATURED_PLAY_LIST
            ),
        ]

        self.nav_rail = NavigationRail(
            selected_index=None,
            label_type=flet_core.NavigationRailLabelType.ALL,
            on_change=self.nav_change,
            destinations=self.nav_items,
            extended=True,
            expand=True,
        )

    def build(self):
        self.view = Container(
            content=Column(
                [
                    self.nav_rail,
                ],
                tight=False),
            width=200,
            expand=True,
            bgcolor=colors.WHITE,
            alignment=alignment.center
        )
        return self.view

    def nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            self.app_layout.set_first_view()
        elif index == 1:
            self.app_layout.set_second_view()
        self.page.update()


class AppLayout(Row):
    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.sidebar = Sidebar(page, self)

        self.text_field_1 = Container(
            content=MyTestField()
        )

        self.text_field_2 = Text()

        self._active_view = self.text_field_1
        self.controls = [self.sidebar, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()

    def set_first_view(self):
        self.active_view = self.text_field_1
        self.sidebar.nav_rail.selected_index = 0

    def set_second_view(self):
        self.active_view = self.text_field_2
        self.sidebar.nav_rail.selected_index = 1


def main(page: Page):
    page.add(AppLayout(
        page,
        tight=True,
        expand=True,
        auto_scroll=True,
        vertical_alignment="start",
    ))
    page.update()


flet.app(target=main)
