# -*- coding: utf-8 -*-
from ...utils.ui_utils import *


class LifecycleUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def on_create(self):
        self.hud.ui_create = True
        if self.hud.screen is None:
            return

        self.hud.track_base_positions = [
            self.hud.top_margin + (i * self.hud.font_height)
            for i in range(self.hud.track_count)
        ]
        self.hud.track_available_time = [0] * self.hud.track_count
        self.hud.track_available_time_top = [0] * self.hud.track_count

        panel = self.hud.screen.GetBaseUIControl(BP)
        self.hud.child = self.hud.screen.CreateChildControl("xg_hud.root_panel_watermelon", "root_panel_watermelon", panel)
        self.hud.DanmakuPanel = self.hud.screen.GetBaseUIControl(BP + "/root_panel_watermelon/danmaku")

        self.hud.perspective = CF.CreatePlayerView(playerId).GetPerspective()

    def on_destroy(self):
        if getattr(self.hud, "screen", None) is not None and getattr(self.hud, "child", None) is not None:
            self.hud.screen.RemoveChildControl(self.hud.child)
        self.hud.ui_create = False
        self.hud.child = None
        self.hud.DanmakuPanel = None