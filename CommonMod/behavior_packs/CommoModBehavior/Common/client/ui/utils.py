# -*- encoding: utf-8 -*-
from ..utils import *
import re
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
base_path = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
LevelId  = clientApi.GetLevelId()

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

class BaseCustomScreen(ScreenNode):
    ListenDict = {"Minecraft": ("Minecraft", "Engine"), "client": (modName, "main"), "server": (modName, "main")}
    system = None
    def __init__(self, namespace, name, param):
        super(BaseCustomScreen, self).__init__(namespace, name, param)
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
        self.system = weakref.proxy(clientApi.GetSystem(modName, "main"))
        self.screen = screenNode  # type: ScreenNode
        self.Register()

    def OnCreate(self):
        pass

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


class ScreenNode(object):
    def SetBindWorldPosition(self, dimension, position):
        # type: (int, Tuple[float,float,float]) -> 'bool'
        """
        设置UI绑定的worldPosition
        """
        pass

    def Update(self):
        # type: () -> 'None'
        """
        客户端每帧调用，1秒有30帧
        """
        pass

    def Destroy(self):
        # type: () -> 'None'
        """
        UI生命周期函数，当UI销毁时调用。
        """
        pass

    def Create(self):
        # type: () -> 'None'
        """
        UI生命周期函数，当UI创建成功时调用。
        """
        pass

    def OnDeactive(self):
        # type: () -> 'None'
        """
        UI生命周期函数，当栈顶UI有其他UI入栈时调用。
        """
        pass

    def OnActive(self):
        # type: () -> 'None'
        """
        UI生命周期函数，当UI重新回到栈顶时调用。
        """
        pass

    def SetScreenVisible(self, visible):
        # type: (bool) -> 'None'
        """
        设置是否显示本界面
        """
        pass

    def ChangeBindEntityId(self, entityId):
        # type: (str) -> 'bool'
        """
        修改绑定的实体id，**只对已绑定实体的UI界面生效，如何将UI与实体绑定详见CreateUI接口**
        """
        pass

    def BindVirtualWorldModel(self, bindToObjId, offset):
        # type: (int, Tuple[float,float,float]) -> 'bool'
        """
        绑定虚拟世界中的模型
        """
        pass

    def ChangeBindOffset(self, offset):
        # type: (Tuple[float,float,float]) -> 'bool'
        """
        修改与绑定实体之间的偏移量，**只对已绑定实体的UI界面生效，如何将UI与实体绑定详见CreateUI接口**
        """
        pass

    def ChangeBindAutoScale(self, autoScale):
        # type: (int) -> 'bool'
        """
        设置已绑定实体的UI是否根据绑定实体与本地玩家间的距离动态缩放，**只对已绑定实体的UI界面生效，如何将UI与实体绑定详见CreateUI接口**
        """
        pass

    def GetBindEntityId(self):
        # type: () -> 'str'
        """
        获取该UI绑定的实体id，未绑定的UI将传回默认值None
        """
        pass

    def GetBindWorldPosition(self):
        # type: () -> 'Tuple[int,Tuple[float,float,float]]'
        """
        获取该UI绑定的worldPosition，未绑定返回默认值None
        """
        pass

    def GetBindOffset(self):
        # type: () -> 'Tuple[float,float,float]'
        """
        获取该UI绑定实体的偏移量，未绑定的UI将传回默认值(0, 0, 0)
        """
        pass

    def GetBindAutoScale(self):
        # type: () -> 'int'
        """
        获取该绑定实体的UI是否动态缩放，未绑定的UI将传回默认值1
        """
        pass

    def Clone(self, componentPath, parentPath, newName, syncRefresh=True, forceUpdate=True):
        # type: (str, str, str, bool, bool) -> 'bool'
        """
        克隆一个已有的控件，修改它的名称，并将它挂接到指定的父节点上，目前文本、图片、按钮控件的克隆控件表现正常，其他复杂控件的克隆控件可能存在运行问题，建议在json编写的过程中，手动复制一份对应控件使用。
        """
        pass

    def GetChildrenName(self, parentPath):
        # type: (str) -> 'List[str]'
        """
        获取子节点的名称list
        """
        pass

    def GetAllChildrenPath(self, parentPath):
        # type: (str) -> 'List[str]'
        """
        获取所有子节点的路径list
        """
        pass

    def RemoveComponent(self, componentPath, parentPath):
        # type: (str, str) -> 'None'
        """
        动态删除某一控件
        """
        pass

    def SetRemove(self):
        # type: () -> 'None'
        """
        删除本界面节点
        """
        pass

    def CreateChildControl(self, defName, childName, parentControl=None, forceUpdate=True):
        # type: (str, str, BaseUIControl, bool) -> 'BaseUIControl'
        """
        在当前画布中创建子控件，如果该子控件已经存在则返回已存在的子控件
        """
        pass

    def RemoveChildControl(self, childControl):
        # type: (BaseUIControl) -> 'bool'
        """
        移除当前画布中的子控件
        """
        pass

    def SetUiModel(self, componentPath, modelName, animateName='idle', looped=True):
        # type: (str, str, str, bool) -> 'bool'
        """
        设置PaperDoll控件需要显示的模型,PaperDoll控件的配置方式详见<a href="../../../../mcguide/18-界面与交互/30-UI说明文档.html#paperdoll">控件介绍PaperDoll</a>
        """
        pass

    def SetUiEntity(self, componentPath, entityIdentifier):
        # type: (str, str) -> 'None'
        """
        设置PaperDoll控件需要显示的生物模型,PaperDoll控件的配置方式详见<a href="../../../../mcguide/18-界面与交互/30-UI说明文档.html#paperdoll">控件介绍PaperDoll</a>
        """
        pass

    def SetUiModelScale(self, componentPath, scale=1.0):
        # type: (str, float) -> 'None'
        """
        设置PaperDoll控件模型的缩放比例
        """
        pass

    def UpdateScreen(self, syncRefresh=True):
        # type: (bool) -> 'None'
        """
        刷新界面，重新计算各个控件的相关数据
        """
        pass

    def SetStackGridCount(self, componentPath, count):
        # type: (str, int) -> 'None'
        """
        设置StackGrid控件的大小
        """
        pass

    def SetSelectControl(self, componentPath, enable):
        # type: (str, bool) -> 'None'
        """
        设置当前焦点所在的控件,当设置控件为文本输入框时会弹出系统小键盘
        """
        pass

    def GetRichTextItem(self, componentPath):
        # type: (str) -> 'object'
        """
        返回一个富文本控件实例
        """
        pass

    def SetIsHud(self, isHud):
        # type: (int) -> 'None'
        """
        设置本界面的输入模式
        """
        pass

    def GetIsHud(self):
        # type: () -> 'int'
        """
        获得本界面的输入模式
        """
        pass

    def GetScreenName(self):
        # type: () -> 'str'
        """
        获得本界面的名称
        """
        pass

    def GetSelf(self):
        # type: () -> 'ScreenNode'
        """
        获取零件界面自身
        """
        pass

    def GetBaseUIControl(self, path):
        # type: (str) -> 'BaseUIControl'
        """
        根据路径获取BaseUIControl实例
        """
        pass

