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

    def on_enable(self):
        print("启用NpcDialog")
        self.ListenForEvent(modName, systemName, "OpenDialogue", self, self.OpenDialogue)
    
    
    def OpenDialogue(self, args):
        print("OpenDialogue",args)
        dialogue_id = args.get("dialogue_id")
        npc_name = args.get("npc_name")
        npc_icon = args.get("npc_icon")
        text = args.get("text")
        step_index = args.get("step_index")
        buttons = args.get("buttons")

        if dialogue_id and npc_name and text and step_index and buttons:
            





    def on_disable(self):
        print("禁用NpcDialog")
        self.UnListenAllEvents()
