# coding=utf-8
from ..utils import *
from ..module_registry import Module


@Module("CrateAnimation")
class CrateAnimationModule(BaseState):
    def __init__(self, namespace, systemName):
        super(CrateAnimationModule, self).__init__(namespace, systemName)
        self.ui_registered = None

    def on_enable(self):
        self.ListenForEvent(modName, "main", "OpenCrateAnimation", self, self.open_animation)
        self.ListenForEvent("Minecraft", "Engine", "UiInitFinished", self, self.on_ui_init_finished)
        self.register_ui()

    def on_disable(self):
        pass

    def on_ui_init_finished(self, args):
        self.register_ui()

    def register_ui(self):
        self.ui_registered = clientApi.RegisterUI(
            modName,
            "crateanimation",
            "{}.ui.CrateAnimation.Main".format(modName),
            "crateanimation.main"
        )
        print("[LobbyMod][CrateAnimation] RegisterUI result={}".format(self.ui_registered))
        return self.ui_registered

    def open_animation(self, args):
        if not isinstance(args, dict):
            return
        items = args.get("items")
        if not isinstance(items, (list, tuple)) or not items:
            return
        print("[LobbyMod][CrateAnimation] OpenCrateAnimation items={}".format(len(items)))
        self.register_ui()
        screen = clientApi.PushScreen(modName, "crateanimation", {"isHud": 1, "data": args, "client": self})
        print("[LobbyMod][CrateAnimation] PushScreen result={}".format(screen))
