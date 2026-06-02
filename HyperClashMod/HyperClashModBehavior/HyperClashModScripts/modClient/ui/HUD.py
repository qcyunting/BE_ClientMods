# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import time

CF = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
Game = CF.CreateGame(levelId)
from ...modCommon.modConfig import ModName

ScreenNode = clientApi.GetScreenNodeCls()


class HUD(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        print "==== HUD __init__ ===="
        self.param = param
        self.skills = {}
        self.all_cooldown = {}
        self.clientSystem = None
        self._initialized = False
        self._last_click_at = {}

    def Create(self):
        """UI创建成功时调用 - 在这里初始化UI"""
        print "==== HUD Create ===="

        data = self.param.get("data", {})
        self.RefreshSkillData(data)

    def RefreshSkillData(self, data):
        """刷新技能按钮数据"""
        self.skills.clear()
        for skill in data.get("skills", []):
            skillId = skill.get("skillId", "null")
            if not skillId or skillId == "null":
                continue
            icon = skill.get("icon", "")
            try:
                slot = int(skill.get("slot", 1))
            except Exception:
                print "[HUD] Invalid skill slot:", skillId, skill.get("slot", 1)
                continue
            self.skills[skillId] = (slot, icon)

        print self.skills

        # 获取客户端系统。这里失败也不能阻断按钮绑定，点击时会再次尝试获取。
        print "[HUD] Before GetSystem:", ModName, "ShopSystem"
        try:
            self.clientSystem = clientApi.GetSystem(ModName, "ShopSystem")
            print "[HUD] After GetSystem:", self.clientSystem
        except Exception as e:
            self.clientSystem = None
            print "[HUD] GetSystem error:", e

        # 初始化按钮
        print "[HUD] Before _init_buttons"
        try:
            self._init_buttons()
            print "[HUD] After _init_buttons"
        except Exception as e:
            print "[HUD] _init_buttons fatal error:", e
        self._initialized = True

    def _init_buttons(self):
        """初始化所有技能按钮"""
        print "[HUD] _init_buttons start, skills:", self.skills
        for i in range(1, 4):
            button_path = "/skill_button_" + str(i)
            print "[HUD] Hide button lookup:", button_path
            button = self.GetBaseUIControl(button_path)
            if button:
                print "[HUD] Hide button found:", button_path
                button.SetVisible(False)
            else:
                print "[HUD] Button not found:", button_path

        for skillId, (slot, texture) in self.skills.items():
            try:
                print "[HUD] Prepare skill button:", skillId, slot, texture
                if slot < 1 or slot > 3:
                    print "[HUD] Invalid visible slot:", skillId, slot
                    continue

                # 获取按钮控件
                button_path = "/skill_button_" + str(slot)
                print "[HUD] Skill button lookup:", skillId, button_path
                button_control = self.GetBaseUIControl(button_path)
                if not button_control:
                    print "[HUD] Button not found:", button_path
                    continue

                print "[HUD] Skill button found:", skillId, button_path
                button_control.SetVisible(True)
                button_control.SetTouchEnable(True)

                button = button_control.asButton()
                if not button:
                    print "[HUD] Control is not button:", button_path
                    continue
                print "[HUD] Skill button asButton ok:", skillId, button_path

                # 获取图标控件
                icon_path = button_path + "/icon"
                icon_control = self.GetBaseUIControl(icon_path)
                if icon_control:
                    icon = icon_control.asImage()
                    if icon:
                        icon.SetSprite(texture)

                # 为每个按钮单独创建回调
                def make_button_callback(s_id, s_slot, source):
                    def on_button_event(args):
                        print "[HUD] Skill button", source, ":", s_id, s_slot, args
                        try:
                            self._on_skill_button_click(s_id, s_slot, source)
                        except Exception as e:
                            print "[HUD] Skill button callback error:", s_id, e

                    return on_button_event

                def make_touch_callback(s_id, s_slot):
                    def on_touch(args):
                        print "[HUD] Skill button raw touch:", s_id, s_slot, args
                        if args.get("TouchEvent") == 1:
                            try:
                                self._on_skill_button_click(s_id, s_slot, "raw_touch")
                            except Exception as e:
                                print "[HUD] Skill button raw touch error:", s_id, e

                    return on_touch

                # 设置按钮回调
                print "[HUD] Before AddTouchEventParams:", skillId, slot
                button.AddTouchEventParams({"skillId": skillId, "slot": slot, "isSwallow": True})
                print "[HUD] Before SetButtonTouchDownCallback:", skillId, slot
                button.SetButtonTouchDownCallback(make_button_callback(skillId, slot, "touch_down"))
                button.SetButtonTouchUpCallback(make_button_callback(skillId, slot, "touch_up"))
                button_control.SetTouchEventHandler(make_touch_callback(skillId, slot))
                print "[HUD] Bind skill button:", skillId, slot, button_path

            except Exception as e:
                print "[HUD] Error initializing button for skill", skillId, ":", e

    def _on_skill_button_click(self, skillId, slot, source="button"):
        """技能按钮点击处理"""
        now = time.time()
        last = self._last_click_at.get(skillId, 0)
        if now - last < 0.2:
            print "[HUD] Skill button debounce:", skillId, source
            return
        self._last_click_at[skillId] = now
        print "[HUD] Skill button accepted:", skillId, slot, source

        # 检查是否已在冷却中
        if skillId in self.all_cooldown:
            print "[HUD] Skill already in cooldown:", skillId
            return

        if not self.clientSystem:
            self.clientSystem = clientApi.GetSystem(ModName, "ShopSystem")
        if not self.clientSystem:
            print "[HUD] Cannot notify server, ShopSystem not found:", skillId
            return

        # 先通知服务端，避免本地UI控件异常导致技能包发不出去。
        data = {"skillId": skillId, "slot": slot}
        print "[HUD] Before NotifyToServer ClickSkillButton:", data
        try:
            self.clientSystem.NotifyToServer("ClickSkillButton", data)
            print "[HUD] After NotifyToServer ClickSkillButton:", data
        except Exception as e:
            print "[HUD] NotifyToServer ClickSkillButton error:", data, e
            return

        button_path = "/skill_button_" + str(slot)
        self._set_icon_alpha(button_path, 0.5)

    def _set_icon_alpha(self, button_path, alpha):
        icon_control = self.GetBaseUIControl(button_path + "/icon")
        if not icon_control:
            print "[HUD] Icon control not found:", button_path + "/icon"
            return
        icon = icon_control.asImage()
        if icon:
            icon.SetAlpha(alpha)

    def _set_button_text(self, button_path, text):
        text_control = self.GetBaseUIControl(button_path + "/text")
        if not text_control:
            print "[HUD] Text control not found:", button_path + "/text"
            return
        label = text_control.asLabel()
        if label:
            label.SetText(text)

    def UpdateSkillCooldown(self, args):
        """每秒接收冷却值"""
        for skill in args.get('skills', []):
            skillId = skill.get("skillId", '')
            if skillId not in self.skills:
                print "[HUD] Cooldown skill not found:", skillId
                continue
            cooldown = skill.get("cooldown", 0)
            try:
                cooldown = int(cooldown)
            except Exception:
                cooldown = 0
            slot, texture = self.skills[skillId]
            button_path = "/skill_button_" + str(slot)
            if cooldown > 0:
                self.all_cooldown[skillId] = cooldown
                self._set_icon_alpha(button_path, 0.5)
                self._set_button_text(button_path, str(cooldown))
            else:
                if skillId in self.all_cooldown:
                    self.all_cooldown.pop(skillId)
                self._set_icon_alpha(button_path, 1.0)
                self._set_button_text(button_path, '')

    def UpdateStats(self, args):
        for index, stat in enumerate(args.get('stats', [])):
            if index >= 8:
                break
            icon = stat.get("icon", "")
            name = stat.get("name", "")
            path = "/player_game_info_panel/item_button" + str(index)
            icon_control = self.GetBaseUIControl(path + "/icon")
            if icon_control:
                icon_panel = icon_control.asImage()
                if icon_panel:
                    icon_panel.SetSprite(icon)
            text_control = self.GetBaseUIControl(path + "/text")
            if text_control:
                label = text_control.asLabel()
                if label:
                    label.SetText(name)

    def Destroy(self):
        """UI销毁时调用"""
        pass
