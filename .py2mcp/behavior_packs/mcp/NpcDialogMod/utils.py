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


class BaseState(ClientSystem):
    """
    状态基类，所有具体状态都应继承此类
    实现了基本的状态管理功能和事件监听机制
    """

    enabled = None  # 状态是否启用标志
    state_name = "on"  # 状态名称，子类必须设置
    system = None  # 系统引用
    fsm = None  # 所属状态机引用
    parent_state = None  # 父状态引用（用于子状态）

    # 事件监听配置字典，定义不同类型事件的监听目标
    ListenDict = {
        Listen.Minecraft: ("Minecraft", "Engine"),
        Listen.client: (modName, "main"),
        Listen.server: (modName, "main")
    }

    def __init__(self, namespace, name):
        """
        初始化状态
        :param namespace: 命名空间
        :param name: 系统名称
        """
        super(BaseState, self).__init__(namespace, name)
        # 获取系统弱引用，避免循环引用导致内存泄漏
        self.system = weakref.proxy(clientApi.GetSystem(modName, systemName))
        self.sub_states = set()  # 子状态集合

    def _on_enable(self, *args, **kwargs):
        """启用状态 - 自动启用所有子状态"""
        self._on_disable(*args, **kwargs)  # 先清理
        self.enabled = True
        self.Register()
        self.on_enable(*args, **kwargs)

        # 自动启用所有子状态
        for sub_state in self.sub_states:
            if not sub_state.enabled:
                sub_state._on_enable(*args, **kwargs)

    def _on_disable(self, *args, **kwargs):
        """禁用状态 - 自动禁用所有子状态"""
        self.enabled = False
        self.UnListenAllEvents()

        # 先自动禁用所有子状态
        for sub_state in self.sub_states:
            if sub_state.enabled:
                sub_state._on_disable(*args, **kwargs)

        self.on_disable(*args, **kwargs)

    def on_enable(self, *args, **kwargs):
        """子类应重写此方法实现状态启用时的逻辑"""
        pass

    def on_disable(self, *args, **kwargs):
        """子类应重写此方法实现状态禁用时的逻辑"""
        pass

    def Register(self):
        """
        自动注册带有监听器注解的方法
        遍历类的所有属性，检查是否有监听器注解
        """
        for key in dir(self):
            obj = getattr(self, key)
            # 检查方法是否有listen_event属性（被监听器装饰器装饰过）
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, 'listen_event')  # 获取事件名称
                _type = getattr(obj, 'listen_type')  # 获取事件类型
                priority = getattr(obj, 'listen_priority')  # 获取监听优先级
                self.listen(event, obj, _type, priority)

    def listen(self, event, func, _type, priority):
        """
        注册事件监听器
        :param event: 事件名称
        :param func: 回调函数
        :param _type: 事件类型
        :param priority: 监听优先级
        """
        # 从ListenDict中获取实际的系统名称和命名空间
        if _type not in self.ListenDict:
            name, system = _type, "main"  # 默认值
        else:
            name, system = self.ListenDict[_type]

        self.ListenForEvent(name, system, event, self, func, priority)

    def unlisten(self, event, func, _type, priority):
        """
        取消事件监听
        :param event: 事件名称
        :param func: 回调函数
        :param _type: 事件类型
        :param priority: 监听优先级
        """
        # 从ListenDict中获取实际的系统名称和命名空间
        if _type not in self.ListenDict:
            name, system = _type, "main"  # 默认值
        else:
            name, system = self.ListenDict[_type]

        self.UnListenForEvent(name, system, event, self, func, priority)

    def add_sub_state(self, state_type, *args, **kwargs):
        """
        添加子状态
        :param state_type: 子状态类
        :return: 创建的子状态实例
        """
        state = state_type(modName, systemName)
        state.fsm = self.fsm or self  # 子状态继承父状态的FSM
        state.parent_state = self  # 设置父状态引用
        self.sub_states.add(state)  # 添加到子状态集合
        return state

    def start_sub_state(self, state_name, *args, **kwargs):
        """
        激活指定的子状态（禁用其他子状态）
        :param state_name: 要激活的子状态名称
        """
        for state in self.sub_states:
            if state.state_name == state_name:
                state._on_enable(*args, **kwargs)
                logger.debug("Enable sub-state {} under {}".format(state.state_name, self.state_name))
            else:
                state._on_disable()
                logger.debug("Disable sub-state {} under {}".format(state.state_name, self.state_name))

    def end_sub_state(self, state_name, *args, **kwargs):
        """
        结束指定的子状态（禁用）
        :param state_name: 要结束的子状态名称
        :param args: 传递给子状态on_disable的可变参数
        :param kwargs: 传递给子状态on_disable的关键字参数
        """
        for state in self.sub_states:
            if state.state_name == state_name:
                state._on_disable(*args, **kwargs)
                logger.debug("End sub-state {} under {}".format(state_name, self.state_name))
                return True
        logger.warning("Sub-state {} not found under {}".format(state_name, self.state_name))
        return False

class OFF(BaseState):
    state_name = "off"