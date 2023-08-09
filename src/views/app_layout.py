import glob
import os
import time

import torch
from flet import (
    Control,
    Page,
    Row,
    Text,
)
from flet_core import Column, MainAxisAlignment, Ref, Container, padding, CrossAxisAlignment

from src.data.config import config_instance
from src.utils import sentence_transformer_utils
from src.views.feature.extract_log import ExtractLog
from src.views.feature.feature_bar import FeatureBar
from src.views.search.img_list import ImgList
from src.views.search.search_bar import SearchBar
from src.views.sidebar import Sidebar


class AppLayout(Row):
    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.sidebar = Sidebar(page, self)
        self.expand = True
        self.search_bar = Ref[SearchBar]()
        self.img_list = Ref[ImgList]()
        self.feature_bar = Ref[FeatureBar]()
        self.extract_log = Ref[ExtractLog]()

        # 搜索视图
        self.search_view = Ref[Container]()
        Container(
            ref=self.search_view,
            expand=True,
            padding=padding.only(0, 50, 0, 0),
            content=Column(
                # 垂直居中对齐
                alignment=MainAxisAlignment.START,
                # 水平居中对齐
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    # 搜索栏
                    SearchBar(ref=self.search_bar, page=self.page, app_layout=self),
                    # 图片展示列表
                    ImgList(ref=self.img_list, page=self.page, app_layout=self),
                ]
            )
        )

        # 提取特征视图
        self.feature_view = Ref[Container]()
        Container(
            ref=self.feature_view,
            expand=True,
            padding=padding.only(0, 50, 0, 0),
            content=Column(
                # 垂直居中对齐
                alignment=MainAxisAlignment.START,
                # 水平居中对齐
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    # 特征向量存储地址栏
                    FeatureBar(ref=self.feature_bar, page=self.page, app_layout=self),
                    # 提取日志框
                    ExtractLog(ref=self.extract_log, page=self.page, app_layout=self)
                ]
            )
        )

        # 设置视图
        self.setting_view = Text("设置视图")

        # 类成员变量的初始化语句，Control是变量的类型，self.all_boards_view是初始值。
        # 右侧界面的激活视图，默认为搜索视图
        self._active_view: Ref[Container] = self.search_view
        self.controls = [self.sidebar, self.active_view.current]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()

    # 切换到搜索视图
    def set_search_view(self):
        self.active_view = self.search_view.current
        self.sidebar.nav_rail.selected_index = 0  # 导航栏选择索引为0

    # 切换到提取特征视图
    def set_feature_view(self):
        self.active_view = self.feature_view.current
        self.sidebar.nav_rail.selected_index = 1  # 导航栏选择索引为1
        # self.sidebar.update()
        # self.page.update()

    # 切换到设置视图
    def set_setting_view(self):
        self.active_view = self.setting_view
        self.sidebar.nav_rail.selected_index = 2  # 导航栏选择索引为1
        # self.sidebar.update()
        # self.page.update()

    # 提取特征按钮点击触发函数，开始提取特征，extract_log 显示日志
    def extract_feature(self, feature_bar: FeatureBar):
        time_start = time.time()  # 记录提取开始时间
        error_img = []  # 错误图片列表
        extract_log_text = ""  # 记录日志

        img_path_list = list(glob.glob(config_instance.get_gallery_path() + "/*"))
        # 过滤掉非图片类型的文件
        img_path_list = [name for name in img_path_list if
                         os.path.splitext(name)[1] in config_instance.get_allow_types()]

        img_emb_list = None  # 特征向量
        img_path_list_batch = []  # 记录一部分图片路径，和 img_emb_list 一一对应
        cnt = 1  # 记录当前提取的图片索引
        extract_log_text += "开始提取！\n"
        for img_path in img_path_list:
            try:
                img_emb = sentence_transformer_utils.extract(img_path)

                img_path_list_batch.append(img_path)
                if img_emb_list is None:
                    img_emb_list = img_emb
                else:
                    img_emb_list = torch.concat((img_emb_list, img_emb), dim=0)

                # 每 1024 个维度存储一次
                if cnt % 1024 == 0:
                    sentence_transformer_utils.dump(img_path_list_batch, img_emb_list)
                    img_path_list_batch.clear()
                    img_emb_list = None

                extract_log_text += "当前提取图片：" + img_path + " --> " + str(cnt) + "\n"
                cnt += 1
                self.extract_log.current.log_text.current.value = extract_log_text
                self.extract_log.current.update()
            except Exception as e:
                # 图片打开失败
                print(e)
                error_img.append(img_path)
                img_path_list.remove(img_path)

        # 存储剩余维度
        sentence_transformer_utils.dump(img_path_list_batch, img_emb_list)

        time_end = time.time()  # 记录结束时间
        time_sum = time_end - time_start
        extract_log_text += "提取结束，总共耗时：" + str(time_sum) + "秒\n"

        if error_img:
            extract_log_text += "提取失败图片:\n"
            for path in error_img:
                extract_log_text += path + "\n"

        self.extract_log.current.log_text.current.value = extract_log_text
        self.extract_log.current.update()

# def main(page: Page):
#     page.title = "Flet Trello clone"
#     page.padding = 0
#     # page.theme = theme.Theme(font_family="Verdana")
#     # page.theme.page_transitions.windows = "cupertino"
#     page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
#     page.bgcolor = colors.BLUE_GREY_200
#     app_layout = AppLayout(page, tight=False,
#                            expand=False,
#                            vertical_alignment="start")
#     page.add(app_layout)
#     page.update()
#     # app.initialize()
#
#
# flet.app(target=main, assets_dir="../assets")
