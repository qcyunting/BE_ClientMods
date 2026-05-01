# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from ..misc.blur import GaussianBlurController
from ..misc.debug_shop import test_shop as run_test_shop
from ..misc.input import handle_alt_camera_key
from ..misc.screen_registry import register_screen_proxies


class Main(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.game_info_text = playerName
        self.blur_controller = GaussianBlurController()
        self.regScreenProxy()
        clientApi.SetEnableReconnectNetgame(True)

    @Listen(event_type=Listen.server)
    def startMod(self, args):
        print("startMod", args)
        self.BroadcastEvent("StartMod", args["all_mod"])

    @Listen(event_type=Listen.server)
    def SetGameInfoText(self, args):
        """
        设置游戏信息文本
        """
        self.game_info_text = args["text"]

    @Listen()
    def UiInitFinished(self, args):
        """
        ui创建成功
        """
        self.NotifyToServer("UiInitFinished", dict())

    @Listen()
    def OnKeyPressInGame(self, args):
        handle_alt_camera_key(args)

    def test_shop(self):
        return run_test_shop()

    def regScreenProxy(self):
        NativeScreenManager = clientApi.GetNativeScreenManagerCls()

        clientApi.HideChangePersonGui(True)
        clientApi.HidePauseGUI(True)
        clientApi.HideChatGUI(True)
        clientApi.HideFoldGUI(True)
        clientApi.HideVoiceGUI(True)
        clientApi.Hide

        screen_list = {
            "hud.hud_screen": "{}.client.hud.ui.hud.Main".format(modName),
            "pause.pause_screen": "{}.client.misc.ui.pause_ui.Main".format(modName),
        }
        for screenName, proxyClassName in screen_list.items():
            NativeScreenManager.instance().RegisterScreenProxy(
                screenName, proxyClassName
            )

    @Listen()
    def PushScreenEvent(self, args):
        self.blur_controller.on_push_screen_event(args)

    @Listen()
    def PopScreenAfterClientEvent(self, args):
        self.blur_controller.on_pop_screen_after_client_event(args)

    def clearGaussianBlur(self):
        self.blur_controller.clear()
