# -*- coding: utf-8 -*-
from utils import *


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
        self.PlayerPosInfo = {}  # 玩家位置信息 {"players_pos": {"1": (0, 0, 0)}}
        self.scoreboard_text_dict = dict()
        self.NewPingValue = 0
        self.ping_value = ""
        self.CPS_left_click_set = []
        self.CPS_right_click_set = []
        self.player_info_visible = False
        self.DanmakuCache = {1: 0, 2: 0, 3: 0}
        # 弹幕轨道配置
        self.font_height = 15  # 弹幕字体高度
        self.top_margin = 20  # 顶部安全区
        self.track_count = 5  # 5个轨道
        self.track_offset_range = 2  # 每条弹幕的随机上下偏移范围（±2px）
        self.all_punctuation = dict()
        self.lase_punctuation_time = 0

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

        panel = self.screen.GetBaseUIControl(base_path)
        self.child = self.screen.CreateChildControl("xg_hud.root_panel_watermelon", "root_panel_watermelon", panel)
        self.DanmakuPanel = self.screen.GetBaseUIControl(base_path + "/root_panel_watermelon/danmaku")
        # self.SetScoreboard({"title": "分数板", "order": ("1", "2", "3"), "text_dict": {"1": "志云工作室", "2": "测试", "3": "TEST"}})
        self.screen.GetBaseUIControl(
            base_path + "/root_panel_watermelon/player_info/frame").asImage().SetSpritePlatformFrame()
        self.screen.GetBaseUIControl(
            base_path + "/root_panel_watermelon/player_info/frame/head").asImage().SetSpritePlatformHead()
        self.screen.GetBaseUIControl(
            base_path + "/root_panel_watermelon/player_info/lvl_and_name/name").asLabel().SetText(PlayerName)
        self.screen.GetBaseUIControl(base_path + "/root_panel_watermelon/player_info").SetVisible(False)

    @Listen()
    def OnKeyPressInGame(self, args):
        if (args["screenName"] in ["hud_screen"]) and (args["isDown"] == "1"):
            key = args["key"]
            if key == "-97":
                if self.lase_punctuation_time <= time.time() - 1:
                    self.lase_punctuation_time = time.time()
                    block_list = clientApi.getEntitiesOrBlockFromRay(
                        PosComp.GetPos(),
                        clientApi.GetDirFromRot(RotComp.GetRot()),
                        64,
                        False,
                        enum.RayFilterType.OnlyBlocks
                        )
                    if block_list:
                        block_pos = block_list[0].get("hitPos", (0, 0, 0))
                        self.NotifyToServer("createPunctuation", {"pos": block_pos})
                    else:
                        Game.SetTipMessage("§c标点距离超过64格")

    @Listen(event_type=Listen.server)
    def createPunctuation(self, args):
        pos = args.get("pos")
        if pos in self.all_punctuation:
            return
        punctuationId = TextBoardComp.CreateTextBoardInWorld("\n§a\n§a\n§a", (1, 1, 1, 0.5), (0, 0, 0, 0))
        textId = TextBoardComp.CreateTextBoardInWorld("", (1, 1, 1, 1), (0, 0, 0, 0.8))
        self.all_punctuation[pos] = (punctuationId, textId)
        TextBoardComp.SetBoardPos(punctuationId, pos)
        TextBoardComp.SetBoardPos(textId, (pos[0], pos[1] - 0.2, pos[2]))
        TextBoardComp.SetBoardDepthTest(punctuationId, False)
        TextBoardComp.SetBoardDepthTest(textId, False)
        Music.PlayCustomMusic("punctuation", entityId=PlayerId)
        def callback():
            self.all_punctuation.pop(pos)
            TextBoardComp.RemoveTextBoard(punctuationId)
            TextBoardComp.RemoveTextBoard(textId)
        Game.AddTimer(10, callback)

    def OnTick(self):
        player_pos = PosComp.GetPos()
        for pos, (punctuationId, textId) in self.all_punctuation.items():
            distance, size = calculate_panel_size(player_pos, pos, 1.2, 0.04)
            TextBoardComp.SetBoardScale(punctuationId, (size, size))
            TextBoardComp.SetBoardScale(textId, (size, size))
            TextBoardComp.SetText(textId, "{}m".format(int(distance)))

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
        screen_width, screen_height = Game.GetScreenSize()
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
        screen_width, screen_height = Game.GetScreenSize()
        size_x = child.GetFullSize("x")["absoluteValue"]
        base_x = (screen_width / 2) - (size_x / 2)
        if background:
            child.asImage().SetSprite(background)
        text = child.GetChildByPath("/text").asLabel()
        text.SetText(content)
        child.SetPosition((base_x, base_y))

        def callback():
            self.screen.RemoveChildControl(child)

        Game.AddTimer(7, callback)

    @Listen("SetPlayerInfoVisible", "server")
    def OnSetPlayerInfoVisible(self, visible):
        self.player_info_visible = visible
        if self.ui_create:
            self.screen.GetBaseUIControl(base_path + "/root_panel_watermelon/player_info").asImage().SetVisible(visible)

    @Listen("LeftClickBeforeClientEvent")
    def OnLeftClickBeforeClientEvent(self, args):
        self.CPS_left_click_set.append(time.time())

    @Listen("TapBeforeClientEvent")
    def OnTapBeforeClientEvent(self, args):
        self.CPS_left_click_set.append(time.time())

    @Listen("RightClickBeforeClientEvent")
    def OnRightClickBeforeClientEvent(self, args):
        self.CPS_right_click_set.append(time.time())

    @Listen("players_pos", "server")
    def OnPlayerPosChange(self, args):
        self.PlayerPosInfo = args

    @Listen("ping_value", "server")
    def OnPingValueChange(self, value):
        self.NewPingValue = int((time.time() * 1000 - value["ping_value"])) / 2
        if self.NewPingValue < 20:
            self.NewPingValue = 20

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#player_info.visible")
    def return_player_info_visible(self):
        return self.player_info_visible

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.keyboard_and_mouse")
    def return_input_mode_keyboard_and_mouse(self):
        if CF.CreatePlayerView(PlayerId).GetToggleOption("INPUT_MODE") == 0:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.touch")
    def return_input_mode_touch(self):
        if CF.CreatePlayerView(PlayerId).GetToggleOption("INPUT_MODE") == 1:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#input_mode.controller")
    def return_input_mode_controller(self):
        if CF.CreatePlayerView(PlayerId).GetToggleOption("INPUT_MODE") == 2:
            return True
        return False

    @ViewBinder.binding(ViewBinder.BF_BindString, "#game_info.text")
    def return_game_info_text(self):
        return self.system.game_info_text

    @ViewBinder.binding(ViewBinder.BF_BindString, "#FPS_value")
    def return_FPS_value(self):
        return "FPS:{}".format(int(Game.GetFps()))

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
        ping_list = sorted(PING_ICONS.keys())
        if int(time.time()) % 5 == 0:
            self.ping_value = "§c{}ms".format(self.NewPingValue)
            for ping in ping_list:
                if self.NewPingValue <= ping:
                    self.ping_value = "{}{}ms".format(PING_ICONS[ping]["color"], self.NewPingValue)
                    break
        return self.ping_value

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
            text = text.replace("%death%", str(self.system.death_number)).replace("%kill%", str(self.system.kill_number))
            return text
        except IndexError:
            return "溢出"
        except Exception:
            return "未知错误"

    def OnDestroy(self):
        """
        @description UI销毁时调用
        """
        self.screen.RemoveChildControl(self.child)
        self.ui_create = False

