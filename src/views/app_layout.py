import glob
import os
import time
import traceback

import torch
from flet import (
    Page,
    Row,
    Text,
)
from flet_core import Column, MainAxisAlignment, Ref, Container, padding, CrossAxisAlignment, AlertDialog, TextButton, \
    ControlEvent, ElevatedButton, Stack

from src.config.config import config_instance
from src.exception.no_feature_file_exception import NoFeatureFileException
from src.exception.no_feature_path_exception import NoFeaturePathException
from src.utils import sentence_transformer_utils
from src.views.feature.extract_log import ExtractLog
from src.views.feature.feature_bar import FeatureBar
from src.views.feature.process_bar import ExtractProcessBar
from src.views.search.img_list import ImgList
from src.views.search.search_bar import SearchBar
from src.views.setting.setting_view import SettingView
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
        self.extract_process_bar = Ref[ExtractProcessBar]()

        # 搜索视图
        self.search_view = Container(
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
        self.feature_view = Container(
            expand=True,
            visible=False,
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
                    ExtractLog(ref=self.extract_log, page=self.page, app_layout=self),
                    # 提取进度条
                    ExtractProcessBar(ref=self.extract_process_bar, page=self.page, app_layout=self)
                ]
            )
        )

        # 设置视图
        self.setting_view = Container(
            expand=True,
            visible=False,
            padding=padding.only(0, 20, 0, 0),
            content=Column(
                expand=True,
                controls=[
                    SettingView(self.page, self)
                ]
            )
        )

        # 提示对话框
        self.dialog = AlertDialog(
            title=Text("提示"),
            content=Text(""),
            actions=[
                TextButton("是", on_click=self.close_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        # 类成员变量的初始化语句，Control是变量的类型，self.all_boards_view是初始值。
        # 右侧界面的激活视图，默认为搜索视图
        self.view_stack = Stack(
            controls=[self.setting_view, self.feature_view, self.search_view],
            expand=True,
        )
        self.controls = [self.sidebar, self.view_stack]

    # 切换到搜索视图
    def set_search_view(self):
        self.setting_view.visible = False
        self.feature_view.visible = False
        self.search_view.visible = True
        self.sidebar.nav_rail.selected_index = 0  # 导航栏选择索引为0

    # 切换到提取特征视图
    def set_feature_view(self):
        self.setting_view.visible = False
        self.feature_view.visible = True
        self.search_view.visible = False
        self.sidebar.nav_rail.selected_index = 1  # 导航栏选择索引为1

    # 切换到设置视图
    def set_setting_view(self):
        self.setting_view.visible = True
        self.feature_view.visible = False
        self.search_view.visible = False
        self.sidebar.nav_rail.selected_index = 2  # 导航栏选择索引为1

    # 提取特征按钮点击触发函数，开始提取特征，extract_log 显示日志
    def extract_feature(self, e: ControlEvent):
        extract_button: ElevatedButton = e.control

        # 配置校验
        if len(config_instance.get_gallery_path()) == 0:
            self.dialog.content = Text("请先设置图片库地址")
            self.open_dialog(None)
            return

        if len(config_instance.get_feature_path()) == 0:
            self.dialog.content = Text("请先设置特征文件保存地址")
            self.open_dialog(None)
            return

        # 禁用提取按钮
        extract_button.disabled = True
        extract_button.update()

        time_start = time.time()  # 记录提取开始时间
        error_img_list = []  # 错误图片列表
        extract_log_text = ""  # 记录日志
        self.extract_process_bar.current.reset_process_bar()  # 重置进度条

        img_path_list = list(glob.glob(config_instance.get_gallery_path() + "/*"))
        # 过滤掉非图片类型的文件
        img_path_list = [name for name in img_path_list if
                         os.path.splitext(name)[1] in config_instance.get_allow_types()]

        totle_image_count = len(img_path_list)

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

                extract_log_text = "当前提取图片：" + img_path + " --> " + str(cnt) + "\n"
                self.extract_process_bar.current.process_bar.current.value = cnt / totle_image_count
                self.extract_process_bar.current.progress_percentage.current.value = "{}%".format(
                    int(round(cnt / totle_image_count, 2) * 100))
                self.extract_process_bar.current.update()
                cnt += 1
                self.extract_log.current.log_text.current.value = extract_log_text
                self.extract_log.current.update()
            except Exception as e:
                # 图片打开失败
                # traceback.print_exc()
                error_img_list.append(img_path)
                img_path_list.remove(img_path)

        # 存储剩余维度
        sentence_transformer_utils.dump(img_path_list_batch, img_emb_list)

        time_end = time.time()  # 记录结束时间
        time_sum = time_end - time_start
        extract_log_text = "提取结束，提取成功图片: {} 张,  提取失败图片: {} 张, 总耗时: {} 秒\n".format(
            len(img_path_list), len(error_img_list), time_sum)

        if error_img_list:
            extract_log_text += "提取失败图片:\n"
            for path in error_img_list:
                extract_log_text += path + "\n"

        self.extract_log.current.log_text.current.value = extract_log_text
        self.extract_log.current.update()

        # 开启提取按钮
        extract_button.disabled = False
        extract_button.update()

    # 打开提示对话框
    def open_dialog(self, e):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    # 关闭提示对话框
    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()

    # 搜索图片
    def search_image(self, query):
        if len(query) == 0:
            self.dialog.content = Text("请先选择查询图片")
            self.open_dialog(None)
            return
        if not os.path.exists(query):
            self.dialog.content = Text("不存在对应的文件路径")
            self.open_dialog(None)
            return
        try:
            similar_img_list = sentence_transformer_utils.search(query)
        except NoFeaturePathException:
            self.dialog.content = Text("请先设置特征文件保存地址")
            self.open_dialog(None)
            return
        except NoFeatureFileException:
            self.dialog.content = Text("没有找到特征文件")
            self.open_dialog(None)
            return
        except Exception as e:
            # traceback.print_exc()
            self.dialog.content = Text("未知错误")
            self.open_dialog(None)
            return

        #  展示图片
        self.img_list.current.show_result_image(similar_img_list)
