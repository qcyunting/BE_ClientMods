# -*- encoding: utf-8 -*-
import time, math, mod.client.extraClientApi as clientApi, mod.common.minecraftEnum as enum, random, weakref
from mod_log import logger as logger
from .config import *
ClientSystem = clientApi.GetClientSystemCls()
CF = clientApi.GetEngineCompFactory()
LevelId = clientApi.GetLevelId()
PlayerId = clientApi.GetLocalPlayerId()

Game = CF.CreateGame(LevelId)
PosComp = CF.CreatePos(PlayerId)
RotComp = CF.CreateRot(PlayerId)
TextBoardComp = CF.CreateTextBoard(PlayerId)
Music = CF.CreateCustomAudio(LevelId)
NameComp = CF.CreateName(PlayerId)
ItemComp = CF.CreateItem(PlayerId)

PlayerName = NameComp.GetName()

class Listen(object):
    Minecraft = "Minecraft"
    server = "server"
    client = "client"
    def __init__(self, event_name=None, event_type='Minecraft', priority=3):
        self.event_name = event_name
        self.event_type = event_type
        self.priority = priority

    def __call__(self, func):
        func.listen_type = self.event_type
        func.listen_event = self.event_name or func.__name__
        func.listen_priority = self.priority
        return func

class BaseSystem(ClientSystem):
    ListenDict = {"Minecraft": ("Minecraft", "Engine"), "client": (modName, "main"), "server": (modName, "main")}
    def __init__(self, namespace, systemName):
        super(BaseSystem, self).__init__(namespace, systemName)
        self.Register()

    def Register(self):
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, 'listen_event')
                _type = getattr(obj, 'listen_type')
                priority = getattr(obj, 'listen_priority')
                self.listen(event, obj, _type=_type, priority=priority)

    def listen(self, event, func, _type, priority):
        if _type not in self.ListenDict:
            name, system = _type, "main"
        else:
            name, system = self.ListenDict[_type]
        self.ListenForEvent(name, system, event, self, func, priority=priority)

class BaseComponent(object):
    ListenDict = {"Minecraft": ("Minecraft", "Engine"), "client": (modName, "main"), "server": (modName, "main")}
    system = None
    def __init__(self):
        self.system = weakref.proxy(clientApi.GetSystem(modName, "main"))
        self.Register()

    def Register(self):
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, 'listen_event')
                _type = getattr(obj, 'listen_type')
                priority = getattr(obj, 'listen_priority')
                self.ListenForEvent(event, obj, _type=_type, priority=priority)

    def ListenForEvent(self, event, func, _type, priority):
        if _type not in self.ListenDict:
            name, system = _type, "main"
        else:
            name, system = self.ListenDict[_type]
        self.system.ListenForEvent(name, system, event, self, func, priority=priority)

    def NotifyToClient(self, pid=str(), eventName=str(), eventData=None):
        """
        给客户端发送事件
        """
        if pid is None:
            self.NotifyToMultiClients(clientApi.GetPlayerList(), eventName, eventData)
        self.system.NotifyToClient(pid, eventName, eventData)

    def NotifyToMultiClients(self, pidList=None, eventName=str(), eventData=None):
        """
        给多个客户端发送事件
        """
        self.system.NotifyToMultiClients(pidList, eventName, eventData)

    def RequestToServiceMod(self, modname, method, args, callback=None, timeout=2):
        """
        给service发请求
        """
        self.system.RequestToServiceMod(modname, method, args, callback, timeout)


def calculate_panel_size(player_pos, panel_pos, base_size=1.0, scale_factor=0.5, max_distance=None):
    """
    计算游戏面板的大小，基于玩家与面板距离的指数函数

    参数:
    player_pos: 玩家坐标 (x, y, z)
    panel_pos: 面板坐标 (x, y, z)
    base_size: 基础大小（距离为0时的大小）
    scale_factor: 缩放因子，控制大小随距离变化的敏感度
    max_distance: 可选，最大参考距离（用于归一化）

    返回:
    distance: 距离
    size: 面板的X和Y大小
    """
    # 计算欧几里得距离
    distance = math.sqrt(
        (player_pos[0] - panel_pos[0]) ** 2 +
        (player_pos[1] - panel_pos[1]) ** 2 +
        (player_pos[2] - panel_pos[2]) ** 2
    )

    # 使用指数函数计算大小
    size = base_size * math.exp(scale_factor * distance)

    return distance, size
