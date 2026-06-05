# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
import math

path = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

path_mapname_padding = "/pause_screen_main_panels/info_panel/info_panel_list/player_list_scrolling_panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content/normal_list"


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
        self.input_panel_visible_value = False
        self.GaussianBlur = False

    def OnCreate(self):
        self.screen = self.GetScreenNode()
        self.ui_create = True

        # 隐藏原版全部UI
        self.screen.GetBaseUIControl(
            path + "/pause_screen_main_panels/menu"
        ).asStackPanel().SetVisible(False)
        self.screen.GetBaseUIControl(
            path + "/pause_screen_main_panels/info_panel"
        ).asImage().SetAlpha(0)
        self.screen.GetBaseUIControl(
            path + "/pause_screen_main_panels/info_panel/info_panel_background"
        ).asImage().SetVisible(False)

        self.screen.GetBaseUIControl(
            path + "/pause_screen_main_panels/info_panel/info_panel_list"
        ).asStackPanel().SetVisible(False)


        # # 处理地图名字滚动条
        # for i in range(2,6):
        #     print "[SUC] asInputPanel",path + path_mapname_padding + "/vertical_padding_{}".format(i)
        #     print self.screen.GetBaseUIControl(
        #         path + path_mapname_padding + "/vertical_padding_{}".format(i)
        #     ).asStackPanel()

        # 创建自定义按钮文本框和发送按钮
        panel = self.screen.GetBaseUIControl(path)
        self.child = self.screen.CreateChildControl(
            "pause.background", "pause_ui", panel
        )

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def list_button(self, index):
        """
        点击排行榜按钮
        """
        pass
        # clientApi.PushScreen(modName, "list_ui")

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_panel_visible")
    def input_panel_visible(self):
        """
        输入面板可见性绑定
        """
        return self.input_panel_visible_value

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#quit_button_click")
    def quit_button_click(self, args):
        """
        点击退出按钮
        """
        self.input_panel_visible_value = True
        # self.screen.GetBaseUIControl(path + "/pause_ui/input_panel").SetVisible(True)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#close_button_click")
    def close_button_click(self, args):
        """
        点击关闭按钮
        """
        self.input_panel_visible_value = False
        # self.screen.GetBaseUIControl(path + "/pause_ui/input_panel").SetVisible(False)


    def OnDestroy(self):
        """
        @description UI销毁时调用
        """
        self.screen.RemoveChildControl(self.child)
        self.ui_create = False