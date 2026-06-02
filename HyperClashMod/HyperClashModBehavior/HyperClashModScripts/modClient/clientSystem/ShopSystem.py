# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
from HyperClashModScripts.modCommon import modConfig

engineCompFactory = clientApi.GetEngineCompFactory()

class ShopSystem(ClientSystem):
	def __init__(self, namespace, systemName):
		print "==== ShopSystem Init ===="
		ClientSystem.__init__(self, namespace, systemName)
		self._ClientListenEvent()
		self.mLocalPlayerId = clientApi.GetLocalPlayerId()

		self.levelId = clientApi.GetLevelId()
		self.msgComp = engineCompFactory.CreateTextNotifyClient(self.levelId)
		# 保存商店UI实例引用
		self.shopUI = None
		self.uiRegistered = False
		self.skillData = None
		self.lastStatsData = None
		self.lastCooldownData = None

	def _ClientListenEvent(self):
		# 监听引擎事件 - UI初始化完成
		self.listen_client("UiInitFinished",self.UiInitFinished)

		# 监听服务端事件
		self.listen_server("showMsg", self._showMsg)
		self.listen_server("OpenCustomShop", self._OpenCustomShop)
		self.listen_server("UpdateItemDetail", self._UpdateItemDetail)

		self.ListenForEvent(modConfig.ModName, "SkillSystem", "ShowSkillButtons", self, self.initSkill)  # 初始化
		self.ListenForEvent(modConfig.ModName, "SkillSystem", "UpdateSkillCooldown", self, self._UpdateSkillCooldown)
		self.ListenForEvent(modConfig.ModName, "PlayerStats", "UpdateStats", self, self._UpdateStats)


	def listen_server(self, event, func):
		self.ListenForEvent(modConfig.ModName, "ShopSystem", event, self, func)

	def listen_client(self, event, func):
		self.ListenForEvent("Minecraft", "Engine", event, self, func)

	def UiInitFinished(self, args):
		print "==== UiInitFinished, RegisterUI ===="
		path_h = "HyperClashModScripts.modClient.ui."
		# RegisterUI(namespace, uiKey, clsPath, uiDef)
		# uiDef 格式: "jsonNamespace.screenName"
		clientApi.RegisterUI("HyperClash", "shop", "%sShopUI.ShopUI" % path_h, "shop.main")
		clientApi.RegisterUI("HyperClashHUD", "main", "%sHUD.HUD" % path_h, "HyperClashHUD.main")
		self.uiRegistered = True

	def _showMsg(self, args):
		# 客户端通知事件
		comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLevelId())
		comp.SetLeftCornerNotify(args['msg'])

	def initSkill(self, args):
		self.skillData = args
		hud_ui = self._ensure_hud()
		if hud_ui:
			hud_ui.RefreshSkillData(args)
			if self.lastStatsData:
				hud_ui.UpdateStats(self.lastStatsData)
			if self.lastCooldownData:
				hud_ui.UpdateSkillCooldown(self.lastCooldownData)

	def _ensure_hud(self):
		if not self.uiRegistered:
			self.UiInitFinished(None)

		hud_ui = clientApi.GetUI("HyperClashHUD", "main")
		if hud_ui:
			return hud_ui

		data = self.skillData if self.skillData else {}
		try:
			return clientApi.CreateUI("HyperClashHUD", "main", {"isHud": 1, "data": data})
		except Exception as e:
			print "[ShopSystem] Create HUD failed:", e
			return clientApi.GetUI("HyperClashHUD", "main")

	def _UpdateSkillCooldown(self, args):
		self.lastCooldownData = args
		hud_ui = self._ensure_hud()
		if hud_ui:
			hud_ui.UpdateSkillCooldown(args)

	def _UpdateStats(self, args):
		self.lastStatsData = args
		hud_ui = self._ensure_hud()
		if hud_ui:
			hud_ui.UpdateStats(args)

	def _OpenCustomShop(self, args):
		# 确保UI已注册
		if not self.uiRegistered:
			self.UiInitFinished(None)

		# 检查UI是否已经存在
		if self.shopUI:
			try:
				# 尝试更新数据
				self.shopUI.UpdateShopData(args)
				print "[ShopSystem] Updated existing shop UI"
				return
			except Exception as e:
				print "[ShopSystem] Failed to update UI, will recreate: " + str(e)
				self.shopUI = None

		# 第一次打开，或者UI被关闭了
		self.shopUI = clientApi.PushScreen("HyperClash", "shop", args)
		print "[ShopSystem] Created new shop UI"

	def _UpdateItemDetail(self, args):
		# 更新物品详情
		print "_UpdateItemDetail", args
		if self.shopUI:
			self.shopUI.UpdateItemDetail(args)

	def Destroy(self):
		print "===== ShopSystem Destroy ====="
		self.shopUI = None
