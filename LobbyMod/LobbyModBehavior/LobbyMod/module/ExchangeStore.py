# coding=utf-8
from ..utils import *
from ..module_registry import Module


@Module("ExchangeStore")
class ExchangeStoreModule(BaseState):
    UI_NAME = "exchangestore"

    def __init__(self, namespace, systemName):
        super(ExchangeStoreModule, self).__init__(namespace, systemName)
        self.ui_registered = None

    def on_enable(self):
        self.ListenForEvent(modName, "main", "OpenMainShop", self, self.open_shop)
        self.ListenForEvent(modName, "main", "OpenGameShop", self, self.open_shop)
        self.ListenForEvent(modName, "main", "ShopActionResult", self, self.action_result)
        self.ListenForEvent("Minecraft", "Engine", "UiInitFinished", self, self.on_ui_init_finished)
        self.ListenForEvent("Minecraft", "Engine", "OnKeyPressInGame", self, self.on_key_press)
        self.register_ui()

    def on_disable(self):
        self.stop_preview()

    def on_ui_init_finished(self, args):
        self.register_ui()

    def register_ui(self):
        self.ui_registered = clientApi.RegisterUI(
            modName,
            self.UI_NAME,
            "{}.ui.ExchangeStore.Main".format(modName),
            "exchangestore.main"
        )
        print("[LobbyMod][ExchangeStore] RegisterUI result={}".format(self.ui_registered))
        return self.ui_registered

    def open_shop(self, args):
        if not isinstance(args, dict):
            print("[LobbyMod][ExchangeStore] rejected non-dict payload")
            return
        categories = args.get("categories")
        goods = args.get("goods")
        if not isinstance(categories, (list, tuple)) or not isinstance(goods, (list, tuple)):
            print("[LobbyMod][ExchangeStore] rejected malformed categories/goods")
            return
        print("[LobbyMod][ExchangeStore] OpenShop categories={} goods={}".format(len(categories), len(goods)))
        top = clientApi.GetTopScreen()
        if top is not None and hasattr(top, "update_shop_data"):
            top.update_shop_data(args)
            print("[LobbyMod][ExchangeStore] updated active screen")
            return
        self.register_ui()
        screen = clientApi.PushScreen(
            modName,
            self.UI_NAME,
            {"isHud": 1, "data": args, "client": self}
        )
        print("[LobbyMod][ExchangeStore] PushScreen result={}".format(screen))

    def action_result(self, args):
        top = clientApi.GetTopScreen()
        if top is not None and hasattr(top, "show_action_result"):
            top.show_action_result(args if isinstance(args, dict) else {})

    def send_event(self, event_name, data):
        payload = data if isinstance(data, dict) else {}
        print("[LobbyMod][ExchangeStore] SEND {} {}".format(event_name, payload))
        self.NotifyToServer(event_name, payload)

    def stop_preview(self):
        self.send_event("StopPreviewEffect", {})

    def on_key_press(self, args):
        if not isinstance(args, dict):
            return
        if args.get("key") != "27" or args.get("isDown") != "0":
            return
        top = clientApi.GetTopScreen()
        if top is not None and hasattr(top, "close_shop"):
            top.close_shop(None)

