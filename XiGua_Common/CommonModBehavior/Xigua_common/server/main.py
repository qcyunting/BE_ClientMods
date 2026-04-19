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
            "dragon_wings_phantom": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "is_new": True,
              "texture": {
                "dragon_wings": "textures/decorations/dragon_wings/dragon_wings_phantom"
              },
              "name": "幻影龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 11,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_sky": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "is_hot": True,
              "texture": {
                "dragon_wings_sky": "textures/decorations/dragon_wings/dragon_wings_sky"
              },
              "name": "天空龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 16,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_sky": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_autumn": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_autumn": "textures/decorations/dragon_wings/dragon_wings_autumn"
              },
              "name": "秋日龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 0,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_autumn": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_purple": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_purple": "textures/decorations/dragon_wings/dragon_wings_purple"
              },
              "name": "紫罗兰龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 13,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_purple": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_green": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_green": "textures/decorations/dragon_wings/dragon_wings_green"
              },
              "name": "翠绿龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 7,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_green": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_sunset": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_sunset": "textures/decorations/dragon_wings/dragon_wings_sunset"
              },
              "name": "日落龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 17,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_sunset": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_grap": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_grap": "textures/decorations/dragon_wings/dragon_wings_grap"
              },
              "name": "葡萄龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 6,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_grap": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_gold": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_gold": "textures/decorations/dragon_wings/dragon_wings_gold"
              },
              "name": "黄金龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 5,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_gold": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "15th_cape": {
              "bg": "textures/ui/pet_rarity/panel_02@3x",
              "texture": {
                "15th_cape": "textures/decorations/cape/15th_anniversary_cape"
              },
              "name": "15周年披风",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 0,
              "type": "披风",
              "render": {
                "controller.render.player.15th_cape": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {},
              "rarity": "COMMON"
            },
            "dragon_wings_puperice": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_puperice": "textures/decorations/dragon_wings/dragon_wings_puperice"
              },
              "name": "紫冰龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 12,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_puperice": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_bloody": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_bloody": "textures/decorations/dragon_wings/dragon_wings_bloody"
              },
              "name": "血煞龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 1,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_bloody": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_red": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_red": "textures/decorations/dragon_wings/dragon_wings_red"
              },
              "name": "赤红龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 14,
              "model": {
                "dragon_wings": "geometry.dragon_wings_red"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_turtle": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_turtle": "textures/decorations/dragon_wings/dragon_wings_turtle"
              },
              "name": "灵龟龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 18,
              "model": {
                "dragon_wings": "geometry.dragon_wings_turtle"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_sea": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_sea": "textures/decorations/dragon_wings/dragon_wings_sea"
              },
              "name": "海洋龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 15,
              "model": {
                "dragon_wings": "geometry.dragon_wings_sea"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_cottoncandy": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_cottoncandy": "textures/decorations/dragon_wings/dragon_wings_cottoncandy"
              },
              "name": "棉花糖龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 3,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_cottoncandy": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_light_blue": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_light_blue": "textures/decorations/dragon_wings/dragon_wings_light_blue"
              },
              "name": "淡蓝龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 10,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_light_blue": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_chainsketch": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_chainsketch": "textures/decorations/dragon_wings/dragon_wings_chainsketch"
              },
              "name": "锁链龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 2,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_chainsketch": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_lemon": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_lemon": "textures/decorations/dragon_wings/dragon_wings_lemon"
              },
              "name": "柠檬龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 9,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_lemon": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_greyscale": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_greyscale": "textures/decorations/dragon_wings/dragon_wings_greyscale"
              },
              "name": "灰度龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 8,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_greyscale": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            },
            "dragon_wings_default": {
              "bg": "textures/ui/pet_rarity/panel_04@3x",
              "texture": {
                "dragon_wings_default": "textures/decorations/dragon_wings/dragon_wings_default"
              },
              "name": "默认龙翼",
              "icon": "textures/ui/pet_icon/hubingbing",
              "index": 4,
              "model": {
                "dragon_wings": "geometry.dragon_wings"
              },
              "type": "翅膀",
              "render": {
                "controller.render.player.dragon_wings_default": "!variable.is_first_person && !query.is_spectator"
              },
              "animation": {
                "dragon_wings": "animation.dragon_wings.idle"
              },
              "animation_controller": {
                "dragon_wings": "controller.animation.decoration.dragon_wings"
              },
              "rarity": "COMMON"
            }
          },
          "has": {
            "15th_cape": {
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
          }
        }
        self.NotifyToClient(pid, "openDressingRoom", data)
        #self.NotifyToClient(pid, "setText", {"item_id": "text", "text": "测试设置文本"})
        #self.NotifyToClient(pid, "setTextColor", {"item_id": "text", "color": [1, 1, 1]})
        #self.NotifyToClient(pid, "setBackground", {"item_id": "text", "background": "textures/netease/common/image/default"})
        #self.NotifyToClient(pid, "setImage", {"item_id": "image", "texture": "textures/ui/Add-Ons_8x8"})
        #self.NotifyToClient(pid, "setImageColor", {"item_id": "image", "color": [0, 1, 0]})
