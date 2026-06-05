# -*- coding: utf-8 -*-
from ...utils.ui_utils import *


class ScoreboardUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def set_scoreboard(self, args):
        self.hud.scoreboard_text_dict = dict(args)

    def add_scoreboard_text(self, args):
        for name, text in args.items():
            order = list(self.hud.scoreboard_text_dict.get("order", ()))
            order.append(name)
            text_dict = self.hud.scoreboard_text_dict.setdefault("text_dict", {})
            text_dict[name] = text
            self.hud.scoreboard_text_dict["order"] = tuple(order)
            self.hud.scoreboard_text_dict["text_dict"] = text_dict

    def remove_scoreboard_text(self, args):
        for name in args.values():
            order = self.hud.scoreboard_text_dict.get("order", ())
            text_dict = self.hud.scoreboard_text_dict.get("text_dict", {})
            if name in order:
                order = list(order)
                order.remove(name)
                self.hud.scoreboard_text_dict["order"] = tuple(order)
            if name in text_dict:
                text_dict.pop(name)
                self.hud.scoreboard_text_dict["text_dict"] = text_dict

    def set_scoreboard_text(self, args):
        name, text = args["name"], args["text"]
        text_dict = self.hud.scoreboard_text_dict.setdefault("text_dict", {})
        text_dict[name] = text
        self.hud.scoreboard_text_dict["text_dict"] = text_dict

    def set_scoreboard_title(self, args):
        self.hud.scoreboard_text_dict["title"] = args["title"]

    def get_visible(self):
        return bool(self.hud.scoreboard_text_dict.get("order"))

    def get_title(self):
        text = self.hud.scoreboard_text_dict.get("title", "")
        if self.hud.child:
            c = self.hud.child.GetChildByPath("/scoreboard/title_image/image")
            image = scoreboard_title_image_dict.get(text, "")
            if image:
                c.SetVisible(True)
                c.asImage().SetSprite("textures/sfxs/" + image)
                return ""
            c.SetVisible(False)
            return text
        return text

    def get_item_count(self):
        return len(self.hud.scoreboard_text_dict.get("order", ()))

    def get_text(self, index):
        try:
            item_id = self.hud.scoreboard_text_dict.get("order", ())[index]
            return self.hud.scoreboard_text_dict.get("text_dict", {}).get(item_id, "无")
        except IndexError:
            return "溢出"
        except Exception as e:
            logger.error(e)
            return "未知错误"