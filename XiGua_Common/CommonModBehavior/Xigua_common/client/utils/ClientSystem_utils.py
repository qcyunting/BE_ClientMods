# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MC_Enum
from mod_log import logger as logger
from ..config import *
from listen_util import *
ClientSystem = clientApi.GetClientSystemCls()
CF = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
playerId = clientApi.GetLocalPlayerId()

gameComp = CF.CreateGame(levelId)
posComp = CF.CreatePos(playerId)
rotComp = CF.CreateRot(playerId)
textBoardComp = CF.CreateTextBoard(levelId)
musicComp = CF.CreateCustomAudio(levelId)
nameComp = CF.CreateName(playerId)
itemComp = CF.CreateItem(playerId)
cameraComp = CF.CreateCamera(levelId)

playerComp = CF.CreatePlayer
attrComp = CF.CreateAttr
modelComp = CF.CreateModel
actorRenderComp = CF.CreateActorRender

playerName = nameComp.GetName()

class BaseSystem(ClientSystem):
    ListenDict = {
        "Minecraft": ("Minecraft", "Engine"),
        "client": (modName, "main"),
        "server": (modName, "main")
    }
    local_id = -2
    def __init__(self, namespace, systemName):
        super(BaseSystem, self).__init__(namespace, systemName)
        self.Register()

    def Register(self):
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, 'listen_event')
                sys_name = getattr(obj, 'system_name')
                _type = getattr(obj, 'listen_type')
                priority = getattr(obj, 'listen_priority')
                self.listen(event, obj, _type=_type, sys_name=sys_name, priority=priority)

    def listen(self, event, func, _type, sys_name, priority):
        if _type not in self.ListenDict:
            name, system = _type, sys_name
        else:
            name, system = self.ListenDict[_type]
        self.ListenForEvent(name, system, event, self, func, priority=priority)

    @Listen(event_type=Listen.server)
    def setLocalId(self, args):
        """
        设置本地的玩家Id
        """
        self.local_id = args.get("local_id", -2)