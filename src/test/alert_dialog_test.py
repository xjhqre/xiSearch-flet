import flet as ft
from flet_core import Row


class MyDialog(Row):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=self.close_dlg),
                ft.TextButton("No", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    page.add(
        ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
    )


ft.app(target=main)
