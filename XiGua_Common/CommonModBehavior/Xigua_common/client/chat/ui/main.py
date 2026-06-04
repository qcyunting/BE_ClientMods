# -*- coding: utf-8 -*-
from .. import chatUtils
from ...utils.ui_utils import *


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.system = clientApi.GetSystem(modName, "chat")
        self.ui_create = False
        self.system.gui_instance = self

        self.msg_panel = None
        self.msg_content = None
        self.msg_content_instance = {}

    def OnCreate(self):
        self.ui_create = True
        self.msg_panel = self.screen.GetBaseUIControl(
            BP + "/panel/chat_panel/chat_panel/scroll_view"
        ).asScrollView().GetScrollViewContentControl()
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

    def new_message(self, msg_data):
        if not self.ui_create:
            return

        msg_id = msg_data["msg_id"]
        message = msg_data["message"]
        user_uid = str(msg_data["user_uid"])
        username = msg_data["username"]

        if user_uid == str(self.system.uid):
            def_name = "xg_chat.m_msg"
        else:
            def_name = "xg_chat.other_user_msg"

        content_instance = self.screen.CreateChildControl(def_name, msg_id, self.msg_content)
        self.msg_content_instance[msg_id] = content_instance

        content_instance.GetChildByPath("/msg_bp/label").asLabel().SetText(str(message))
        content_instance.GetChildByPath("/user_name/user_name_panel/name").asLabel().SetText(username)
        self._set_message_image(content_instance, user_uid)

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
