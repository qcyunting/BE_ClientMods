# -*- coding: utf-8 -*-
from utils.ClientSystem_utils import *
from utils.listen_util import *


class Main(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)

    @Listen()
    def UiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})
        clientApi.RegisterUI(modName, "vd_shop", "{}.client.ui.shop.Shop".format(modName), "vd_shop.main")
        clientApi.RegisterUI(modName, "vd_effect", "{}.client.ui.effect.Effect".format(modName), "vd_effect.main")

    @Listen(event_type=Listen.server)
    def openShop(self, args):
        clientApi.PushScreen(modName, "vd_shop", {"data": args})

    @Listen(event_type=Listen.server)
    def openBuffShop(self, args):
        clientApi.PushScreen(modName, "vd_effect", {"data": args})