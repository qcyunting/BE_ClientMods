# coding=utf-8
"""
Created on 2025-11-03
NpcDialog模块
这里主要 提供一个NpcDialog模块
接口：
- 
"""
from ..utils import *
from ..module_registry import Module

@Module("NpcDialog")
class NpcDialogModule(BaseState):
    npc_icon_default = [
        "ALEX_3D",
        "ALLAY",
        "CREEPER",
        "DIAMOND_GUY",
        "DOCTOR",
        "DOG",
        "EVIL",
        "GIRL",
        "GIRL_RABBIT",
        "GUARD",
        "HIM",
        "HORSE_RIDING",
        "IRON_GOLEM",
        "LIGHTNING_GUY",
        "MUSIC_GUY",
        "PARROT",
        "PIG",
        "PIGLIN",
        "REWARDER",
        "RUNNING_MAN",
        "SKELETON_HORSE",
        "SOLDIER",
        "STEVE",
        "STEVE_3D",
        "STEVE_DIAMONDS_WORD",
        "TECHNOBLADE",
        "TRAVELER",
        "UNDERGROUND_STEVE",
        "UNDYING",
        "UNDYING_OLD",
        "VEX",
        "WITCH",
        "WITHER_BOSS"
    ]
    def __init__(self, namespace, systemName):
        super(NpcDialogModule, self).__init__(namespace, systemName)

        self.ui_npcdialog_enable = None
        self.ui_npcdialog = None

    def on_enable(self):
        print("启用NpcDialog")
        self.ListenForEvent(modName, systemName, "OpenDialogue", self, self.OpenDialogue)
        self.ListenForEvent(modName, systemName, "PauseDialogue", self, self.PauseDialogue)
        self.listen_client("UiInitFinished", self.UiInitFinished)
        self.listen_client("OnKeyPressInGame", self.OnKeyPressInGame)

        self.ui_npcdialog_enable = clientApi.RegisterUI(modName, 'npcdialog', "{}.ui.NpcDialog.Main".format(modName),"npcdialog.main")
        print "ui_npcdialog_enable",self.ui_npcdialog_enable
        
    def listen_client(self, event, func):
        self.ListenForEvent("Minecraft", "Engine", event, self, func)
    
    def UiInitFinished(self,args):
        print("UiInitFinished")
        if not self.ui_npcdialog_enable:
            self.ui_npcdialog_enable = clientApi.RegisterUI(modName, 'npcdialog', "{}.ui.NpcDialog.Main".format(modName),"npcdialog.main")
            print "ui_npcdialog_enable",self.ui_npcdialog_enable

    def OnKeyPressInGame(self,args):
        key = args["key"]
        isDown = args["isDown"]
        if isDown == "0":
            if key == "27":
                pass
                ## esc键
                # self.NotifyToServerF("RequestClose", {})
                # clientApi.PopScreen()
                # self.ui_npcdialog = None

    def OpenDialogue(self, args):
        print("OpenDialogue",args)
        dialogue_id = args.get("dialogue_id")
        npc_name = args.get("npc_name")
        npc_icon = self.npc_icon_default_fun(args.get("npc_icon","STEVE"))
        text = args.get("text")
        step_index = int(args.get("step_index",0))
        buttons = args.get("buttons")
        sound = args.get("sound")
        if sound:
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(LevelId)
            comp.PlayCustomUIMusic(sound, 1, 1, False)

        if all([dialogue_id,npc_name,npc_icon,text,buttons]) and step_index>=0:
            if self.ui_npcdialog is None:
                self.ui_npcdialog = clientApi.PushScreen(modName, 'npcdialog', {"isHud": 1, 'data': {}, 'client': self})
            if self.ui_npcdialog is not None:
                self.ui_npcdialog.SetData(dialogue_id, npc_name, npc_icon, text, step_index, buttons)
        else:
            print "[ERROR] OpenDialogue",args
    
    def PauseDialogue(self, args):
        if self.ui_npcdialog is not None:
            clientApi.PopScreen()
            self.ui_npcdialog = None
    
    def NotifyToServerF(self,event,args):
        print "NotifyToServerF",event,args
        self.NotifyToServer(event,args)

    def npc_icon_default_fun(self,icon):
        # 进行路径转换
        if "/" in icon:
            # 则为路径
            if icon[0] == "/":
               icon = icon[1:]  
            return icon
        else:
            if not icon in self.npc_icon_default:
                icon = "STEVE"
            return "textures/npc/" + icon.lower()


    def on_disable(self):
        print("禁用NpcDialog")
        self.UnListenAllEvents()
