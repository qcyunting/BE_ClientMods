# -*- coding: utf-8 -*-
"""
Created on 2025-11-03
服务端系统
"""
from .utils import *


class Main(BaseServer):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)

    @Listen()
    def OnPlayerActionServerEvent(self, args):
        pid = args["playerId"]
        #self.NotifyToClient(pid, "openDressingRoom", data)
        #self.NotifyToClient(pid, "setText", {"item_id": "text", "text": "测试设置文本"})
        #self.NotifyToClient(pid, "setTextColor", {"item_id": "text", "color": [1, 1, 1]})
        #self.NotifyToClient(pid, "setBackground", {"item_id": "text", "background": "textures/netease/common/image/default"})
        #self.NotifyToClient(pid, "setImage", {"item_id": "image", "texture": "textures/ui/Add-Ons_8x8"})
        #self.NotifyToClient(pid, "setImageColor", {"item_id": "image", "color": [0, 1, 0]})

    @Listen(event_type=Listen.client)
    def UiInitFinished(self, args):
        pid = args["__id__"]
        print "服务端设置是否是测试版游戏"
        self.NotifyToClient(pid, "setTestServer", {"is_test_server": True})
