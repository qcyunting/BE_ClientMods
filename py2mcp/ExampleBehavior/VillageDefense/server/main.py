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
        self.NotifyToClient(pid, "openShop", {
  "potion": [
    {
      "slot": 9,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 200,
          "name": "瞬间治疗I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 800,
          "name": "瞬间治疗II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1800,
          "name": "瞬间治疗III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 3200,
          "name": "瞬间治疗IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 5000,
          "name": "瞬间治疗V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 7200,
          "name": "瞬间治疗VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 9800,
          "name": "瞬间治疗VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 12800,
          "name": "瞬间治疗VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 16200,
          "name": "瞬间治疗IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 20000,
          "name": "瞬间治疗X"
        }
      ],
      "maxLevel": 3
    },
    {
      "slot": 10,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 180,
          "name": "迅捷I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 720,
          "name": "迅捷II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1620,
          "name": "迅捷III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 2880,
          "name": "迅捷IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 4500,
          "name": "迅捷V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 6480,
          "name": "迅捷VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 8820,
          "name": "迅捷VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 11520,
          "name": "迅捷VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 14580,
          "name": "迅捷IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 18000,
          "name": "迅捷X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 11,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 170,
          "name": "迟缓I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 680,
          "name": "迟缓II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1530,
          "name": "迟缓III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 2720,
          "name": "迟缓IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 4250,
          "name": "迟缓V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 6120,
          "name": "迟缓VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 8330,
          "name": "迟缓VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 10880,
          "name": "迟缓VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 13770,
          "name": "迟缓IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 17000,
          "name": "迟缓X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 12,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 220,
          "name": "力量I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 880,
          "name": "力量II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1980,
          "name": "力量III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 3520,
          "name": "力量IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 5500,
          "name": "力量V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 7920,
          "name": "力量VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 10780,
          "name": "力量VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 14080,
          "name": "力量VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 17820,
          "name": "力量IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 22000,
          "name": "力量X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 13,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 160,
          "name": "虚弱I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 640,
          "name": "虚弱II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1440,
          "name": "虚弱III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 2560,
          "name": "虚弱IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 4000,
          "name": "虚弱V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 5760,
          "name": "虚弱VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 7840,
          "name": "虚弱VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 10240,
          "name": "虚弱VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 12960,
          "name": "虚弱IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 16000,
          "name": "虚弱X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 14,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 210,
          "name": "再生I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 840,
          "name": "再生II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1890,
          "name": "再生III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 3360,
          "name": "再生IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 5250,
          "name": "再生V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 7560,
          "name": "再生VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 10290,
          "name": "再生VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 13440,
          "name": "再生VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 17010,
          "name": "再生IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 21000,
          "name": "再生X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 15,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 175,
          "name": "跳跃提升I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 700,
          "name": "跳跃提升II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 1575,
          "name": "跳跃提升III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 2800,
          "name": "跳跃提升IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 4375,
          "name": "跳跃提升V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 6300,
          "name": "跳跃提升VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 8575,
          "name": "跳跃提升VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 11200,
          "name": "跳跃提升VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 14175,
          "name": "跳跃提升IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 17500,
          "name": "跳跃提升X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 16,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 260,
          "name": "隐身I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 1040,
          "name": "隐身II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 2340,
          "name": "隐身III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 4160,
          "name": "隐身IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 6500,
          "name": "隐身V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 9360,
          "name": "隐身VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 12740,
          "name": "隐身VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 16640,
          "name": "隐身VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 21060,
          "name": "隐身IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 26000,
          "name": "隐身X"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 17,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potion",
          "price": 240,
          "name": "火焰抗性I"
        },
        {
          "slot": 1,
          "item": "minecraft:potion",
          "price": 960,
          "name": "火焰抗性II"
        },
        {
          "slot": 2,
          "item": "minecraft:potion",
          "price": 2160,
          "name": "火焰抗性III"
        },
        {
          "slot": 3,
          "item": "minecraft:potion",
          "price": 3840,
          "name": "火焰抗性IV"
        },
        {
          "slot": 4,
          "item": "minecraft:potion",
          "price": 6000,
          "name": "火焰抗性V"
        },
        {
          "slot": 5,
          "item": "minecraft:potion",
          "price": 8640,
          "name": "火焰抗性VI"
        },
        {
          "slot": 6,
          "item": "minecraft:potion",
          "price": 11760,
          "name": "火焰抗性VII"
        },
        {
          "slot": 7,
          "item": "minecraft:potion",
          "price": 15360,
          "name": "火焰抗性VIII"
        },
        {
          "slot": 8,
          "item": "minecraft:potion",
          "price": 19440,
          "name": "火焰抗性IX"
        },
        {
          "slot": 9,
          "item": "minecraft:potion",
          "price": 24000,
          "name": "火焰抗性X"
        }
      ],
      "maxLevel": 0
    }
  ],
  "armor": [
    {
      "slot": 0,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:leather_helmet",
          "price": 80,
          "name": "皮革头盔"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_helmet",
          "price": 180,
          "name": "铁质头盔"
        },
        {
          "slot": 2,
          "item": "minecraft:diamond_helmet",
          "price": 380,
          "name": "钻石头盔"
        },
        {
          "slot": 3,
          "item": "minecraft:netherite_helmet",
          "price": 750,
          "name": "下界合金头盔"
        }
      ],
      "maxLevel": 2
    },
    {
      "slot": 1,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:leather_chestplate",
          "price": 100,
          "name": "皮革胸甲"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_chestplate",
          "price": 220,
          "name": "铁质胸甲"
        },
        {
          "slot": 2,
          "item": "minecraft:diamond_chestplate",
          "price": 450,
          "name": "钻石胸甲"
        },
        {
          "slot": 3,
          "item": "minecraft:netherite_chestplate",
          "price": 850,
          "name": "下界合金胸甲"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 2,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:leather_leggings",
          "price": 90,
          "name": "皮革护腿"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_leggings",
          "price": 200,
          "name": "铁质护腿"
        },
        {
          "slot": 2,
          "item": "minecraft:diamond_leggings",
          "price": 420,
          "name": "钻石护腿"
        },
        {
          "slot": 3,
          "item": "minecraft:netherite_leggings",
          "price": 800,
          "name": "下界合金护腿"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 3,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:leather_boots",
          "price": 70,
          "name": "皮革靴子"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_boots",
          "price": 160,
          "name": "铁质靴子"
        },
        {
          "slot": 2,
          "item": "minecraft:diamond_boots",
          "price": 350,
          "name": "钻石靴子"
        },
        {
          "slot": 3,
          "item": "minecraft:netherite_boots",
          "price": 700,
          "name": "下界合金靴子"
        }
      ],
      "maxLevel": 0
    }
  ],
  "weapon": [
    {
      "slot": 4,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:stone_sword",
          "price": 60,
          "name": "石质剑"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_sword",
          "price": 150,
          "name": "铁质剑"
        },
        {
          "slot": 2,
          "item": "minecraft:diamond_sword",
          "price": 360,
          "name": "钻石剑"
        },
        {
          "slot": 3,
          "item": "minecraft:netherite_sword",
          "price": 720,
          "name": "下界合金剑"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 5,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:trident",
          "price": 260,
          "name": "普通三叉戟"
        },
        {
          "slot": 1,
          "item": "minecraft:trident",
          "price": 520,
          "name": "激流忠诚三叉戟"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 6,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:bow",
          "price": 120,
          "name": "普通弓"
        },
        {
          "slot": 1,
          "item": "minecraft:bow",
          "price": 280,
          "name": "力量I弓"
        },
        {
          "slot": 2,
          "item": "minecraft:bow",
          "price": 600,
          "name": "无限力量弓"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 7,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:crossbow",
          "price": 150,
          "name": "普通弩"
        },
        {
          "slot": 1,
          "item": "minecraft:crossbow",
          "price": 320,
          "name": "穿透I弩"
        },
        {
          "slot": 2,
          "item": "minecraft:crossbow",
          "price": 650,
          "name": "穿透多重弩"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 8,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:arrow",
          "price": 35,
          "name": "普通箭"
        },
        {
          "slot": 1,
          "item": "minecraft:tipped_arrow",
          "price": 160,
          "name": "迟缓药箭"
        },
        {
          "slot": 2,
          "item": "minecraft:tipped_arrow",
          "price": 320,
          "name": "剧毒药箭"
        }
      ],
      "maxLevel": 0
    }
  ],
  "food": [
    {
      "slot": 27,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:apple",
          "price": 60,
          "name": "苹果"
        },
        {
          "slot": 1,
          "item": "minecraft:baked_potato",
          "price": 120,
          "name": "烤土豆"
        },
        {
          "slot": 2,
          "item": "minecraft:golden_apple",
          "price": 450,
          "name": "金苹果"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 28,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:beef",
          "price": 50,
          "name": "生牛肉"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_beef",
          "price": 130,
          "name": "熟牛排"
        },
        {
          "slot": 2,
          "item": "minecraft:enchanted_golden_apple",
          "price": 680,
          "name": "附魔金苹果"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 29,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:chicken",
          "price": 45,
          "name": "生鸡肉"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_chicken",
          "price": 110,
          "name": "熟鸡肉"
        },
        {
          "slot": 2,
          "item": "minecraft:pumpkin_pie",
          "price": 280,
          "name": "南瓜派"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 30,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:bread",
          "price": 70,
          "name": "面包"
        },
        {
          "slot": 1,
          "item": "minecraft:carrot",
          "price": 55,
          "name": "胡萝卜"
        },
        {
          "slot": 2,
          "item": "minecraft:golden_carrot",
          "price": 320,
          "name": "金胡萝卜"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 31,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:porkchop",
          "price": 48,
          "name": "生猪排"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_porkchop",
          "price": 125,
          "name": "熟猪排"
        },
        {
          "slot": 2,
          "item": "minecraft:mushroom_stew",
          "price": 240,
          "name": "蘑菇煲"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 32,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:potato",
          "price": 40,
          "name": "土豆"
        },
        {
          "slot": 1,
          "item": "minecraft:sweet_berries",
          "price": 65,
          "name": "甜浆果"
        },
        {
          "slot": 2,
          "item": "minecraft:rabbit_stew",
          "price": 260,
          "name": "兔肉煲"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 33,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:rabbit",
          "price": 42,
          "name": "生兔肉"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_rabbit",
          "price": 115,
          "name": "熟兔肉"
        },
        {
          "slot": 2,
          "item": "minecraft:honey_bottle",
          "price": 220,
          "name": "蜂蜜瓶"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 34,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:cod",
          "price": 44,
          "name": "生鳕鱼"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_cod",
          "price": 105,
          "name": "熟鳕鱼"
        },
        {
          "slot": 2,
          "item": "minecraft:pufferfish",
          "price": 180,
          "name": "河豚"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 35,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:salmon",
          "price": 46,
          "name": "生三文鱼"
        },
        {
          "slot": 1,
          "item": "minecraft:cooked_salmon",
          "price": 118,
          "name": "熟三文鱼"
        },
        {
          "slot": 2,
          "item": "minecraft:tropical_fish",
          "price": 160,
          "name": "热带鱼"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 36,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:melon_slice",
          "price": 52,
          "name": "西瓜片"
        },
        {
          "slot": 1,
          "item": "minecraft:dried_kelp",
          "price": 58,
          "name": "干海带"
        },
        {
          "slot": 2,
          "item": "minecraft:cookie",
          "price": 95,
          "name": "曲奇"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 37,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:beetroot",
          "price": 38,
          "name": "甜菜根"
        },
        {
          "slot": 1,
          "item": "minecraft:beetroot_soup",
          "price": 210,
          "name": "甜菜汤"
        },
        {
          "slot": 2,
          "item": "minecraft:cake",
          "price": 350,
          "name": "蛋糕"
        }
      ],
      "maxLevel": 0
    }
  ],
  "other": [
    {
      "slot": 18,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:enchanted_book",
          "price": 220,
          "name": "保护 I"
        },
        {
          "slot": 1,
          "item": "minecraft:enchanted_book",
          "price": 230,
          "name": "火焰保护 I"
        },
        {
          "slot": 2,
          "item": "minecraft:enchanted_book",
          "price": 230,
          "name": "弹射物保护 I"
        },
        {
          "slot": 3,
          "item": "minecraft:enchanted_book",
          "price": 200,
          "name": "锋利 I"
        },
        {
          "slot": 4,
          "item": "minecraft:enchanted_book",
          "price": 190,
          "name": "击退 I"
        },
        {
          "slot": 5,
          "item": "minecraft:enchanted_book",
          "price": 210,
          "name": "火焰附加 I"
        },
        {
          "slot": 6,
          "item": "minecraft:enchanted_book",
          "price": 200,
          "name": "力量 I"
        },
        {
          "slot": 7,
          "item": "minecraft:enchanted_book",
          "price": 190,
          "name": "冲击 I"
        },
        {
          "slot": 8,
          "item": "minecraft:enchanted_book",
          "price": 210,
          "name": "火矢 I"
        },
        {
          "slot": 9,
          "item": "minecraft:enchanted_book",
          "price": 220,
          "name": "穿透 I"
        },
        {
          "slot": 10,
          "item": "minecraft:enchanted_book",
          "price": 260,
          "name": "多重射击 I"
        },
        {
          "slot": 11,
          "item": "minecraft:enchanted_book",
          "price": 180,
          "name": "耐久 I"
        },
        {
          "slot": 12,
          "item": "minecraft:enchanted_book",
          "price": 380,
          "name": "经验修补 I"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 19,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:fishing_rod",
          "price": 120,
          "name": "钓鱼竿"
        },
        {
          "slot": 1,
          "item": "minecraft:ender_pearl",
          "price": 350,
          "name": "末影珍珠"
        },
        {
          "slot": 2,
          "item": "minecraft:totem_of_undying",
          "price": 680,
          "name": "不死图腾"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 20,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:shield",
          "price": 140,
          "name": "普通盾牌"
        },
        {
          "slot": 1,
          "item": "minecraft:shield",
          "price": 260,
          "name": "精致装饰盾牌"
        },
        {
          "slot": 2,
          "item": "minecraft:shield",
          "price": 480,
          "name": "满级附魔盾牌"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 21,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:book",
          "price": 40,
          "name": "普通书本"
        },
        {
          "slot": 1,
          "item": "minecraft:lapis_lazuli",
          "price": 90,
          "name": "青金石"
        }
      ],
      "maxLevel": 0
    },
    {
      "slot": 22,
      "data": [
        {
          "slot": 0,
          "item": "minecraft:pillager_spawn_egg",
          "price": 600,
          "name": "生成弩手"
        },
        {
          "slot": 1,
          "item": "minecraft:iron_golem_spawn_egg",
          "price": 1800,
          "name": "生成机械傀儡"
        }
      ],
      "maxLevel": 0
    }
  ],
  "player_coin": 20
})

    @Listen(event_type=Listen.client)
    def UiInitFinished(self, args):
        pid = args["__id__"]

    @Listen(event_type=Listen.client)
    def goodsButtonClick(self, args):
        pid = args["__id__"]