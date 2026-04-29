# coding=utf-8
"""
Created on 2025-11-03
游戏选择器模块
这里主要 提供一个游戏选择器模块
接口：
- 
"""
from ..utils import *
from ..module_registry import Module

@Module("GameSelect")
class GameSelectModule(BaseState):
    def __init__(self, namespace, systemName):
        super(GameSelectModule, self).__init__(namespace, systemName)

        self.ui_gameselect = None

    def on_enable(self):
        print "启用GameSelect"
        self.listen_client("UiInitFinished", self.UiInitFinished)

        self.ListenForEvent(modName, "main", "OpenGameMenu", self, self.OpenGameMenu)

        clientApi.RegisterUI(modName, 'gameselect', "{}.ui.GameSelect.Main".format(modName),"gameselect.main")

    def on_disable(self):
        print "禁用GameSelect"

    def listen_client(self, event, func):
        self.ListenForEvent("Minecraft", "Engine", event, self, func)

    def UiInitFinished(self,args):
        print("UiInitFinished")
        clientApi.RegisterUI(modName, 'gameselect', "{}.ui.GameSelect.Main".format(modName),"gameselect.main")
        print "ui_gameselect_enable"

    def OpenGameMenu(self,args):
        # 打开游戏选择器
        print "OpenGameMenu",args
        if not args:
            comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(LevelId)
            comp.SetLeftCornerNotify("[Error] 菜单数据异常")
            print ("[Error] 菜单数据异常")
            return
        print "打开UI", clientApi.PushScreen(modName,"gameselect",{"isHud": 1, 'data': args, 'client': self})

    def send_to_server(self,event,args):
        self.NotifyToServer(event,args)

