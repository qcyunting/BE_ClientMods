# -*- coding: utf-8 -*-
from ..utils.ui_utils import *
import chatUtils
import time
import uuid
from ..utils import escape
instance = escape.Escape()


class Chat(BaseSystem):
    def __init__(self, namespace, name):
        super(Chat, self).__init__(namespace, name)
        self.player_data_by_uid = {}  # type: {str: dict}

        self.msg_ids = []
        self.messages = {}
        self.max_messages = 100

        self.gui_instance = None

    @Listen(event_type=Listen.server)
    def AddPlayer(self, args):
        pid = str(args.get("pid"))
        uid = str(args.get("uid"))
        username = args.get("username", "用户{}".format(uid))
        if not pid:
            return
        if not uid:
            return
        if uid in self.player_data_by_uid:
            return
        chatUtils.download_player_head_image(pid, uid)
        self.player_data_by_uid[uid] = {"username": username}

    @Listen(event_type=Listen.server)
    def SendMessage(self, args):
        msg = args.get("message")
        msg_type = args.get("type", "system")
        user_uid = str(args.get("uid"))
        username = args.get("username", self.get_username_by_uid(user_uid))
        msg_time = int(time.time() * 1000)
        msg_id = self._generate_msg_id(msg_time)

        msg_data = {
            "msg_id": msg_id,
            "type": msg_type,
            "time": msg_time,
            "message": msg,
            "user_uid": user_uid,
            "username": username
        }

        self.msg_ids.append(msg_id)
        self.messages[msg_id] = msg_data
        self._limit_cache_size()

        if self.gui_instance:
            self.gui_instance.new_message(msg_data)

    @Listen(event_type=Listen.server)
    def ClearAllMessages(self, args):
        self.msg_ids[:] = []
        self.messages.clear()

    def _generate_msg_id(self, time_time):
        return "msg_{}_{}".format(time_time, uuid.uuid4().hex[:8])

    def get_username_by_uid(self, uid):
        uid = str(uid)
        user_data = self.player_data_by_uid.get(uid)
        if user_data and isinstance(user_data, dict):
            return user_data.get("username", "用户{}".format(uid))
        return "用户{}".format(uid)

    def _limit_cache_size(self):
        if len(self.msg_ids) > self.max_messages:
            old_msg_ids = self.msg_ids[:-self.max_messages]
            for old_id in old_msg_ids:
                self.messages.pop(old_id, None)
            self.msg_ids = self.msg_ids[-self.max_messages:]

    def get_all_messages(self):
        return [self.messages[msg_id] for msg_id in self.msg_ids if msg_id in self.messages]

    def get_latest_messages(self, count=20):
        latest_ids = self.msg_ids[-count:] if count < len(self.msg_ids) else self.msg_ids
        return [self.messages[msg_id] for msg_id in latest_ids if msg_id in self.messages]

    def get_messages_by_range(self, start_index=0, end_index=None):
        msg_count = len(self.msg_ids)
        if end_index is None or end_index > msg_count:
            end_index = msg_count

        if start_index < 0 or start_index >= msg_count:
            return []

        range_ids = self.msg_ids[start_index:end_index]
        return [self.messages[msg_id] for msg_id in range_ids if msg_id in self.messages]

    def get_message_by_id(self, msg_id):
        return self.messages.get(msg_id)

    def update_message_status(self, msg_id, status):
        if msg_id in self.messages:
            self.messages[msg_id]["status"] = status
            return True
        return False

    def delete_message_by_id(self, msg_id):
        if self.messages.pop(msg_id, None):
            self.msg_ids.remove(msg_id)
            return True
        return False

    def get_messages_by_user(self, user_uid):
        user_uid = str(user_uid)
        return [msg for msg in self.get_all_messages() if msg.get("user_uid") == user_uid]

    def get_message_count(self):
        return len(self.msg_ids)

    def search_messages(self, keyword):
        keyword = keyword.lower()
        return [
            msg for msg in self.get_all_messages()
            if keyword in msg.get("message", "").lower()
        ]

    def clear_messages_by_user(self, user_uid):
        user_uid = str(user_uid)
        msg_ids_to_delete = [
            msg_id for msg_id, msg in self.messages.items()
            if msg.get("user_uid") == user_uid
        ]

        for msg_id in msg_ids_to_delete:
            self.messages.pop(msg_id, None)

        self.msg_ids = [mid for mid in self.msg_ids if mid not in msg_ids_to_delete]

    def sort_messages_by_time(self, reverse=False):
        self.msg_ids.sort(
            key=lambda x: self.messages[x].get("time", 0),
            reverse=reverse
        )

    @Listen(event_type=Listen.server)
    def SetLocalUID(self, args):
        uid = args.get("local_uid")
        self.uid = uid
        def callback(data):
            player_data = data.get(str(uid), {"headImageUrl": None, "frameImageUrl": None, "username": None})
            self.NotifyToServer("requestUidUsernameCallback", {"data": player_data})
        chatUtils.requestUidUsername([str(uid), ], callback)