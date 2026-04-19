# -*- coding: utf-8 -*-
"""
Created on 2025-11-03
服务端系统
"""
from .utils import *


class Main(BaseServer):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)

    @Listen()
    def OnPlayerActionServerEvent(self, args):
        pid = args["playerId"]
        data = {
          "all": {
            "cape_15th": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "15周年披风",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 0,
              "type": "披风",
              "render_name": "controller.render.player.cape_15th",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "cape",
              "rarity": "COMMON"
            },
            "dragon_wings_bloody": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "血煞龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 1,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_bloody",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_chainsketch": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "锁链龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 2,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_chainsketch",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_cottoncandy": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "棉花糖龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 3,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_cottoncandy",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_default": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "默认龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 4,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_default",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_gold": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "黄金龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 5,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_gold",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_grap": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "葡萄龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 6,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_grap",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_green": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "翠绿龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 7,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_green",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_greyscale": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "灰度龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 8,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_greyscale",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_lemon": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "柠檬龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 9,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_lemon",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_light_blue": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "淡蓝龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 10,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_light_blue",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_phantom": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "is_new": True,
              "name": "幻影龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 11,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_phantom",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_puperice": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "紫冰龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 12,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_puperice",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_purple": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "紫罗兰龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 13,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_purple",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_red": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "赤红龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 14,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_sea": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "海洋龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 15,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_sky": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "is_hot": True,
              "name": "天空龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 16,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_sky",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_sunset": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "日落龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 17,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_sunset",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_turtle": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "灵龟龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 18,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            },
            "dragon_wings_autumn": {
              "bg": "textures/ui/pet_rarity/panel_0{}@3x".format(random.randint(1, 5)),
              "name": "秋日龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 0,
              "type": "翅膀",
              "render_name": "controller.render.player.dragon_wings_autumn",
              "render_condition": "!variable.is_first_person && !query.is_spectator",
              "slot": "wings",
              "rarity": "COMMON"
            }
          },
          "has": {
            "cape_15th": {
              "expireTime": None,
              "isEquipped": False,
              "acquiredTime": 1776380967000
            },
            "dragon_wings_default": {
              "expireTime": None,
              "isEquipped": False,
              "acquiredTime": 1776380967000
            },
            "dragon_wings_lemon": {
              "expireTime": None,
              "isEquipped": False,
              "acquiredTime": 1776380967000
            }
          },
          "dressed": {
            "pid": ["15th_cape"]
          }
        }
        self.NotifyToClient(pid, "openDressingRoom", data)
        #self.NotifyToClient(pid, "setText", {"item_id": "text", "text": "测试设置文本"})
        #self.NotifyToClient(pid, "setTextColor", {"item_id": "text", "color": [1, 1, 1]})
        #self.NotifyToClient(pid, "setBackground", {"item_id": "text", "background": "textures/netease/common/image/default"})
        #self.NotifyToClient(pid, "setImage", {"item_id": "image", "texture": "textures/ui/Add-Ons_8x8"})
        #self.NotifyToClient(pid, "setImageColor", {"item_id": "image", "color": [0, 1, 0]})
