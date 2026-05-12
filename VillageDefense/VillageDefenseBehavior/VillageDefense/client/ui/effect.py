# -*- coding: utf-8 -*-
import time

from ..utils.ui_utils import *
import tab_button
from .shop_data_tool import ShopDataTool
import uuid
from ..utils import escape


class Effect(BaseCustomScreen):
    def __init__(self, namespace, name, param):
        super(Effect, self).__init__(namespace, name, param)
        self.data = param.get("data", {})
        self.player_coin = self.data.get("player_coin")
        self.is_create = False
        self.shop_content_panel = None

    def Create(self):
        self.shop_content_panel = self.GetBaseUIControl(BP + "/content_panel/content/scrolling_panel").asScrollView().GetScrollViewContentControl()

        self.is_create = True
        self.update_shop_content()

    @Listen(event_type=Listen.server)
    def refreshBuffShop(self, args):
        if self.is_create:
            self.data = args
            self.update_shop_content()

    def update_shop_content(self):
        if self.is_create:
            for effect_name in ["HEALTH_BOOST", "SPEED", "DAMAGE_RESISTANCE", "INCREASE_DAMAGE"]:
                self.set_effect(effect_name)

    def set_effect(self, effect_name):
        rotten_flesh = self.data.get(effect_name, {}).get("rotten_flesh")
        max_rotten_flesh = self.data.get(effect_name, {}).get("max_rotten_flesh")
        level = self.data.get(effect_name, {}).get("level")

        # 设置文本
        text = "当前等级:{}, {}/{}".format(level, rotten_flesh, max_rotten_flesh)
        self.shop_content_panel.GetChildByPath("/" + effect_name + "/name/level").asLabel().SetText(text)

        # 设置进度
        progress = rotten_flesh * 1.0 / max_rotten_flesh
        self.shop_content_panel.GetChildByPath("/" + effect_name + "/progress_bar").asProgressBar().SetValue(progress)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#HEALTH_BOOST")
    def effect_button_HEALTH_BOOST(self, args):
        self.NotifyToServer("buffButtonClick", {"button": "HEALTH_BOOST"})

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#SPEED")
    def effect_button_SPEED(self, args):
        self.NotifyToServer("buffButtonClick", {"button": "SPEED"})

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#DAMAGE_RESISTANCE")
    def effect_button_DAMAGE_RESISTANCE(self, args):
        self.NotifyToServer("buffButtonClick", {"button": "RESISTANCE"})

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#INCREASE_DAMAGE")
    def effect_button_INCREASE_DAMAGE(self, args):
        self.NotifyToServer("buffButtonClick", {"button": "INCREASE_DAMAGE"})

    def Destroy(self):
        self.is_create = False
