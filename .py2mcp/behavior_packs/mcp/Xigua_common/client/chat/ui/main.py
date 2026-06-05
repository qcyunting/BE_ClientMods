# -*- coding: utf-8 -*-
from .. import chatUtils
from ...utils.ui_utils import *
import time


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.system = clientApi.GetSystem(modName, "chat")
        self.ui_create = False
        self.system.gui_instance = self

        self.msg_panel = None
        self.msg_content = None
        self.scroll_view = None
        self.msg_content_instance = {}

        self.msg_panel_path = ""
        self.msg_panel_pressed_time = 0
        self.copy_msg_text = ""

    def OnCreate(self):
        self.ui_create = True
        self.scroll_view = self.screen.GetBaseUIControl(
            BP + "/panel/chat_panel/chat_panel/scroll_view"
        ).asScrollView()
        self.msg_panel = self.scroll_view.GetScrollViewContentControl()
        self.msg_content = self.msg_panel.GetChildByPath("/msg_content")

        for msg_id in self.system.msg_ids:
            msg_data = self.system.messages.get(msg_id)
            if msg_data is None:
                continue
            self.new_message(msg_data)

    def OnDestroy(self):
        self.ui_create = False
        if self.system.gui_instance is self:
            self.system.gui_instance = None

    @ViewBinder.binding(ViewBinder.BF_ButtonClickDown, "#msg_panel_pressed")
    def msg_panel_pressed_down(self, args):
        if self.msg_panel_path:
            self.screen.GetBaseUIControl('/'.join(self.msg_panel_path.split('/')[1:-2]) + '/msg_tip').SetVisible(False)

        self.msg_panel_path = args.get("ButtonPath")
        self.msg_panel_pressed_time = time.time()

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#msg_panel_pressed")
    def msg_panel_pressed_up(self, args):
        ButtonPath = args.get("ButtonPath")
        tip = self.screen.GetBaseUIControl('/'.join(ButtonPath.split('/')[1:-2]) + '/msg_tip')
        if time.time() - self.msg_panel_pressed_time >= 0.3:
            parts = ButtonPath.split('/')
            result = parts[-3]
            tip.SetVisible(True)
            msg_data = self.system.messages.get(result, {})
            username = msg_data["username"]
            msg = msg_data["message"]
            text = "@{}: {}".format(username, msg)
            self.copy_msg_text = text
            return
        tip.SetVisible(False)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#copy_msg")
    def copy_msg(self, args):
        ButtonPath = args.get("ButtonPath")
        tip = self.screen.GetBaseUIControl('/'.join(ButtonPath.split('/')[1:-1]))
        tip.SetVisible(False)
        gameComp.SetClipboardContent(self.copy_msg_text)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#msg_content_pressed")
    def msg_content_pressed(self, args):
        if self.msg_panel_path:
            self.screen.GetBaseUIControl('/'.join(self.msg_panel_path.split('/')[1:-2]) + '/msg_tip').SetVisible(False)

    def new_message(self, msg_data):
        if not self.ui_create:
            return

        msg_id = msg_data["msg_id"]
        msg_type = msg_data["type"]
        message = msg_data["message"]
        user_uid = str(msg_data["user_uid"])
        username = msg_data["username"]

        if msg_type == "system":
            def_name = "xg_chat.system_msg"
        elif msg_type == "chat":
            if user_uid == str(self.system.uid):
                def_name = "xg_chat.m_msg"
            else:
                def_name = "xg_chat.other_user_msg"
        else:
            return

        content_instance = self.screen.CreateChildControl(def_name, msg_id, self.msg_content)
        self.msg_content_instance[msg_id] = content_instance
        if msg_type == "system":
            content_instance.asLabel().SetText(str(message))
            self.scroll_view.SetScrollViewPercentValue(100)
            return

        content_instance.GetChildByPath("/message").asLabel().SetText(str(message))
        content_instance.GetChildByPath("/user_name/user_name_panel/name").asLabel().SetText(username)
        self._set_message_image(content_instance, user_uid)
        self.scroll_view.SetScrollViewPercentValue(100)

    def refresh_user_image(self, user_uid):
        if not self.ui_create:
            return

        user_uid = str(user_uid)
        for msg_id, content_instance in self.msg_content_instance.items():
            msg_data = self.system.messages.get(msg_id)
            if not msg_data or str(msg_data.get("user_uid")) != user_uid:
                continue
            self._set_message_image(content_instance, user_uid)

    def _set_message_image(self, content_instance, user_uid):
        if user_uid not in self.system.player_data_by_uid.keys():
            return
        head = content_instance.GetChildByPath("/frame/head").asImage()
        chatUtils.set_user_head(head.mScreenName, head.FullPath(), user_uid)

        frame = content_instance.GetChildByPath("/frame").asImage()
        chatUtils.set_user_frame(frame.mScreenName, frame.FullPath(), user_uid)
