import os
import threading
import traceback

from flet import (
    Page,
    Row,
    Text,
)
from flet_core import Column, MainAxisAlignment, Ref, Container, padding, CrossAxisAlignment, AlertDialog, TextButton, \
    ControlEvent, ElevatedButton, Stack, ProgressBar

from src.config.config import config_instance
from src.exception.no_feature_file_exception import NoFeatureFileException
from src.exception.no_feature_path_exception import NoFeaturePathException
from src.services.feature_service import run_extraction
from src.services.search_service import run_search, SearchError
from src.utils.dialog_mixin import DialogMixin
from src.views.feature.extract_log import ExtractLog
from src.views.feature.feature_bar import FeatureBar
from src.views.feature.process_bar import ExtractProcessBar
from src.views.search.img_list import ImgList
from src.views.search.search_bar import SearchBar
from src.views.setting.setting_view import SettingView
from src.views.sidebar import Sidebar


class AppLayout(Row, DialogMixin):
    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.sidebar = Sidebar(page, self)
        self.expand = True
        self.search_bar = Ref[SearchBar]()
        self.img_list = Ref[ImgList]()
        self.search_loading = Ref[ProgressBar]()
        self.feature_bar = Ref[FeatureBar]()
        self.extract_log = Ref[ExtractLog]()
        self.extract_process_bar = Ref[ExtractProcessBar]()

        # 搜索视图
        self.search_view = Container(
            expand=True,
            padding=padding.only(50, 50, 50, 50),
            content=Column(
                # 垂直居中对齐
                alignment=MainAxisAlignment.START,
                # 水平居中对齐
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    # 搜索栏
                    SearchBar(ref=self.search_bar, page=self.page, app_layout=self),
                    # 搜索加载指示器
                    ProgressBar(
                        ref=self.search_loading,
                        visible=False,
                        height=4,
                    ),
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

        # 后台提取任务取消标志
        self._extraction_cancel_event = threading.Event()
        self._extraction_running = False

        # 提示对话框
        self._init_dialog()

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

    # 提取特征按钮点击触发函数
    def extract_feature(self, e: ControlEvent):
        extract_button: ElevatedButton = e.control

        if len(config_instance.get_gallery_path()) == 0:
            self._show_dialog("请先设置图片库地址")
            return

        if len(config_instance.get_feature_path()) == 0:
            self._show_dialog("请先设置特征文件保存地址")
            return

        # 禁用提取按钮，显示取消按钮
        extract_button.visible = False
        extract_button.update()
        self.feature_bar.current.cancel_extract_button.current.visible = True
        self.feature_bar.current.cancel_extract_button.current.update()
        self.extract_process_bar.current.reset_process_bar()
        self._extraction_cancel_event.clear()
        self._extraction_running = True

        def on_progress(current, total, current_path):
            if self._extraction_cancel_event.is_set():
                return
            self.extract_process_bar.current.process_bar.current.value = current / total
            self.extract_process_bar.current.progress_percentage.current.value = "{}%".format(
                int(round(current / total, 2) * 100))
            self.extract_process_bar.current.update()
            self.extract_log.current.log_text.current.value = "当前提取图片：" + current_path + " --> " + str(current) + "\n"
            self.extract_log.current.update()
            self.page.update()

        def on_complete(success_count, error_count, time_sum, error_img_list, cancelled=False):
            if cancelled:
                log_text = "提取已取消，成功提取图片: {} 张,  失败图片: {} 张, 耗时: {} 秒\n".format(
                    success_count, error_count, time_sum)
            else:
                log_text = "提取结束，提取成功图片: {} 张,  提取失败图片: {} 张, 总耗时: {} 秒\n".format(
                    success_count, error_count, time_sum)
            if error_img_list:
                log_text += "提取失败图片:\n"
                for item in error_img_list:
                    if isinstance(item, tuple):
                        log_text += "{} 原因: {}\n".format(item[0], item[1])
                    else:
                        log_text += item + "\n"
            self.extract_log.current.log_text.current.value = log_text
            self.extract_log.current.update()
            extract_button.visible = True
            extract_button.update()
            self.feature_bar.current.cancel_extract_button.current.visible = False
            self.feature_bar.current.cancel_extract_button.current.update()
            self._extraction_running = False
            self.page.update()

        def _run():
            run_extraction(on_progress, on_complete, self._extraction_cancel_event)

        threading.Thread(target=_run, daemon=True).start()

    def cancel_extraction(self, e: ControlEvent):
        self._extraction_cancel_event.set()
        cancel_button: ElevatedButton = e.control
        cancel_button.disabled = True
        cancel_button.text = "取消中..."
        cancel_button.update()

    # 搜索图片
    def search_image(self, query, on_complete=None):
        self.search_loading.current.visible = True
        self.search_loading.current.update()

        def _run():
            try:
                similar_img_list = run_search(query)
            except SearchError as e:
                self._show_dialog(e.message)
                self.search_loading.current.visible = False
                self.search_loading.current.update()
                self.page.update()
                if on_complete:
                    on_complete(False)
                return
            self.img_list.current.show_result_image(similar_img_list)
            self.search_loading.current.visible = False
            self.search_loading.current.update()
            self.page.update()
            if on_complete:
                on_complete(True)

        threading.Thread(target=_run, daemon=True).start()
