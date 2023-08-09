import glob

import flet as ft
from flet_core import ScrollMode, Container


def main(page: ft.Page):
    # wrap：是否包裹，若为True则将超出视图的部分放到下一行显示；若为False，则只显示一行
    # scroll：滚动条显示策略
    # expend：是否可以滚动
    r = Container(
        padding=50,
        expand=True,
        content=ft.Row(
            wrap=True,
            scroll=ScrollMode.AUTO,
            expand=True
        )
    )

    # page.add(
    #     Row(
    #         auto_scroll=True,
    #         expand=True,
    #         controls=[
    #             TextField(value="afsasfasf"),
    #             Container(
    #                 expand=True,
    #                 content=Column(
    #                     # 垂直居中对齐
    #                     alignment=MainAxisAlignment.START,
    #                     # 水平居中对齐
    #                     horizontal_alignment=CrossAxisAlignment.CENTER,
    #                     auto_scroll=True,
    #                     expand=True,
    #                     controls=[
    #                         TextField(value="sadasfasf"),
    #                         r
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    # )

    page.add(r)

    for path in list(
            # glob.glob("F:\ACG\壁纸" + "/*")
            glob.glob("C:\\Users\\xjhqre\\Desktop\\新建文件夹" + "/*")
    ):
        r.content.controls.append(
            ft.Image(
                src=path,
                # width=200,
                height=150,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                tooltip="xjhqre",
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()


ft.app(target=main)
