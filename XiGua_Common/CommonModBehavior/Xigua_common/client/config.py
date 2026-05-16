# coding=utf-8
modName = "Xigua_common"
version = "0.0.1"

base_clsPath = "{}.client.".format(modName)
system_dict = {
    "main": base_clsPath + "hud.main.Main",
    "decoration": base_clsPath + "decoration.main.Decoration",
    "text_board": base_clsPath + "text_board.main.TextBoard",
    "npc_dialog": base_clsPath + "npc_dialog.main.NpcDialog",
    "settings": base_clsPath + "xg_settings.settings.Settings",
}


scoreboard_title_image_dict = {
    "超能激战": "cnjz",
    "村庄守卫战": "cs",
    "决斗游戏": "jdyx",
    "饥饿游戏": "je",
    "街机游戏": "jjyx",
    "猎人游戏": "lryx",
    "云庭庄园": "ytzy",
}