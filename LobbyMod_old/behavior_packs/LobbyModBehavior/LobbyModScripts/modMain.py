# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi

from LobbyModScripts.modCommon import modConfig

@Mod.Binding(name = modConfig.ModName, version = modConfig.ModVersion)
class imchuyun(object):
	ScriptsName = "LobbyModScripts"
	@Mod.InitClient()
	def OpenSystemInit(self):
		"""
		调度客户端初始化
		"""
		CliName = "OpenSystem"
		path = "%s.modClient.clientSystem.%s.%s" % (self.ScriptsName,CliName,CliName)
		clientApi.RegisterSystem(modConfig.ModName, CliName, path)
	@Mod.DestroyClient()
	def OpenSystemDestroy(self):
		pass

