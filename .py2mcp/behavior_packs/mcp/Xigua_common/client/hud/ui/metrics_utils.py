# -*- coding: utf-8 -*-
import time
from ...utils.ui_utils import *


class MetricsUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def on_left_click(self, args):
        self.hud.CPS_left_click_set.append(time.time())

    def on_tap(self, args):
        self.hud.CPS_left_click_set.append(time.time())

    def on_right_click(self, args):
        self.hud.CPS_right_click_set.append(time.time())

    def on_ping_change(self, args):
        self.hud.all_player_ping = args
        for pid, info in args.items():
            if pid == self.hud.local_id:
                self.hud.NewPingValue = info.get("value")

    def get_input_mode_kb_mouse(self):
        return CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 0

    def get_input_mode_touch(self):
        return CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 1

    def get_input_mode_controller(self):
        return CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 2

    def get_fps(self):
        return "FPS:{}".format(int(gameComp.GetFps()))

    def get_cps(self):
        now = time.time()
        self.hud.CPS_left_click_set = [t for t in self.hud.CPS_left_click_set if now - t <= 1]
        self.hud.CPS_right_click_set = [t for t in self.hud.CPS_right_click_set if now - t <= 1]
        left_cps = len(self.hud.CPS_left_click_set)
        right_cps = len(self.hud.CPS_right_click_set)
        if left_cps == 0 and right_cps == 0:
            return ""
        elif left_cps == 0:
            return "CPS:0|{}".format(right_cps)
        elif right_cps == 0:
            return "CPS:{}".format(left_cps)
        else:
            return "CPS:{}|{}".format(left_cps, right_cps)

    def get_ping(self):
        PING_ICONS = {
            100: {"color": "§a"},
            200: {"color": "§e"},
            300: {"color": "§6"},
            400: {"color": "§c"}
        }
        ping_list = sorted(PING_ICONS.keys())
        if self.hud.NewPingValue == -1:
            return ""
        value = max(self.hud.NewPingValue, 20)
        for ping in ping_list:
            if value <= ping:
                return " ping {}{} §fms".format(PING_ICONS[ping]["color"], value)
        return " ping§c{} §fms".format(value)

    def get_health_percentage(self):
        self.hud.health_max = attrComp(playerId).GetAttrMaxValue(MC_Enum.AttrType.HEALTH)
        self.hud.health_now = attrComp(playerId).GetAttrValue(MC_Enum.AttrType.HEALTH)
        return self.hud.health_now / self.hud.health_max

    def get_health_text(self):
        return str(int(self.hud.health_now)) + "/" + str(int(self.hud.health_max))

    def get_hunger_percentage(self):
        self.hud.hunger_max = attrComp(playerId).GetAttrMaxValue(MC_Enum.AttrType.HUNGER)
        self.hud.hunger_now = attrComp(playerId).GetAttrValue(MC_Enum.AttrType.HUNGER)
        return self.hud.hunger_now / self.hud.hunger_max

    def get_hunger_text(self):
        return str(int(self.hud.hunger_now)) + "/" + str(int(self.hud.hunger_max))

    def get_armor_percentage(self):
        self.hud.armor_max = 20
        self.hud.armor_now = attrComp(playerId).GetAttrValue(MC_Enum.AttrType.ARMOR)
        if self.hud.armor_now < 0:
            self.hud.armor_now = 0
        return max(0, min(self.hud.armor_now / float(self.hud.armor_max), 1))

    def get_armor_text(self):
        return str(int(self.hud.armor_now)) + "/" + str(int(self.hud.armor_max))
