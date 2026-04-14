# -*- encoding: utf-8 -*-
from .ClientSystem_utils import *
import re
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
BP = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
LevelId  = clientApi.GetLevelId()

class BaseCustomScreen(ScreenNode):
    ListenDict = {"Minecraft": ("Minecraft", "Engine"), "client": (modName, "main"), "server": (modName, "main")}
    system = None
    def __init__(self, namespace, name, param):
        super(BaseCustomScreen, self).__init__(namespace, name, param)
        self.system = clientApi.GetSystem(modName, "main")
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

    def NotifyToServer(self, eventName=str(), eventData=None):
        """
        给服务器发送事件通知
        """
        self.system.NotifyToServer(eventName, eventData)

CustomUIScreenProxy = clientApi.GetUIScreenProxyCls()
class BaseCustomScreenProxy(CustomUIScreenProxy):
    ListenDict = {"Minecraft": ("Minecraft", "Engine"), "client": (modName, "main"), "server": (modName, "main")}
    system = None
    screen = None
    def __init__(self, screenName, screenNode):
        super(BaseCustomScreenProxy, self).__init__(screenName, screenNode)
        self.system = clientApi.GetSystem(modName, "main")
        self.screen = screenNode  # type: ScreenNode
        self.Register()

    def OnCreate(self):
        pass

    def Register(self):
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, 'listen_event')
                sys_name = getattr(obj, 'system_name')
                _type = getattr(obj, 'listen_type')
                priority = getattr(obj, 'listen_priority')
                self.ListenForEvent(event, obj, _type=_type, sys_name=sys_name, priority=priority)

    def ListenForEvent(self, event, func, _type, sys_name, priority):
        if _type not in self.ListenDict:
            name, system = _type, sys_name
        else:
            name, system = self.ListenDict[_type]
        self.system.ListenForEvent(name, system, event, self, func, priority=priority)

    def NotifyToServer(self, eventName=str(), eventData=None):
        """
        给服务器发送事件通知
        """
        self.system.NotifyToServer(eventName, eventData)


