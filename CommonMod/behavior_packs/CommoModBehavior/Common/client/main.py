# -*- coding: utf-8 -*-
from utils import *


NativeScreenManager = clientApi.GetNativeScreenManagerCls()

class Main(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.game_info_text = PlayerName
        self.death_number = 0
        self.kill_number = 0
        self.ui_toptips = None
        self.ui_toptips_args = None
        # self.GaussianBlurValue = 0
        # self.GaussianBlurTimer = None
        Game.AddRepeatedTimer(1, self.ping_timer)
        NativeScreenManager.instance().RegisterScreenProxy("hud.hud_screen", "Common.client.ui.hud_proxys.Main")

    def ping_timer(self):
        self.NotifyToServer("ping_timer", {"ping_value": time.time() * 1000})

    
    @Listen(event_type=Listen.server)
    def startMod(self, args):
        print("startMod",args)
        self.BroadcastEvent("StartMod", args["all_mod"])

    @Listen("SetToptips","server")
    def SetToptips(self,args):
        print("SetToptips",args)
        tip_time = args.get("tip_time",3)
        tip_close = args.get("tip_close",None)
        tip_sound = args.get("tip_sound",True)

        def tip_close_f():
            if self.ui_toptips:
                self.ui_toptips.SetRemove()
                self.ui_toptips = None

        if tip_close:
            # 关闭ui
            tip_close_f()
            return

        if not self.ui_toptips:
            # 判断是否已经创建
            self.ui_toptips_args = args
            self.ui_toptips = clientApi.CreateUI(modName, "cy_toptips", {"isHud": 1, 'data': {}, 'client': self})
            if tip_sound:
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
                comp.PlayCustomUIMusic("random.toast", 1, 1, False)
        else:
            self.ui_toptips_args = args
            self.ui_toptips.update_args()

        # 定时关闭
        if tip_time!=-1:
            comp = clientApi.GetEngineCompFactory().CreateGame(LevelId)
            comp.AddTimer(tip_time,tip_close_f)
            


    @Listen("OnLocalPlayerStopLoading")
    def client_init(self, args):
        self.NotifyToServer("OnLocalPlayerStopLoading", {})

        # 新增molang部分
        query_comp = CF.CreateQueryVariable(LevelId) # 创建queryVariable组件
        query_comp.Register('query.mod.team_red', 0.0) # 注册molang
        query_comp.Register('query.mod.team_blue', 0.0) # 注册molang
        query_comp.Register('query.mod.team_green', 0.0) # 注册molang
        query_comp.Register('query.mod.team_yellow', 0.0) # 注册molang

    @Listen("SetMolangValue", "server")
    def SetMolangValue(self, args):
        """
        设置molang变量的值
        """
        args.pop(PlayerId)
        for pid, team in args.items():
            query_comp = CF.CreateQueryVariable(pid) # 创建queryVariable组件
            query_comp.Set('query.mod.team_' + team, 1.0) # 设置molang变量的值

    @Listen("SetPlayerStroke", "server")
    def setPlayerStroke(self, args):
        """
        设置molang变量的值
        """
        query_comp = CF.CreateQueryVariable(args["id"])  # 创建queryVariable组件
        query_comp.Set('query.mod.team_' + args["team"], 1.0)  # 设置molang变量的值

    @Listen(event_type=Listen.server)
    def SetGameInfoText(self, args):
        """
        设置游戏信息文本
        """
        self.game_info_text = args["text"]

    @Listen(event_type=Listen.server)
    def death(self, args):
        """
        玩家死亡
        """
        self.death_number += 1

    @Listen(event_type=Listen.server)
    def kill(self, args):
        """
        玩家击杀
        """
        self.kill_number += 1

    @Listen(event_type=Listen.server)
    def resetKillandDeath(self, args):
        self.kill_number = 0
        self.death_number = 0

    @Listen()
    def UiInitFinished(self, args):
        """
        ui创建创建成功
        """
        self.NotifyToServer('UiInitFinished', dict())

        clientApi.RegisterUI(modName, "cy_toptips",
                             modName+".client.ui.cy_toptips.Main",
                             "cy_toptips.main")

        # 给原生暂停界面注册委托
        NativeScreenManager.instance().RegisterScreenProxy(
            "pause.pause_screen", "Common.client.ui.pause_ui_proxys.Main"
        )

    # @Listen()
    # def PushScreenEvent(self, args):
    #     if args.get("screenName") in ["toast_screen", "in_game_play_screen", "hud_screen"]:
    #         return
    #     CF.CreatePostProcess(LevelId).SetEnableGaussianBlur(True)
    #     self.GaussianBlurValue = 1
    #     CF.CreatePostProcess(LevelId).SetGaussianBlurRadius(self.GaussianBlurValue)

    # @Listen()
    # def PopScreenAfterClientEvent(self, args):
    #     if args.get("screenName") in ["hud_screen"]:
    #         self.GaussianBlurTimer = Game.AddRepeatedTimer(0.01, self.clearGaussianBlur)

    # def clearGaussianBlur(self):
    #     self.GaussianBlurValue -= 0.4
    #     if self.GaussianBlurValue < 0:
    #         self.GaussianBlurValue = 0
    #         CF.CreatePostProcess(LevelId).SetEnableGaussianBlur(False)
    #         Game.CancelTimer(self.GaussianBlurTimer)
    #         return
    #     CF.CreatePostProcess(LevelId).SetGaussianBlurRadius(self.GaussianBlurValue)

