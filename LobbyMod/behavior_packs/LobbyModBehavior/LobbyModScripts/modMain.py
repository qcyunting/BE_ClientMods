# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi

from LobbyModScripts.modCommon import modConfig

@Mod.Binding(name = modConfig.ModName, version = modConfig.ModVersion)
class imchuyun(object):
	@Mod.InitClient()
	def LobbySystemInit(self):
		"""
		系统客户端初始化
		"""
		CliName = "LobbySystem"
		path = "%s.modClient.clientSystem.%s.%s" % ("LobbyModScripts",CliName,CliName)
		clientApi.RegisterSystem(modConfig.ModName, CliName, path)
	@Mod.InitClient()
	def MusicSystemInit(self):
		"""
		音乐客户端初始化
		"""
		CliName = "MusicSystem"
		path = "%s.modClient.clientSystem.%s.%s" % ("LobbyModScripts",CliName,CliName)
		clientApi.RegisterSystem(modConfig.ModName, CliName, path)

	@Mod.DestroyClient()
	def MusicSystemDestroy(self):
		pass
	@Mod.DestroyClient()
	def LobbySystemDestroy(self):
		pass

