# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
from LobbyModScripts.modCommon import modConfig

engineCompFactory = clientApi.GetEngineCompFactory()

class OpenSystem(ClientSystem):
	# 控制mod包是否启用通用系统
	def __init__(self, namespace, systemName):
		print("==== OpenSystem Init ====")
		ClientSystem.__init__(self, namespace, systemName)
		self._ClientListenEvent()
		self.mLocalPlayerId = clientApi.GetLocalPlayerId()

		self.levelId = clientApi.GetLevelId()
		self.msgComp = engineCompFactory.CreateTextNotifyClient(self.levelId)

	def _ClientListenEvent(self):
		self.listen_client("UiInitFinished", self.UiInitFinished)

		self.listen_server("showMsg", self._showMsg)
		self.listen_server("OpenMod", self._OpenMod)

	def listen_server(self,event,func):
		self.ListenForEvent(modConfig.ModName, "OpenSystem", event, self, func)
	
	def listen_client(self,event,func):
		self.ListenForEvent("Minecraft", "Engine", event, self, func)

	def UiInitFinished(self, args):
		# ui界面注册完毕
		print("UiInitFinished",args)

	def _showMsg(self, args):
		# 客户端通知事件
		comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLevelId())
		comp.SetLeftCornerNotify(args['msg'])

	def _OpenMod(self,args):
		# 启动mod
		print("_OpenMod",args)
		_open = args.get("value",False)
		if _open:
			# 代表接受到开启mod的请求
			self.RegisterSystem()
		

	# 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
	def Destroy(self):
		print("===== OpenSystem Destroy =====")
		pass


	#========================================================================
	# 以下为注册系统
	def RegisterSystem(self):
		ScriptsName = "LobbyModScripts"
		CliNames = [
			"LobbySystem",
			"MusicSystem",
			"GameSelectSystem"
			]
		for CliName in CliNames:
			path = "%s.modClient.clientSystem.%s.%s" % (ScriptsName,CliName,CliName)
			clientApi.RegisterSystem(modConfig.ModName, CliName, path)
	
