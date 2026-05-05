# -*- coding: utf-8 -*-
from ...utils.ui_utils import *


class TopBarUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def init_top_bar(self, args):
        self.hud.top_bar_dict = args
        top_bar = self.hud.screen.GetBaseUIControl(BP + "/root_panel_watermelon/top_bar")
        if top_bar:
            self.hud.screen.RemoveChildControl(top_bar)
        self.hud.top_bar_control = self.hud.screen.CreateChildControl("xg_hud.top_bar", "top_bar", self.hud.child)

        sorted_items = sorted(self.hud.top_bar_dict.items(), key=lambda x: x[1].get("index", 0))
        for item_id, control in sorted_items:
            c_type = control.get("type", "text")
            def_name = "xg_hud.top_bar_" + c_type
            child = self.hud.screen.CreateChildControl(def_name, item_id, self.hud.top_bar_control)
            self._set_control(control, child)
            self.hud.top_bar_dict[item_id]["child"] = child

    def update_top_bar(self, args):
        for item_id, control in args.items():
            item = self.hud.top_bar_dict.get(item_id, dict()).get("child")
            if item:
                self._set_control(control, item)

    def _set_control(self, control, child):
        _type = control.get("type", "text")
        if _type == "text":
            if control.get("text"):
                child.GetChildByPath("/image/text").asLabel().SetText(control.get("text"))
            if control.get("background"):
                child.GetChildByPath("/image").asImage().SetSprite(control.get("background"))
            if control.get("color"):
                child.GetChildByPath("/image/text").asLabel().SetTextColor(control.get("color"))
        elif _type == "image":
            if control.get("text"):
                child.GetChildByPath("/image/text").asLabel().SetText(control.get("text"))
            if control.get("background"):
                child.GetChildByPath("/image").asImage().SetSprite(control.get("background"))
            if control.get("texture"):
                child.GetChildByPath("/image/image").asImage().SetSprite(control.get("texture"))
            if control.get("color"):
                child.GetChildByPath("/image/image").asImage().SetSpriteColor(control.get("color"))
        elif _type == "progress_bar":
            pass

    def set_text(self, args):
        control_id = args["item_id"]
        text = args["text"]
        control = self.hud.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.hud.top_bar_dict[control_id]["text"] = text
            control.GetChildByPath("/image/text").asLabel().SetText(text)

    def set_text_color(self, args):
        control_id = args["item_id"]
        color = args["color"]
        control = self.hud.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.hud.top_bar_dict[control_id]["color"] = color
            control.GetChildByPath("/image/text").asLabel().SetTextColor(color)

    def set_background(self, args):
        control_id = args["item_id"]
        background = args["background"]
        control = self.hud.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.hud.top_bar_dict[control_id]["background"] = background
            control.GetChildByPath("/image").asImage().SetSprite(background)

    def set_image(self, args):
        control_id = args["item_id"]
        texture = args["texture"]
        control = self.hud.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.hud.top_bar_dict[control_id]["texture"] = texture
            control.GetChildByPath("/image/image").asImage().SetSprite(texture)

    def set_image_color(self, args):
        control_id = args["item_id"]
        color = tuple(args["color"])
        control = self.hud.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.hud.top_bar_dict[control_id]["color"] = color
            control.GetChildByPath("/image/image").asImage().SetSpriteColor(color)