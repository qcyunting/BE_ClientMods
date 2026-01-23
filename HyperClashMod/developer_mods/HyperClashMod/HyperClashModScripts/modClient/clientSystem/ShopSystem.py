# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
from HyperClashModScripts.modCommon import modConfig

engineCompFactory = clientApi.GetEngineCompFactory()

class ShopSystem(ClientSystem):
	def __init__(self, namespace, systemName):
		print("==== ShopSystem Init ====")
		ClientSystem.__init__(self, namespace, systemName)
		self._ClientListenEvent()
		self.mLocalPlayerId = clientApi.GetLocalPlayerId()

		self.levelId = clientApi.GetLevelId()
		self.msgComp = engineCompFactory.CreateTextNotifyClient(self.levelId)

	def _ClientListenEvent(self):
		self.listen_client("UiInitFinished", self.UiInitFinished)

		self.listen_server("showMsg", self._showMsg)
		self.listen_server("OpenCustomShop", self._OpenCustomShop)

	def listen_server(self,event,func):
		self.ListenForEvent(modConfig.ModName, "ShopSystem", event, self, func)
	
	def listen_client(self,event,func):
		self.ListenForEvent("Minecraft", "ShopSystem", event, self, func)

	def UiInitFinished(self, args):
		# 注册并创建商店ui
		path_h = "HyperClashModScripts.modClient.ui."
		clientApi.RegisterUI(modConfig.ModName, "shop", "%sShopUI.ShopUI" % path_h, "ShopUI.main")

	def _showMsg(self, args):
		# 客户端通知事件
		comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLevelId())
		comp.SetLeftCornerNotify(args['msg'])

	def _OpenCustomShop(self,args):
		# 弹出商店UI
		print("_OpenCustomShop",args)
		clientApi.PushScreen(modConfig.ModName, "shop",args)

	# 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
	def Destroy(self):
		print("===== ShopSystem Destroy =====")
		pass
