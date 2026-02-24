# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
from LobbyModScripts.modCommon import modConfig

engineCompFactory = clientApi.GetEngineCompFactory()

class GameSelectSystem(ClientSystem):
	def __init__(self, namespace, systemName):
		print("==== GameSelectSystem Init ====")
		ClientSystem.__init__(self, namespace, systemName)
		self._ClientListenEvent()
		self.mLocalPlayerId = clientApi.GetLocalPlayerId()

		self.levelId = clientApi.GetLevelId()
		self.msgComp = engineCompFactory.CreateTextNotifyClient(self.levelId)

		self.UiInitFinished(dict())

	def _ClientListenEvent(self):
		self.listen_client("OnKeyPressInGame", self.OnKeyPressInGame)

		self.listen_server("showMsg", self._showMsg)
		self.listen_server("fzgUI", self._fzgUI)

	def listen_server(self,event,func):
		self.ListenForEvent(modConfig.ModName, "gameselect", event, self, func)
	
	def listen_client(self,event,func):
		self.ListenForEvent("Minecraft", "Engine", event, self, func)

	def UiInitFinished(self, args):
		# 注册并创建商店ui
		path_h = "LobbyModScripts.modClient.ui."
		suc = clientApi.RegisterUI(modConfig.ModName, "gameselect", path_h+"GameSelectSystemUI.Main", "gameselect.main")
		print("UiInitFinished",suc)

	def OnKeyPressInGame(self,args):
		# 按键按下或按键释放时触发
		key = args["key"]
		isDown = args["isDown"]
		if isDown=="0":
			if key=="27":
				# esc关闭键
				clientApi.PopScreen()

	def _showMsg(self, args):
		# 客户端通知事件
		comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLevelId())
		comp.SetLeftCornerNotify(args['msg'])

	def _fzgUI(self,args):
		# 弹出游戏选择器UI
		print("_fzgUI",args)
		clientApi.PushScreen(modConfig.ModName, "gameselect",{"isHud": 1, 'data': args, 'client': self})

	# 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
	def Destroy(self):
		print("===== GameSelectSystem Destroy =====")
		pass
