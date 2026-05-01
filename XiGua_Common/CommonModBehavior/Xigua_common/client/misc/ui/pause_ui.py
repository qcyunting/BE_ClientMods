# -*- coding: utf-8 -*-
from ...utils.ui_utils import *

CustomUIScreenProxy = clientApi.GetUIScreenProxyCls()

path = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

path_mapname_padding = "/pause_screen_main_panels/info_panel/info_panel_list/player_list_scrolling_panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content/normal_list"


class Main(CustomUIScreenProxy):
    def __init__(self, screenName, screenNode):
        CustomUIScreenProxy.__init__(self, screenName, screenNode)
        self.ui_create = False
        self.input_panel_visible_value = False
        self.GaussianBlur = False

    def OnCreate(self):
        self.screen = self.GetScreenNode()
        self.ui_create = True

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

        panel = self.screen.GetBaseUIControl(path)
        self.child = self.screen.CreateChildControl(
            "pause.background", "pause_ui", panel
        )

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def list_button(self, index):
        """
        点击排行列表按钮
        """
        pass

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

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#close_button_click")
    def close_button_click(self, args):
        """
        点击关闭按钮
        """
        self.input_panel_visible_value = False

    def OnDestroy(self):
        """
        @description UI销毁时调用
        """
        self.screen.RemoveChildControl(self.child)
        self.ui_create = False
