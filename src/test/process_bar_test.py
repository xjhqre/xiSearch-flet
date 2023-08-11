from time import sleep

import flet as ft
from flet_core import colors


def main(page: ft.Page):
    pb = ft.ProgressBar(width=400, height=20, color=colors.AMBER, bgcolor="#eeeeee")

    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ft.Text("Doing something..."), pb]),
    )

    for i in range(0, 101):
        pb.value = i * 0.01
        sleep(0.1)
        page.update()


ft.app(target=main)
