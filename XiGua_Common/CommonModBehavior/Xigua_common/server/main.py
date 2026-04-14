# -*- coding: utf-8 -*-
"""
Created on 2025-11-03
服务端系统
"""
from utils import *


class Main(BaseServer):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)

    @Listen()
    def PlayerEatFoodServerEvent(self, args):
        pid = args["playerId"]
        data = {
            "text": {
                "type": "text",
                "background": "textures/ui/hud_tip_text_background",
                "color": [1, 0, 0],
                "text": "测试红色文本颜色"
            },
            "image": {
                "type": "image",
                "background": "textures/ui/hud_tip_text_background",
                "text": "文本",
                "color": [1, 1, 1],
                "texture": "textures/netease/common/image/default"
            },
            "web_image": {
                "type": "image",
                "text": "文本",
                "color": [1, 1, 1],
                "texture": "https://imgservices-1252317822.image.myqcloud.com/image/011820220132828/ac5e77f3.png"
            },
            "progress_bar": {
                "type": "progress_bar",
                "color": [1, 1, 1],
                "bar_texture": "textures/ui/image",
                "bar_background": "textures/ui/image"
            }
        }
        self.NotifyToClient(pid, "initTopBar", data)
        #self.NotifyToClient(pid, "setText", {"item_id": "text", "text": "测试设置文本"})
        #self.NotifyToClient(pid, "setTextColor", {"item_id": "text", "color": [1, 1, 1]})
        #self.NotifyToClient(pid, "setBackground", {"item_id": "text", "background": "textures/netease/common/image/default"})
        #self.NotifyToClient(pid, "setImage", {"item_id": "image", "texture": "textures/ui/Add-Ons_8x8"})
        #self.NotifyToClient(pid, "setImageColor", {"item_id": "image", "color": [0, 1, 0]})
