# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
import time
import random


class DanmakuUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def on_new_danmaku(self, args):
        content = args["content"]
        danmaku_type = args.get("danmaku_type", "scroll")
        background = args.get("background")
        if danmaku_type == "SCROLL":
            self._create_scroll_danmaku(content, background)
        elif danmaku_type == "UP":
            self._create_up_danmaku(content, background)

    def _create_scroll_danmaku(self, content, background):
        if not getattr(self.hud, "DanmakuPanel", None):
            return
        child_name = "danmaku_text_{}".format(time.time())
        child = self.hud.screen.CreateChildControl("xg_hud.danmaku_text", child_name, self.hud.DanmakuPanel)
        screen_width, screen_height = gameComp.GetScreenSize()
        size_x = child.GetFullSize("x")["absoluteValue"]
        size_y = self.hud.font_height

        current_time = time.time()
        track_index = min(range(self.hud.track_count), key=lambda i: self.hud.track_available_time[i])

        base_y = self.hud.track_base_positions[track_index]
        random_offset = random.randint(-self.hud.track_offset_range, self.hud.track_offset_range)
        final_y = max(self.hud.top_margin, min(base_y + random_offset, screen_height - size_y))

        speed = random.randint(1, 4) * 0.01 + 0.03
        animation_duration = (screen_width + size_x) * speed
        self.hud.track_available_time[track_index] = current_time + animation_duration

        animation = {
            "namespace": "danmaku",
            "danmaku_text_offset": {
                "anim_type": "offset",
                "duration": animation_duration,
                "from": [screen_width, final_y],
                "to": [0 - size_x, final_y],
                "next": "",
            },
        }
        clientApi.RegisterUIAnimations(animation)

        def callback():
            self.hud.screen.RemoveChildControl(child)

        child.SetAnimEndCallback("danmaku_text_offset", callback)
        child.SetAnimation("offset", "danmaku", "danmaku_text_offset", True)
        if background:
            child.asImage().SetSprite(background)
        text = child.GetChildByPath("/text").asLabel()
        text.SetText(content)

    def _create_up_danmaku(self, content, background):
        if not getattr(self.hud, "DanmakuPanel", None):
            return
        child_name = "danmaku_text_{}".format(time.time())
        child = self.hud.screen.CreateChildControl("xg_hud.danmaku_text", child_name, self.hud.DanmakuPanel)
        track_index = min(range(self.hud.track_count), key=lambda i: self.hud.track_available_time_top[i])
        self.hud.track_available_time_top[track_index] = time.time() + 7

        base_y = self.hud.track_base_positions[track_index]
        screen_width, screen_height = gameComp.GetScreenSize()
        size_x = child.GetFullSize("x")["absoluteValue"]
        base_x = (screen_width / 2) - (size_x / 2)
        if background:
            child.asImage().SetSprite(background)
        text = child.GetChildByPath("/text").asLabel()
        text.SetText(content)
        child.SetPosition((base_x, base_y))

        def callback():
            self.hud.screen.RemoveChildControl(child)

        gameComp.AddTimer(7, callback)