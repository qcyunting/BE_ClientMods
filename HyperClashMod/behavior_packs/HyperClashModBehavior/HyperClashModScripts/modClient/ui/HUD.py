# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

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

    def Create(self):
        """UI创建成功时调用 - 在这里初始化UI"""
        print "==== HUD Create ===="

        # 解析传入的数据
        data = self.param.get("data", {})
        for skill in data.get("skills", [{}, {}, {}]):
            skillId = skill.get("skillId", "null")
            icon = skill.get("icon", "")
            slot = skill.get("slot", 1)
            self.skills[skillId] = (slot, icon)

        print self.skills

        # 获取客户端系统
        self.clientSystem = clientApi.GetSystem(ModName, "ShopSystem")

        # 监听事件
        self.clientSystem.ListenForEvent(ModName, "SkillSystem", "UpdateSkillCooldown", self, self.UpdateSkillCooldown)

        # 初始化按钮
        self._init_buttons()
        self._initialized = True

    def _init_buttons(self):
        """初始化所有技能按钮"""
        for i in range(1, 4):
            button_path = "/skill_button_" + str(i)
            button = self.GetBaseUIControl(button_path)
            button.SetVisible(False)

        for skillId, (slot, texture) in self.skills.items():
            try:
                # 获取按钮控件
                button_path = "/skill_button_" + str(slot)
                button = self.GetBaseUIControl(button_path)
                if not button:
                    print "[HUD] Button not found:", button_path
                    continue

                button.SetVisible(True)

                button = button.asButton()

                # 获取图标控件
                icon_path = button_path + "/icon"
                icon_control = self.GetBaseUIControl(icon_path)
                if icon_control:
                    icon = icon_control.asImage()
                    if icon:
                        icon.SetSprite(texture)

                # 为每个按钮单独创建回调
                def make_callback(s_id, s_slot):
                    def on_button_down(args):
                        self._on_skill_button_click(s_id, s_slot)

                    return on_button_down

                # 设置按钮回调
                button.AddTouchEventParams()
                button.SetButtonTouchDownCallback(make_callback(skillId, slot))

            except Exception as e:
                print
                "[HUD] Error initializing button for skill", skillId, ":", e

    def _on_skill_button_click(self, skillId, slot):
        """技能按钮点击处理"""
        print 'skill_button_click', skillId

        # 检查是否已在冷却中
        if skillId in self.all_cooldown:
            print
            "[HUD] Skill already in cooldown:", skillId
            return

        button_path = "/skill_button_" + str(slot)

        icon_path = button_path + "/icon"
        icon_control = self.GetBaseUIControl(icon_path).asImage()
        icon_control.SetAlpha(0.5)

        # 通知服务端
        data = {"skillId": skillId, "slot": slot}
        self.clientSystem.NotifyToServer("ClickSkillButton", data)

    def UpdateSkillCooldown(self, args):
        """每秒接收冷却值"""
        for skill in args['skills']:
            print skill
            skillId = skill.get("skillId", '')
            cooldown = skill.get("cooldown", 0)
            self.all_cooldown[skillId] = cooldown
            slot, texture = self.skills[skillId]
            button_path = "/skill_button_" + str(slot)
            if cooldown > 0:
                button_path = "/skill_button_" + str(slot)
                icon_path = button_path + "/icon"
                icon_control = self.GetBaseUIControl(icon_path).asImage()
                icon_control.SetAlpha(0.5)

                text_path = button_path + "/text"
                text_control = self.GetBaseUIControl(text_path).asLabel()
                text_control.SetText(str(cooldown))
            else:
                self.all_cooldown.pop(skillId)

                icon_path = button_path + "/icon"
                icon_control = self.GetBaseUIControl(icon_path).asImage()
                icon_control.SetAlpha(1.0)
                
                text_path = button_path + "/text"
                text_control = self.GetBaseUIControl(text_path).asLabel()
                text_control.SetText('')

    def Destroy(self):
        """UI销毁时调用"""

        # 取消事件监听
        if self.clientSystem:
            self.clientSystem.UnListenForEvent(ModName, "SkillSystem", "UpdateSkillCooldown", self, self.UpdateSkillCooldown)