# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from HyperClashModScripts.modCommon.modConfig import ModName

class ShopUI(clientApi.GetScreenNodeCls()):

    def __init__(self, namespace, name, param):
        super(ShopUI, self).__init__(namespace, name, param)
        self.clientSystem = clientApi.GetSystem(ModName, "ShopSystem")

    def Create(self):
        pass

    def _showMsg(self, args):
        self.clientSystem.NotifyToServer('requestMsg', {})
