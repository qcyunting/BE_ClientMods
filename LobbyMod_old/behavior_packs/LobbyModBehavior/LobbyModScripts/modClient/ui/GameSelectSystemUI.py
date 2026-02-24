# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from LobbyModScripts.modCommon.modConfig import ModName

class Main(clientApi.GetScreenNodeCls()):

    def __init__(self, namespace, name, param):
        super(Main, self).__init__(namespace, name, param)
        self.clientSystem = clientApi.GetSystem(ModName, "gameselect")
        self.levelId = clientApi.GetLevelId()

    def Create(self):
        # 关闭按钮
        btn_close = self.GetBaseUIControl("/image/back").asButton()
        btn_close.AddTouchEventParams()
        btn_close.SetButtonTouchDownCallback(self.closeui)

        # 饥饿游戏
        btn_hunger = self.GetBaseUIControl("/image/card/card_hunger").asButton()
        btn_hunger.AddTouchEventParams({"game_type":"hungergame"})
        btn_hunger.SetButtonTouchDownCallback(self.game_select_post)

        # 猎人游戏
        btn_hunter = self.GetBaseUIControl("/image/card/card_hunter").asButton()
        btn_hunter.AddTouchEventParams({"game_type":"huntergame"})
        btn_hunter.SetButtonTouchDownCallback(self.game_select_post)

        # 超能激战
        btn_hyperclash = self.GetBaseUIControl("/image/card/card_hyperclash").asButton()
        btn_hyperclash.AddTouchEventParams({"game_type":"hyperclash"})
        btn_hyperclash.SetButtonTouchDownCallback(self.game_select_post)

        # 村庄守卫战
        btn_villager = self.GetBaseUIControl("/image/card/card_villager").asButton()
        btn_villager.AddTouchEventParams({"game_type":"villager"})
        btn_villager.SetButtonTouchDownCallback(self.game_select_post)

        # 生存服
        btn_survival = self.GetBaseUIControl("/image/card/card_survival").asButton()
        btn_survival.AddTouchEventParams({"game_type":"survival"})
        btn_survival.SetButtonTouchDownCallback(self.game_select_post)
    
    def game_select_post(self,args):
        # 游戏选择器向服务端发送请求
        AddTouchEventParams = args["AddTouchEventParams"]
        if AddTouchEventParams.get("game_type"):
            # 与服务端通信
            self.clientSystem.NotifyToServer('gameSelected', AddTouchEventParams)

            # 弹出切服提示
            comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(self.levelId)
            comp.SetLeftCornerNotify("§l§e[系统提示] 正在切服中...")

            # 关闭ui
            clientApi.PopScreen()

    def closeui(self,args):
        # 关闭ui
        clientApi.PopScreen()

    def _showMsg(self, args):
        self.clientSystem.NotifyToServer('requestMsg', {})
