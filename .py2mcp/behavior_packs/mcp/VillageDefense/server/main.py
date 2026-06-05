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
        self.NotifyToClient(pid, "openBuffShop", {'DAMAGE_RESISTANCE': {'slot': 3, 'max_rotten_flesh': 128, 'level': 0, 'rotten_flesh': 0}, 'SPEED': {'slot': 1, 'max_rotten_flesh': 128, 'level': 0, 'rotten_flesh': 0}, 'HEALTH_BOOST': {'slot': 0, 'max_rotten_flesh': 32, 'level': 0, 'rotten_flesh': 0}, 'player_coin': 85, 'INCREASE_DAMAGE': {'slot': 2, 'max_rotten_flesh': 512, 'level': 0, 'rotten_flesh': 0}})

    @Listen(event_type=Listen.client)
    def UiInitFinished(self, args):
        pid = args["__id__"]

    @Listen(event_type=Listen.client)
    def buffButtonClick(self, args):
        pid = args["__id__"]
        print args