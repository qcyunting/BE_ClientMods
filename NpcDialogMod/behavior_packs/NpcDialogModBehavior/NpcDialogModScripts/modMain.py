# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi

from NpcDialogModScripts.modCommon import modConfig

@Mod.Binding(name = modConfig.ModName, version = modConfig.ModVersion)
class imchuyun(object):
	@Mod.InitClient()
	def NpcDialogModInit(self):
		"""
		系统客户端初始化
		"""
		CliName = "NpcDialogMod"
		path = "%s.modClient.clientSystem.%s.%s" % ("NpcDialogModScripts",CliName,CliName)
		clientApi.RegisterSystem(modConfig.ModName, CliName, path)

	@Mod.DestroyClient()
	def NpcDialogModDestroy(self):
		pass

