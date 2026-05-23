# coding=utf-8
"""
Created on 2026-02-19
音乐模块
这里主要 给主城提供加入音乐
接口：
- 
"""
from ..utils import *
from ..module_registry import Module

@Module("Music")
class MusicModule(BaseState):
    def __init__(self, namespace, systemName):
        super(MusicModule, self).__init__(namespace, systemName)
        self.events = {"server":{}, "client":{}}
        # 设置音乐列表
        self.LobbyMusicList = [  
                    "flower",
                    "green",
                    "sun"
                  ]
        
        # 当前音乐
        self.MusicNow=None
        
        # 音乐计时器
        self.MusicTipsTimes = 5
        self.LobbyMusicTips_Timer = None
    def on_enable(self):
        print "enable Music"

        self.MusicTipsTimes = 5
        # 播放音乐
        self.LobbyMusic_Play()
    
    def listen_client(self, event, func):
        self.ListenForEvent("Minecraft", "Engine", event, self, func)
        
    def on_disable(self):
        print "disable Music"

        # 停止音乐
        self.Music_Stop()
        # 关闭所有事件监听
        self.UnListenAllEvents()

    
    def LobbyMusic_Play(self):
        """
        主城音乐模块
        """

        # 随机选择一个音乐
        music = random.choice(self.LobbyMusicList)
        self.MusicNow = music

        # 屏蔽原版背景音乐
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
        comp.DisableOriginMusic(True)

        # 开始播放背景音乐
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
        suc = comp.PlayGlobalCustomMusic("lobby.{}".format(music), 1, False)
        print("[DEBUG] LobbyMusic_Play",music,suc)

        # 提示播放音乐标题，保持20秒左右
        comp = clientApi.GetEngineCompFactory().CreateGame(LevelId)
        self.LobbyMusicTips_Timer = comp.AddRepeatedTimer(1.0,self.LobbyMusicTips,music=music)

    def LobbyMusicTips(self,music):
        self.MusicTipsTimes -=1
        if self.MusicTipsTimes >= 0:
            comp = clientApi.GetEngineCompFactory().CreateGame(PlayerId)
            comp.SetTipMessage("§e正在播放：§q音乐-{}".format(music))
        else:
            comp = clientApi.GetEngineCompFactory().CreateGame(LevelId)
            comp.CancelTimer(self.LobbyMusicTips_Timer)
            self.LobbyMusicTips_Timer = None

    def Music_Stop(self):
        """
        停止所有音乐
        """
        # 停止音效，包括场景音效与背景音乐
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
        comp.StopCustomMusic("lobby.%s" % self.MusicNow, 0)
        # 停止原生背景音乐
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
        comp.DisableOriginMusic(True)






