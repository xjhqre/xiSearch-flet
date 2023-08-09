import flet as ft


def main(page: ft.Page):
    text = ft.Text(
        "fsdffdsf\nfsdfdsfdsf\nfsdfsfdsdfsdfsd\newrewwew\nfdsfdsfdsfds\nfsfddsfdsfd\ndfsfdsfdsfds\nfsdffdsf\nfsdfdsfdsf\nfsdfsfdsdfsdfsd\newrewwew\nfdsfdsfdsfds\nfsfddsfdsfd\ndfsfdsfdsfds\nfsdffdsf\nfsdfdsfdsf\nfsdfsfdsdfsdfsd\newrewwew\nfdsfdsfdsfds\nfsfddsfdsfd\ndfsfdsfdsfds\nfsdffdsf\nfsdfdsfdsf\nfsdfsfdsdfsdfsd\newrewwew\nfdsfdsfdsfds\nfsfddsfdsfd\ndfsfdsfdsfds\nfsdffdsf\nfsdfdsfdsf\nfsdfsfdsdfsdfsd\newrewwew\nfdsfdsfdsfds\nfsfddsfdsfd\ndfsfdsfdsfds\n",
        text_align="center",
    )
    col = ft.Column(
        controls=[text],
        scroll=ft.ScrollMode.ALWAYS,
        width=100,
        height=100,
        alignment="center",
        horizontal_alignment="center",
    )
    page.add(col)


ft.app(target=main)
