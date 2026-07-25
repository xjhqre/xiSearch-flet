"""
图片展示列表
"""
import os

from flet_core import Row, Image, ImageFit, ImageRepeat, border_radius, Container, Ref, padding, \
    ScrollMode, border, colors, margin, ControlEvent, SnackBar, Text, TextAlign, SnackBarBehavior, Column, \
    CrossAxisAlignment

from src.constants.layout_constant import (
    IMG_DISPLAY_BATCH_SIZE,
    IMG_LIST_CONTAINER_WIDTH,
    IMG_LIST_CONTAINER_HEIGHT,
    IMG_LIST_BORDER_RADIUS,
    IMG_LIST_MARGIN_TOP,
    IMG_LIST_PADDING_VERTICAL,
    IMG_LIST_PADDING_HORIZONTAL,
    IMG_THUMB_HEIGHT,
    SNACK_BAR_WIDTH,
    SNACK_BAR_DURATION,
    SNACK_BAR_MARGIN_BOTTOM,
    SNACK_BAR_MARGIN_LEFT,
    SNACK_BAR_MARGIN_RIGHT,
)


class ImgList(Container):

    def __init__(self, ref, page, app_layout):
        self.app_layout = app_layout
        self.page = page
        self.img_list_Row = Ref[Row]()

        self.page.snack_bar = SnackBar(
            Text(value="复制成功!", color=colors.TEAL, text_align=TextAlign.CENTER),
            width=SNACK_BAR_WIDTH,
            behavior=SnackBarBehavior.FLOATING,
            bgcolor=colors.WHITE,
            duration=SNACK_BAR_DURATION,
            margin=margin.only(bottom=SNACK_BAR_MARGIN_BOTTOM, left=SNACK_BAR_MARGIN_LEFT, right=SNACK_BAR_MARGIN_RIGHT),
        )

        super().__init__(
            ref=ref,
            width=IMG_LIST_CONTAINER_WIDTH,
            height=IMG_LIST_CONTAINER_HEIGHT,
            margin=margin.only(top=IMG_LIST_MARGIN_TOP),
            border=border.all(1, colors.BLACK),
            border_radius=IMG_LIST_BORDER_RADIUS,
            padding=padding.symmetric(IMG_LIST_PADDING_VERTICAL, IMG_LIST_PADDING_HORIZONTAL),
            expand=True,
            content=Row(
                ref=self.img_list_Row,
                wrap=True,
                scroll=ScrollMode.AUTO,
                expand=True,
            )
        )

    # 展示图片列表
    def show_result_image(self, similar_img_list):
        if similar_img_list is None or similar_img_list == []:
            return
        # 清空上一次搜索结果
        self.img_list_Row.current.clean()
        # 滚动条移动到最上方
        self.img_list_Row.current.scroll_to(offset=0, duration=500)

        for i in range(0, len(similar_img_list), IMG_DISPLAY_BATCH_SIZE):
            batch = similar_img_list[i:i + IMG_DISPLAY_BATCH_SIZE]
            for path in batch:
                self.img_list_Row.current.controls.append(self._build_image_control(path))
            self.update()

    def _build_image_control(self, path):
        filename = os.path.basename(path)
        filename_without_extension = os.path.splitext(filename)[0]
        return Container(
            content=Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        on_click=self.open_local_file,
                        content=Image(
                            tooltip=path,
                            src=path,
                            height=IMG_THUMB_HEIGHT,
                            fit=ImageFit.CONTAIN,
                            repeat=ImageRepeat.NO_REPEAT,
                            border_radius=border_radius.all(10),
                        )
                    ),
                    Container(
                        on_click=self.copy_path,
                        content=Text(
                            value=filename_without_extension
                        )
                    )
                ]
            ),
        )

    # 点击图片复制图片路径到剪贴板
    def copy_path(self, e: ControlEvent):
        self.page.set_clipboard(e.control.content.value)
        self.page.snack_bar.open = True
        self.page.update()

    def open_local_file(self, e: ControlEvent):
        os.startfile(e.control.content.src)
