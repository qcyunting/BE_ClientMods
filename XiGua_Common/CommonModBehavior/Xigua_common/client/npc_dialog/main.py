# coding=utf-8
from ..utils.ClientSystem_utils import *


class NpcDialog(BaseSystem):
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
        super(NpcDialog, self).__init__(namespace, systemName)

        self.ui_npcdialog = None

    @Listen()
    def UiInitFinished(self,args):
        clientApi.RegisterUI(modName, 'npcdialog', "{}.client.npc_dialog.ui.NpcDialog.Main".format(modName),"npcdialog.main")

    @Listen()
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

    @Listen(event_type=Listen.server)
    def OpenDialogue(self, args):
        dialogue_id = args.get("dialogue_id")
        npc_name = args.get("npc_name")
        npc_icon = self.npc_icon_default_fun(args.get("npc_icon","STEVE"))
        text = args.get("text")
        step_index = int(args.get("step_index",0))
        buttons = args.get("buttons")
        sound = args.get("sound")
        if sound:
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            comp.PlayCustomUIMusic(sound, 1, 1, False)

        if all([dialogue_id,npc_name,npc_icon,text,buttons]) and step_index>=0:
            if self.ui_npcdialog is None:
                self.ui_npcdialog = clientApi.PushScreen(modName, 'npcdialog', {"isHud": 1, 'data': {}, 'client': self})
            def ui_npcdialogF():
                self.ui_npcdialog.SetData(dialogue_id,npc_name,npc_icon,text,step_index,buttons)
            comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1,ui_npcdialogF())
        else:
            print "[ERROR] OpenDialogue",args

    @Listen(event_type=Listen.server)
    def PauseDialogue(self,args):
        # 暂时关闭对话
        if self.ui_npcdialog is not None:
            self.ui_npcdialog = None
            clientApi.PopScreen()
    
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
