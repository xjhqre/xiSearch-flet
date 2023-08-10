import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Container(
            ft.Stack(
                [
                    ft.Container(width=20, height=20, bgcolor=ft.colors.RED, border_radius=5),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.colors.YELLOW,
                        border_radius=5,
                        right=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.colors.BLUE,
                        border_radius=5,
                        right=0,
                        bottom=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.colors.GREEN,
                        border_radius=5,
                        left=0,
                        bottom=0,
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.colors.PURPLE,
                                border_radius=5,
                            )
                        ],
                        left=35,
                        top=35,
                    ),
                ]
            ),
            border_radius=8,
            padding=5,
            width=100,
            height=100,
            bgcolor=ft.colors.BLACK,
        )
    )


ft.app(target=main)
