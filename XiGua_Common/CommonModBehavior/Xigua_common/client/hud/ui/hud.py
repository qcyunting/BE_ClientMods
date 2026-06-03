# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
from .danmaku_utils import DanmakuUtils
from .lifecycle_utils import LifecycleUtils
from .metrics_utils import MetricsUtils
from .scoreboard_utils import ScoreboardUtils
from .top_bar_utils import TopBarUtils
from .watermark_utils import WatermarkUtils
import time
import random


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
        self.scoreboard_text_dict = dict()
        self.NewPingValue = -1
        self.ping_value = ""
        self.all_player_ping = dict()
        self.CPS_left_click_set = []
        self.CPS_right_click_set = []
        self.player_info_visible = False
        self.DanmakuCache = {1: 0, 2: 0, 3: 0}
        # 弹幕轨道配置
        self.font_height = 15
        self.top_margin = 20
        self.track_count = 5
        self.track_offset_range = 2

        self.health_max = 20
        self.health_now = 20
        self.hunger_max = 20
        self.hunger_now = 20
        self.armor_max = 20
        self.armor_now = 0

        self.top_bar_dict = {}
        self.top_bar_control = None

        self.is_test_server = False
        self.child = None  # type: ScreenNode
        self.DanmakuPanel = None

        self.perspective = 0

        # 工具类实例
        self.danmaku_utils = DanmakuUtils(self)
        self.lifecycle_utils = LifecycleUtils(self)
        self.metrics_utils = MetricsUtils(self)
        self.scoreboard_utils = ScoreboardUtils(self)
        self.top_bar_utils = TopBarUtils(self)
        self.watermark_utils = WatermarkUtils(self)

    # ==================== 生命周期 ====================
    def OnCreate(self):
        self.lifecycle_utils.on_create()

    def OnDestroy(self):
        self.lifecycle_utils.on_destroy()

    # ==================== 水印 ====================
    @Listen(event_type=Listen.server)
    def setTestServer(self, args):
        self.watermark_utils.set_test_server(args)

    # ==================== 顶栏 ====================
    @Listen(event_type=Listen.server)
    def initTopBar(self, args):
        self.top_bar_utils.init_top_bar(args)

    @Listen(event_type=Listen.server)
    def updateTopBar(self, args):
        self.top_bar_utils.update_top_bar(args)

    @Listen(event_type=Listen.server)
    def setText(self, args):
        self.top_bar_utils.set_text(args)

    @Listen(event_type=Listen.server)
    def setTextColor(self, args):
        self.top_bar_utils.set_text_color(args)

    @Listen(event_type=Listen.server)
    def setBackground(self, args):
        self.top_bar_utils.set_background(args)

    @Listen(event_type=Listen.server)
    def setImage(self, args):
        self.top_bar_utils.set_image(args)

    @Listen(event_type=Listen.server)
    def setImageColor(self, args):
        self.top_bar_utils.set_image_color(args)

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#perspective_0_button")
    def on_perspective_0_button(self):
        return self.perspective == 2

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#perspective_1_button")
    def on_perspective_1_button(self):
        return self.perspective == 0

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#perspective_2_button")
    def on_perspective_2_button(self):
        return self.perspective == 1

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#hud_button_click")
    def OnButtonClick(self, args):
        parts = args["ButtonPath"].split("/")
        result = parts[-2]
        if result == "pause_button":
            clientApi.OpenPauseGui()
        elif result == "chat_button":
            clientApi.OpenChatGui()
            #clientApi.PushScreen(modName, "xg_chat")
        elif result == "perspective_0_button":
            CF.CreatePlayerView(playerId).SetPerspective(0)
            self.perspective = 0
        elif result == "perspective_1_button":
            CF.CreatePlayerView(playerId).SetPerspective(1)
            self.perspective = 1
        elif result == "perspective_2_button":
            CF.CreatePlayerView(playerId).SetPerspective(2)
            self.perspective = 2

    # ==================== 指标 (Metrics) ====================
    @Listen("LeftClickBeforeClientEvent")
    def OnLeftClickBeforeClientEvent(self, args):
        self.metrics_utils.on_left_click(args)

    @Listen("TapBeforeClientEvent")
    def OnTapBeforeClientEvent(self, args):
        self.metrics_utils.on_tap(args)

    @Listen("RightClickBeforeClientEvent")
    def OnRightClickBeforeClientEvent(self, args):
        self.metrics_utils.on_right_click(args)

    @Listen(event_name="pong", event_type=Listen.server)
    def OnPingValueChange(self, args):
        self.metrics_utils.on_ping_change(args)

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#player_info.visible")
    def return_player_info_visible(self):
        return self.player_info_visible

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.keyboard_and_mouse")
    def return_input_mode_keyboard_and_mouse(self):
        return self.metrics_utils.get_input_mode_kb_mouse()

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.touch")
    def return_input_mode_touch(self):
        return self.metrics_utils.get_input_mode_touch()

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.controller")
    def return_input_mode_controller(self):
        return self.metrics_utils.get_input_mode_controller()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#game_info.text")
    def return_game_info_text(self):
        return self.system.game_info_text

    @ViewBinder.binding(ViewBinder.BF_BindString, "#FPS_value")
    def return_FPS_value(self):
        return self.metrics_utils.get_fps()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#CPS_value")
    def return_CPS_value(self):
        return self.metrics_utils.get_cps()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#ping_value")
    def return_ping_value(self):
        return self.metrics_utils.get_ping()

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#health_percentage")
    def health_percentage(self):
        return self.metrics_utils.get_health_percentage()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#health_percentage_text")
    def health_percentage_text(self):
        return self.metrics_utils.get_health_text()

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#hunger_percentage")
    def hunger_percentage(self):
        return self.metrics_utils.get_hunger_percentage()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#hunger_percentage_text")
    def hunger_percentage_text(self):
        return self.metrics_utils.get_hunger_text()

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#armor_percentage")
    def armor_percentage(self):
        return self.metrics_utils.get_armor_percentage()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#armor_percentage_text")
    def armor_percentage_text(self):
        return self.metrics_utils.get_armor_text()

    # ==================== 弹幕 ====================
    @Listen("NewDanmaku", "server")
    def OnNewDanmaku(self, args):
        self.danmaku_utils.on_new_danmaku(args)

    # ==================== 计分板 ====================
    @Listen(event_type=Listen.server)
    def SetScoreboard(self, args):
        self.scoreboard_utils.set_scoreboard(args)

    @Listen(event_type=Listen.server)
    def AddScoreboardText(self, args):
        self.scoreboard_utils.add_scoreboard_text(args)

    @Listen(event_type=Listen.server)
    def RemoveScoreboardText(self, args):
        self.scoreboard_utils.remove_scoreboard_text(args)

    @Listen(event_type=Listen.server)
    def SetScoreboardText(self, args):
        self.scoreboard_utils.set_scoreboard_text(args)

    @Listen(event_type=Listen.server)
    def SetScoreboardTitle(self, args):
        self.scoreboard_utils.set_scoreboard_title(args)

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#scoreboard_panel.visible")
    def return_scoreboard_visible(self):
        return self.scoreboard_utils.get_visible()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#scoreboard_panel.title")
    def return_scoreboard_title(self):
        return self.scoreboard_utils.get_title()

    @ViewBinder.binding(ViewBinder.BF_BindInt, "#scoreboard_panel.item_count")
    def return_scoreboard_item_count(self):
        return self.scoreboard_utils.get_item_count()

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "scoreboard_collection", "#scoreboard_panel.text")
    def return_scoreboard_text(self, index):
        return self.scoreboard_utils.get_text(index)
