import os

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
from src.utils import feature_extractor
from src.views.feature.extract_log import ExtractLog
from src.views.feature.feature_bar import FeatureBar
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
                    ExtractLog(ref=self.extract_log, page=self.page, app_layout=self)
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

        # 批量提取
        feature_extractor.fe.extract_batch(config_instance.get_gallery_path(), self.extract_log)

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
    def search_image(self, query_img_path):
        if len(query_img_path) == 0:
            self.dialog.content = Text("请先选择查询图片")
            self.open_dialog(None)
            return
        if not os.path.exists(query_img_path):
            self.dialog.content = Text("不存在对应的文件路径")
            self.open_dialog(None)
            return
        try:
            similar_img_list = feature_extractor.search(query_img_path)
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
