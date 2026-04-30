# coding=utf-8
modName = "Xigua_common"
version = "0.0.1"

base_clsPath = "{}.client.".format(modName)
system_dict = {
    "main": base_clsPath + "main.Main",
    "decoration": base_clsPath + "decoration.main.Decoration",
    "text_board": base_clsPath + "text_board.main.TextBoard",
    "npc_dialog": base_clsPath + "npc_dialog.main.NpcDialog",
}