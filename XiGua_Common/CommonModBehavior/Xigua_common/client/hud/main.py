# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from ..utils.cube_renderer import *
from ..misc.blur import GaussianBlurController
from ..misc.debug_shop import test_shop as run_test_shop
from ..misc.input import handle_alt_camera_key
import time


class Main(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.game_info_text = playerName
        self.blur_controller = GaussianBlurController()
        self.regScreenProxy()
        self.cube_renderer = CubeRenderer(self)
        clientApi.SetEnableReconnectNetgame(True)
        self.id = None
        self.start_pos = ()
        self.iiiiiiiiiiiiiiiiiiiiiiiiiii = 0

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
        clientApi.RegisterUI(modName, "xg_chat", "{}.client.chat.main.Chat".format(modName), "xg_chat.main")

        clientApi.HideChangePersonGui(True)
        clientApi.HidePauseGUI(True)
        clientApi.HideChatGUI(True)
        clientApi.HideFoldGUI(True)
        clientApi.HideVoiceGUI(True)


    @Listen()
    def ClientItemUseOnEvent(self, args):
        if time.time() - self.iiiiiiiiiiiiiiiiiiiiiiiiiii <= 1:
            return
        self.iiiiiiiiiiiiiiiiiiiiiiiiiii = time.time()
        item = args.get("itemDict")
        x = args.get("x")
        y = args.get("y")
        z = args.get("z")
        pos = (x, y, z)
        if item["newItemName"] == "minecraft:wooden_axe":
            if self.start_pos:
                if self.id:
                    self.removeSfx(self.id)
                    CF.CreateTextNotifyClient(levelId).SetLeftCornerNotify("§c已取消")
                    self.id = None
                    self.start_pos = ()
                else:
                    self.id = self.cube_renderer.renderCube(self.start_pos, pos, True)
                    CF.CreateTextNotifyClient(levelId).SetLeftCornerNotify("§a已记录结束坐标")
            else:
                self.start_pos = pos
                CF.CreateTextNotifyClient(levelId).SetLeftCornerNotify("§a已记录开始坐标")

    def createSfx_test(self):
        frameEntityId = self.CreateEngineSfxFromEditor("effects/test.json")
        frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
        frameAniTransComp.SetPos((0,100,0))
        frameAniTransComp.SetRot((0,0,0))
        frameAniTransComp.SetScale((1,1,1))
        frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
        frameAniControlComp.Play()

    def createSfx(self):
        return self.cube_renderer.renderCube((0, 100, 0), (10, 102, -2))

    # 删除
    def removeSfx(self, frameEntityId):
        self.cube_renderer.removeCube(frameEntityId)

    @Listen()
    def OnKeyPressInGame(self, args):
        handle_alt_camera_key(args)

    def test_shop(self):
        return run_test_shop()

    def regScreenProxy(self):
        NativeScreenManager = clientApi.GetNativeScreenManagerCls()

        screen_list = {
            "hud.hud_screen": "{}.client.hud.ui.hud.Main".format(modName),
            "pause.pause_screen": "{}.client.misc.ui.pause_ui.Main".format(modName),
            "settings.screen_world_controls_and_settings": "{}.client.xg_settings.ui.settings.Settings".format(modName),
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
