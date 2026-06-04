# -*- coding: utf-8 -*-
"""
Created on 2025-11-03
服务端系统
"""
from .utils import *


class Main(BaseServer):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.player_uid = {}

    @Listen()
    def OnPlayerActionServerEvent(self, args):
        pid = args["playerId"]
        #self.NotifyToClient(pid, "openDressingRoom", data)
        #self.NotifyToClient(pid, "setText", {"item_id": "text", "text": "测试设置文本"})
        #self.NotifyToClient(pid, "setTextColor", {"item_id": "text", "color": [1, 1, 1]})
        #self.NotifyToClient(pid, "setBackground", {"item_id": "text", "background": "textures/netease/common/image/default"})
        #self.NotifyToClient(pid, "setImage", {"item_id": "image", "texture": "textures/ui/Add-Ons_8x8"})
        #self.NotifyToClient(pid, "setImageColor", {"item_id": "image", "color": [0, 1, 0]})

    @Listen()
    def ServerChatEvent(self, args):
        pid = args["playerId"]
        message = args["message"]
        self.NotifyToMultiClients(serverApi.GetPlayerList(), "SendMessage", {"message": message, "user_uid": str(self.player_uid.get(pid, -1))})  # 获取其他玩家
        try:
            uid = int(message)
            if uid >= 2147483647:
                self.NotifyToClient(pid, "SetLocalUID", {"local_id": uid})
                self.player_uid[pid] = uid
            # self.NotifyToClient(pid, "GetUserToken", {"url": "/user-detail/query/other", "params": {'entity_id': (str(2147624142))}}) # 获取自己的信息
            # self.NotifyToClient(pid, "GetUserToken", {"url": "/user-allfriends", "params": {"with_game_state": True, "with_dynamic_head_img": 1}}) # 获取好友
            self.NotifyToClient(pid, "GetUserToken", {"url": "/pe-game/query/check_apollo", "params": {'item_id': uid}}) # 获取好友
        except:
            return

    @Listen(event_type=Listen.client)
    def GetUserToken(self, args):
        token = args["user_token"]
        print "user_token:", token

    @Listen(event_type=Listen.client)
    def UiInitFinished(self, args):
        pid = args["__id__"]
        self.NotifyToClient(pid, "SetTestServer", {"is_test_server": True})
        for uid in ["2147624142", "2147636691", "2147590418"]:
            self.NotifyToClient(pid, "AddPlayer", {"uid": uid, "pid": uid})
