# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi

from HyperClashModScripts.modCommon import modConfig

@Mod.Binding(name = modConfig.ModName, version = modConfig.ModVersion)
class imchuyun(object):
	@Mod.InitClient()
	def ShopSystemInit(self):
		"""
		商店系统客户端初始化
		"""
		CliName = "ShopSystem"
		path = "%s.modClient.clientSystem.%s.%s" % (modConfig.ModName,CliName,CliName)
		clientApi.RegisterSystem(modConfig.ModName, CliName, path)

	@Mod.DestroyClient()
	def ShopSystemDestroy(self):
		pass

