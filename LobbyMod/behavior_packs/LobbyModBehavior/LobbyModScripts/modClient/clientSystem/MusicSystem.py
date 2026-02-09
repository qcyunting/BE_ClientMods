# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
from LobbyModScripts.modCommon import modConfig

import random

engineCompFactory = clientApi.GetEngineCompFactory()

class MusicSystem(ClientSystem):
	def __init__(self, namespace, systemName):
		print("==== MusicSystem Init ====")
		ClientSystem.__init__(self, namespace, systemName)
		self._ClientListenEvent()
		self.mLocalPlayerId = clientApi.GetLocalPlayerId()

		self.levelId = clientApi.GetLevelId()
		self.msgComp = engineCompFactory.CreateTextNotifyClient(self.levelId)

		self.LobbyMusicList = [  
                    "flower",
                    "green",
                    "sun"
                  ]
		
		self.MusicTipsTimes = 20
		self.LobbyMusicTips_Timer = None

	def _ClientListenEvent(self):
		self.listen_client("UiInitFinished", self.UiInitFinished)

		self.listen_server("showMsg", self._showMsg)

	def listen_server(self,event,func):
		self.ListenForEvent(modConfig.ModName, "MusicSystem", event, self, func)
	
	def listen_client(self,event,func):
		self.ListenForEvent("Minecraft", "Engine", event, self, func)

	def UiInitFinished(self, args):
		# 客户端UI初始化
		# path_h = "LobbyModScripts.modClient.ui."
		# suc = clientApi.RegisterUI(modConfig.ModName, "shop", path_h+"shopui.Main", "shop.main")
		# print("UiInitFinished",suc)
		self.LobbyMusic_Play()

	def LobbyMusic_Play(self):
		"""
		主城音乐模块
		"""

		# 随机选择一个音乐
		music = random.choice(self.LobbyMusicList)

		# 屏蔽原版背景音乐
		comp = clientApi.GetEngineCompFactory().CreateCustomAudio(self.levelId)
		comp.DisableOriginMusic(True)

		# 开始播放背景音乐
		comp = clientApi.GetEngineCompFactory().CreateCustomAudio(self.levelId)
		suc = comp.PlayGlobalCustomMusic("lobby.{}".format(music), 1, False)
		print("[DEBUG] LobbyMusic_Play",music,suc)

		# 提示播放音乐标题，保持20秒左右
		comp = clientApi.GetEngineCompFactory().CreateGame(self.levelId)
		self.LobbyMusicTips_Timer = comp.AddRepeatedTimer(1.0,self.LobbyMusicTips,music=music)
	
	def LobbyMusicTips(self,music):
		self.MusicTipsTimes -=1
		if self.MusicTipsTimes:
			comp = clientApi.GetEngineCompFactory().CreateGame(self.mLocalPlayerId)
			comp.SetTipMessage("§e正在播放：§q音乐-{}".format(music))
		else:
			comp = clientApi.GetEngineCompFactory().CreateGame(self.levelId)
			comp.CancelTimer(self.LobbyMusicTips_Timer)
			self.LobbyMusicTips_Timer = None
		
	def _showMsg(self, args):
		# 客户端通知事件
		comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLevelId())
		comp.SetLeftCornerNotify(args['msg'])

	# 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
	def Destroy(self):
		print("===== MusicSystem Destroy =====")
		pass
