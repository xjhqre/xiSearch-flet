import flet as ft
from flet_core import SnackBarBehavior, colors, DismissDirection, margin, Container, TextAlign, border, TextThemeStyle, \
    FontWeight


class Data:
    def __init__(self) -> None:
        self.counter = 0


d = Data()


def main(page):
    page.snack_bar = ft.SnackBar(
        content=Container(
            ft.Text(
                value="复制成功!",
                text_align=TextAlign.CENTER,
                color=colors.TEAL,
                font_family="微软雅黑",
                # weight=FontWeight.BOLD
            ),

        ),
        behavior=SnackBarBehavior.FLOATING,
        # width=200,
        bgcolor=colors.WHITE,
        dismiss_direction=DismissDirection.UP,
        duration=2000,
        margin=margin.only(bottom=30, left=1100, right=30),
    )

    def on_click(e):
        page.snack_bar.open = True
        d.counter += 1
        page.update()

    page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))


ft.app(target=main)
