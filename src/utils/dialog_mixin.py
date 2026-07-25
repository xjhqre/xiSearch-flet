from flet_core import AlertDialog, Text, TextButton, MainAxisAlignment


class DialogMixin:
    _dialog: AlertDialog = None

    def _init_dialog(self, title="提示"):
        self._dialog = AlertDialog(
            title=Text(title),
            content=Text(""),
            actions=[TextButton("是", on_click=self._close_dialog)],
            actions_alignment=MainAxisAlignment.END,
        )

    def _show_dialog(self, message):
        self._dialog.content = Text(message)
        self.page.dialog = self._dialog
        self._dialog.open = True
        self.page.update()

    def _close_dialog(self, e=None):
        self._dialog.open = False
        self.page.update()