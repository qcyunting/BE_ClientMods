# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from NpcDialogModScripts.modCommon.modConfig import ModName

class Main(clientApi.GetScreenNodeCls()):

    def __init__(self, namespace, name, param):
        super(Main, self).__init__(namespace, name, param)
        self.clientSystem = clientApi.GetSystem(ModName, "NpcDialogMod")

    def Create(self):
        pass

    def _showMsg(self, args):
        self.clientSystem.NotifyToServer('requestMsg', {})
