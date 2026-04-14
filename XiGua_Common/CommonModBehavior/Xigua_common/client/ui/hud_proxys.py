# -*- coding: utf-8 -*-
from ..utils.listen_util import *
from ..utils.ui_utils import *
from ..utils import escape
escapeInstance = escape.instance
import time
import random


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
        self.scoreboard_text_dict = dict()
        self.NewPingValue = -1
        self.ping_value = ""
        self.all_player_ping = dict()
        self.CPS_left_click_set = []
        self.CPS_right_click_set = []
        self.player_info_visible = False
        self.DanmakuCache = {1: 0, 2: 0, 3: 0}
        # 弹幕轨道配置
        self.font_height = 15  # 弹幕字体高度
        self.top_margin = 20  # 顶部安全区
        self.track_count = 5  # 5个轨道
        self.track_offset_range = 2  # 每条弹幕的随机上下偏移范围（±2px）

        self.health_max = 20
        self.health_now = 20
        self.hunger_max = 20
        self.hunger_now = 20

        self.top_bar_dict = {}
        self.top_bar_control = None

    def OnCreate(self):
        self.ui_create = True
        if self.screen is None:
            return

        # 计算每个轨道的基准Y坐标
        self.track_base_positions = [
            self.top_margin + (i * self.font_height)
            for i in range(self.track_count)
        ]

        # 轨道占用管理（记录弹幕结束时间）
        self.track_available_time = [0] * self.track_count  # 轨道可再次使用的时间戳
        self.track_available_time_top = [0] * self.track_count  # 轨道可再次使用的时间戳

        panel = self.screen.GetBaseUIControl(BP)
        self.child = self.screen.CreateChildControl("xg_hud.root_panel_watermelon", "root_panel_watermelon", panel)
        self.DanmakuPanel = self.screen.GetBaseUIControl(BP + "/root_panel_watermelon/danmaku")
        # self.SetScoreboard({"title": "分数板", "order": ("1", "2", "3"), "text_dict": {"1": "志云工作室", "2": "测试", "3": "TEST"}})

    @Listen(event_type=Listen.server)
    def initTopBar(self, args):
        """
        args: {
            "item_id": {
                "index": 0,
                "type": "text",
                "background": "textures/ui/hud_tip_text_background",
                "color": [1, 1, 1],
                "text": "文本"
            },
            "item_id": {
                "index": 1,
                "type": "image",
                "background": "textures/ui/hud_tip_text_background",
                "text": "文本",
                "text_color": [1, 1, 1],
                "image_color": [1, 1, 1],
                "texture": "textures/ui/image"
            },
            "item_id": {
                "index": 2,
                "type": "progress_bar",
                "color": [1, 1, 1],
                "bar_texture": "textures/ui/image",
                "bar_background": "textures/ui/image"
            }
        }
        """
        self.top_bar_dict = args
        # 先删除旧的
        top_bar = self.screen.GetBaseUIControl(BP + "/root_panel_watermelon/top_bar")
        self.screen.RemoveChildControl(top_bar)
        # 创建新的
        self.top_bar_control = self.screen.CreateChildControl("xg_hud.top_bar", "top_bar", self.child)

        # 根据 index 排序后遍历
        sorted_items = sorted(self.top_bar_dict.items(), key=lambda x: x[1].get("index", 0))

        for item_id, control in sorted_items:
            c_type = control.get("type", "text")
            defName = "xg_hud.top_bar_" + c_type
            child = self.screen.CreateChildControl(defName, item_id, self.top_bar_control)
            self.setTopBarControl(control, child)
            self.top_bar_dict[item_id]["child"] = child

    @Listen(event_type=Listen.server)
    def updateTopBar(self, args):
        for item_id, control in args.items():
            item = self.top_bar_dict.get(item_id, dict()).get("child")
            if item:
                self.setTopBarControl(control, item)

    def setTopBarControl(self, control, child):
        # 设置内容
        _type = control.get("type", "text")
        if _type == "text":
            if control.get("text"):
                child.GetChildByPath("/image/text").asLabel().SetText(control.get("text"))
            if control.get("background"):
                child.GetChildByPath("/image").asImage().SetSprite(control.get("background"))
            if control.get("color"):
                child.GetChildByPath("/image/text").asLabel().SetTextColor(control.get("color"))
        if _type == "image":
            if control.get("text"):
                child.GetChildByPath("/image/text").asLabel().SetText(control.get("text"))
            if control.get("background"):
                child.GetChildByPath("/image").asImage().SetSprite(control.get("background"))
            if control.get("texture"):
                child.GetChildByPath("/image/image").asImage().SetSprite(control.get("texture"))
            if control.get("color"):
                child.GetChildByPath("/image/image").asImage().SetSpriteColor(control.get("color"))
        if _type == "progress_bar":
            pass

    @Listen(event_type=Listen.server)
    def setText(self, args):
        control_id = args["item_id"]
        text = args["text"]
        control = self.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.top_bar_dict[control_id]["text"] = text
            control.GetChildByPath("/image/text").asLabel().SetText(text)

    @Listen(event_type=Listen.server)
    def setTextColor(self, args):
        control_id = args["item_id"]
        color = args["color"]
        control = self.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.top_bar_dict[control_id]["color"] = color
            control.GetChildByPath("/image/text").asLabel().SetTextColor(color)

    @Listen(event_type=Listen.server)
    def setBackground(self, args):
        control_id = args["item_id"]
        background = args["background"]
        control = self.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.top_bar_dict[control_id]["background"] = background
            control.GetChildByPath("/image").asImage().SetSprite(background)

    @Listen(event_type=Listen.server)
    def setImage(self, args):
        control_id = args["item_id"]
        texture = args["texture"]
        control = self.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.top_bar_dict[control_id]["texture"] = texture
            control.GetChildByPath("/image/image").asImage().SetSprite(texture)

    @Listen(event_type=Listen.server)
    def setImageColor(self, args):
        control_id = args["item_id"]
        color = tuple(args["color"])
        control = self.top_bar_dict.get(control_id, {}).get("child")
        if control:
            self.top_bar_dict[control_id]["color"] = color
            control.GetChildByPath("/image/image").asImage().SetSpriteColor(color)

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#health_percentage")
    def health_percentage(self):
        self.health_max = attrComp(playerId).GetAttrMaxValue(MC_Enum.AttrType.HEALTH)
        self.health_now = attrComp(playerId).GetAttrValue(MC_Enum.AttrType.HEALTH)
        return self.health_now / self.health_max

    @ViewBinder.binding(ViewBinder.BF_BindString, "#health_percentage_text")
    def health_percentage_text(self):
        return str(int(self.health_now)) + "/" + str(int(self.health_max))

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#hunger_percentage")
    def hunger_percentage(self):
        self.hunger_max = attrComp(playerId).GetAttrMaxValue(MC_Enum.AttrType.HUNGER)
        self.hunger_now = attrComp(playerId).GetAttrValue(MC_Enum.AttrType.HUNGER)
        return self.hunger_now / self.hunger_max

    @ViewBinder.binding(ViewBinder.BF_BindString, "#hunger_percentage_text")
    def hunger_percentage_text(self):
        return str(int(self.hunger_now)) + "/" + str(int(self.hunger_max))

    @Listen("NewDanmaku", "server")
    def OnNewDanmaku(self, args):
        content = args["content"]
        danmaku_type = args.get("danmaku_type", "scroll")
        background = args.get("background")
        if danmaku_type == "SCROLL":
            self.CreateScrollDanmaku(content, background)
        elif danmaku_type == "UP":
            self.CreateUPDanmaku(content, background)

    def CreateScrollDanmaku(self, content, background):
        child_name = "danmaku_text_{}".format(time.time())
        child = self.screen.CreateChildControl("xg_hud.danmaku_text", child_name, self.DanmakuPanel)
        screen_width, screen_height = gameComp.GetScreenSize()
        size_x = child.GetFullSize("x")["absoluteValue"]
        size_y = self.font_height  # 固定高度15px

        # 1. 智能选择轨道（LRU策略：优先选择最久未使用的轨道）
        current_time = time.time()
        track_index = min(range(self.track_count), key=lambda i: self.track_available_time[i])

        # 2. 计算弹幕的Y坐标（基准轨道位置 + 随机偏移）
        base_y = self.track_base_positions[track_index]
        random_offset = random.randint(-self.track_offset_range, self.track_offset_range)
        final_y = max(self.top_margin, min(base_y + random_offset, screen_height - size_y))  # 确保不超出屏幕

        # 3. 计算动画时长和轨道占用时间
        speed = random.randint(1, 4) * 0.01 + 0.03  # 像素/ms（可调整弹幕速度）
        animation_duration = (screen_width + size_x) * speed
        self.track_available_time[track_index] = current_time + animation_duration

        # 4. 设置动画
        animation = {
            "namespace": "danmaku",
            "danmaku_text_offset": {
                "anim_type": "offset",
                "duration": animation_duration,
                "from": [screen_width, final_y],
                "to": [0 - size_x, final_y],
                "next": "",
            },
        }
        clientApi.RegisterUIAnimations(animation)

        def callback():
            self.screen.RemoveChildControl(child)

        child.SetAnimEndCallback("danmaku_text_offset", callback)
        child.SetAnimation("offset", "danmaku", "danmaku_text_offset", True)
        if background:
            child.asImage().SetSprite(background)
        text = child.GetChildByPath("/text").asLabel()
        text.SetText(content)

    def CreateUPDanmaku(self, content, background):
        child_name = "danmaku_text_{}".format(time.time())
        child = self.screen.CreateChildControl("xg_hud.danmaku_text", child_name, self.DanmakuPanel)
        track_index = min(range(self.track_count), key=lambda i: self.track_available_time_top[i])
        self.track_available_time_top[track_index] = time.time() + 7

        # 计算弹幕的Y坐标
        base_y = self.track_base_positions[track_index]
        screen_width, screen_height = gameComp.GetScreenSize()
        size_x = child.GetFullSize("x")["absoluteValue"]
        base_x = (screen_width / 2) - (size_x / 2)
        if background:
            child.asImage().SetSprite(background)
        text = child.GetChildByPath("/text").asLabel()
        text.SetText(content)
        child.SetPosition((base_x, base_y))

        def callback():
            self.screen.RemoveChildControl(child)

        gameComp.AddTimer(7, callback)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#hud_button_click")
    def OnButtonClick(self, args):
        parts = args["ButtonPath"].split('/')
        result = parts[-2]
        if result == "pause_button":
            clientApi.OpenPauseGui()
        elif result == "chat_button":
            clientApi.OpenChatGui()

    @Listen("LeftClickBeforeClientEvent")
    def OnLeftClickBeforeClientEvent(self, args):
        self.CPS_left_click_set.append(time.time())

    @Listen("TapBeforeClientEvent")
    def OnTapBeforeClientEvent(self, args):
        self.CPS_left_click_set.append(time.time())

    @Listen("RightClickBeforeClientEvent")
    def OnRightClickBeforeClientEvent(self, args):
        self.CPS_right_click_set.append(time.time())

    @Listen(event_name="ping_update", event_type="Xigua_common", system_name="main")
    def OnPingValueChange(self, args):
        self.all_player_ping = args
        for name, info in args.items():
            if name == playerName:
                self.NewPingValue = info.get("value")

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#player_info.visible")
    def return_player_info_visible(self):
        return self.player_info_visible

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.keyboard_and_mouse")
    def return_input_mode_keyboard_and_mouse(self):
        if CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 0:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.touch")
    def return_input_mode_touch(self):
        if CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 1:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.controller")
    def return_input_mode_controller(self):
        if CF.CreatePlayerView(playerId).GetToggleOption("INPUT_MODE") == 2:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindString, "#game_info.text")
    def return_game_info_text(self):
        return self.system.game_info_text

    @ViewBinder.binding(ViewBinder.BF_BindString, "#FPS_value")
    def return_FPS_value(self):
        return "FPS:{}".format(int(gameComp.GetFps()))

    @ViewBinder.binding(ViewBinder.BF_BindString, "#CPS_value")
    def return_CPS_value(self):
        now = time.time()
        for left in self.CPS_left_click_set:
            if now - left > 1:
                self.CPS_left_click_set.remove(left)
                continue
        for right in self.CPS_right_click_set:
            if now - right > 1:
                self.CPS_right_click_set.remove(right)
                continue
        left_cps = len(self.CPS_left_click_set)
        right_cps = len(self.CPS_right_click_set)
        if left_cps == 0 and right_cps == 0:
            return ""
        elif left_cps == 0:
            return "CPS:0|{}".format(right_cps)
        elif right_cps == 0:
            return "CPS:{}".format(left_cps)
        else:
            return "CPS:{}|{}".format(left_cps, right_cps)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#ping_value")
    def return_ping_value(self):
        PING_ICONS = {
            100: {"color": "§a"},
            200: {"color": "§e"},
            300: {"color": "§6"},
            400: {"color": "§c"}
        }
        ping_list = sorted(PING_ICONS.keys())
        if self.NewPingValue == -1:
            return ""
        ping_value = "延迟: §c{}ms".format(self.NewPingValue)
        for ping in ping_list:
            if self.NewPingValue <= ping:
                ping_value = "延迟: {}{}ms".format(PING_ICONS[ping]["color"], self.NewPingValue)
                break
        return ping_value

    @Listen(event_type=Listen.server)
    def SetScoreboard(self, args):
        """
        设置分数板数据
        """
        self.scoreboard_text_dict = args

    @Listen(event_type=Listen.server)
    def AddScoreboardText(self, args):
        """
        创建分数板文本
        """
        for name, text in args.items():
            order = self.scoreboard_text_dict.setdefault("order", (name,))
            order = list(order)
            order.append(name)
            text_dict = self.scoreboard_text_dict.setdefault("text_dict", {})
            text_dict[name] = text
            self.scoreboard_text_dict["order"] = tuple(order)
            self.scoreboard_text_dict["text_dict"] = text_dict

    @Listen(event_type=Listen.server)
    def RemoveScoreboardText(self, args):
        """
        移除分数板文本
        """
        for name in args.values():
            order = self.scoreboard_text_dict.get("order", ())
            text_dict = self.scoreboard_text_dict.get("text_dict", {})
            if name in order:
                order = list(order)
                order.remove(name)
                self.scoreboard_text_dict["order"] = tuple(order)
            if name in text_dict:
                text_dict.pop(name)
                self.scoreboard_text_dict["text_dict"] = text_dict

    @Listen(event_type=Listen.server)
    def SetScoreboardText(self, args):
        """
        设置分数板文本
        """
        name, text = args["name"], args["text"]
        text_dict = self.scoreboard_text_dict.setdefault("text_dict", {})
        text_dict[name] = text
        self.scoreboard_text_dict["text_dict"] = text_dict

    @Listen(event_type=Listen.server)
    def SetScoreboardTitle(self, args):
        """
        设置分数板文本
        """
        self.scoreboard_text_dict["title"] = args["title"]

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#scoreboard_panel.visible")
    def return_scoreboard_visible(self):
        if self.scoreboard_text_dict.get("order"):
            return True
        else:
            return False

    @ViewBinder.binding(ViewBinder.BF_BindString, "#scoreboard_panel.title")
    def return_scoreboard_title(self):
        return self.scoreboard_text_dict.get("title", "")

    @ViewBinder.binding(ViewBinder.BF_BindInt, "#scoreboard_panel.item_count")
    def return_scoreboard_item_count(self):
        return len(self.scoreboard_text_dict.get("order", ""))

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "scoreboard_collection", "#scoreboard_panel.text")
    def return_scoreboard_text(self, index):
        try:
            item_id = self.scoreboard_text_dict.get("order", "")[index]
            text = self.scoreboard_text_dict.get("text_dict", {}).get(item_id, "无")
            return text
        except IndexError:
            return "溢出"
        except Exception as e:
            logger.error(e)
            return "未知错误"

    def OnDestroy(self):
        """
        @description UI销毁时调用
        """
        self.screen.RemoveChildControl(self.child)
        self.ui_create = False

