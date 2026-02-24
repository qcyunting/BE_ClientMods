# coding=utf-8
from mod.common.mod import Mod

import mod.client.extraClientApi as clientApi
import config as client_config
@Mod.Binding(name=client_config.modName, version=client_config.version)
class XiGua_client(object):
    @Mod.InitClient()
    def clientInit(self):
        path = "{}.StateBase.Main".format(client_config.modName)
        clientApi.RegisterSystem(client_config.modName, client_config.systemName, path)
        print ("======Init{}Client======".format(client_config.modName))

