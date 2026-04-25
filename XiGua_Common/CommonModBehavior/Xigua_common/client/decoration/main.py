# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from .utils import ItemsManager


class Decoration(BaseSystem):
    BATCH_SYNC_EVENT = "saveDressingRoomChanges"
    REMOTE_SYNC_EVENT = "syncPlayerDecorations"

    def __init__(self, namespace, systemName):
        super(Decoration, self).__init__(namespace, systemName)
        self.manager = ItemsManager({}, {}, {})
        self._origin_dressed_keys = []

    def _get_server_local_id(self):
        if self.local_id not in (None, -2):
            return self.local_id
        return clientApi.GetLocalPlayerId()

    def _get_local_player_id(self):
        return clientApi.GetLocalPlayerId()

    @Listen()
    def UiInitFinished(self, args):
        clientApi.RegisterUI(modName, "dressing_room", base_clsPath + "decoration.ui.dressing_room.Main",
                             "dressing_room.main")

    @Listen(event_type=Listen.server)
    def openDressingRoom(self, args):
        self.manager.set_all(args.get("all", {}))
        self.manager.set_has(args.get("has", {}))
        self.manager.set_dressed(args.get("dressed", {}))
        self.manager.clear_trying()

        server_local_id = self._get_server_local_id()
        player_id = self._get_local_player_id()
        if player_id != server_local_id:
            self.manager.set_player_dressed(player_id, self.manager.get_dressed_by_pid(server_local_id))
        self._origin_dressed_keys = self.manager.get_dressed_by_pid(player_id)
        self._rebuild_local_player_render()

        clientApi.PushScreen(modName, "dressing_room", {"system": self})

    @Listen(event_type=Listen.server)
    def syncPlayerDecorations(self, args):
        server_local_id = self._get_server_local_id()
        local_player_id = self._get_local_player_id()
        self.manager.set_all(args.get("all", {}))
        dressed_map = args.get("dressed", {})
        if not isinstance(dressed_map, dict):
            return

        for player_id, dressed_keys in dressed_map.items():
            if player_id == server_local_id:
                self.manager.set_player_dressed(local_player_id, dressed_keys)
                self._rebuild_player_render(local_player_id, include_try=False)
                continue

            self.manager.set_player_dressed(player_id, dressed_keys)
            self._rebuild_player_render(player_id, include_try=False)

    def get_type_list(self):
        return self.manager.get_type_list()

    def get_items_for_type(self, item_type, owned_only=False):
        return self.manager.get_items_by_type(item_type, owned_only)

    def toggle_try_decoration(self, key):
        if not key or not self.manager.get_item(key):
            self.clear_try_decoration()
            return
        if self.manager.is_trying(key):
            self.clear_try_decoration()
            return
        self.manager.set_trying(key)
        self._rebuild_local_player_render()

    def show_one_decoration(self, key):
        self.toggle_try_decoration(key)
    def clear_try_decoration(self):
        if not self.manager.get_trying_key():
            return
        self.manager.clear_trying()
        self._rebuild_local_player_render()

    def wear_one_decoration(self, key):
        player_id = self._get_local_player_id()
        item_data = self.manager.get_item(key)
        if not item_data or not self.manager.is_owned(key):
            return False

        slot = item_data.get("slot")
        dressed_keys = self.manager.get_dressed_by_pid(player_id)
        old_key = self.manager.get_equipped_key_by_slot(player_id, slot)

        if old_key == key:
            return False

        if old_key in dressed_keys:
            dressed_keys.remove(old_key)
        dressed_keys.append(key)
        self.manager.set_player_dressed(player_id, dressed_keys)

        if self.manager.is_trying(key):
            self.manager.clear_trying()

        self._rebuild_local_player_render()
        return True

    def unwear_one_decoration(self, key):
        player_id = self._get_local_player_id()
        dressed_keys = self.manager.get_dressed_by_pid(player_id)
        if key not in dressed_keys:
            return False

        dressed_keys.remove(key)
        self.manager.set_player_dressed(player_id, dressed_keys)

        if self.manager.is_trying(key):
            self.manager.clear_trying()

        self._rebuild_local_player_render()
        return True

    def buy_one_decoration(self, key):
        if not key or self.manager.is_owned(key):
            return False
        self.NotifyToServer("buyOneDecoration", {"key": key})
        return True

    def apply_buy_result(self, args):
        msg = args.get("msg")
        if not msg:
            msg = "§c购买失败"

        if not args.get("success"):
            return False, msg

        key = args.get("key")
        if key:
            self.manager.ensure_owned(key, args.get("has_info", {}))

        has_data = args.get("has")
        if isinstance(has_data, dict):
            self.manager.set_has(has_data)

        return True, msg

    def flush_changes_to_server(self):
        player_id = self._get_local_player_id()
        self.clear_try_decoration()

        current_keys = self.manager.get_dressed_by_pid(player_id)
        origin_set = set(self._origin_dressed_keys)
        current_set = set(current_keys)

        wear_list = [key for key in current_keys if key not in origin_set]
        unwear_list = [key for key in self._origin_dressed_keys if key not in current_set]

        data = {
            "wear_list": wear_list,
            "unwear_list": unwear_list,
            "dressed_keys": current_keys
        }
        print "发送事件" + self.BATCH_SYNC_EVENT + str(data)
        self.NotifyToServer(self.BATCH_SYNC_EVENT, data)
        self._origin_dressed_keys = list(current_keys)

    def get_effective_dressed_keys(self, player_id):
        result = self.manager.get_dressed_by_pid(player_id)
        try_key = self.manager.get_trying_key()
        if not try_key:
            return self._merge_keys_by_slot(result)

        try_item = self.manager.get_item(try_key)
        if not try_item:
            return self._merge_keys_by_slot(result)

        try_slot = try_item.get("slot")
        filtered = []
        for key in result:
            item = self.manager.get_item(key)
            if item and item.get("slot") == try_slot:
                continue
            filtered.append(key)
        filtered.append(try_key)
        return self._merge_keys_by_slot(filtered)

    def _merge_keys_by_slot(self, keys):
        merged = []
        slot_to_index = {}
        for key in keys:
            item = self.manager.get_item(key)
            if not item:
                continue

            slot = item.get("slot")
            if not slot:
                if key not in merged:
                    merged.append(key)
                continue

            if slot in slot_to_index:
                merged[slot_to_index[slot]] = key
                continue

            slot_to_index[slot] = len(merged)
            merged.append(key)
        return merged

    def _rebuild_local_player_render(self):
        self._rebuild_player_render(self._get_local_player_id(), include_try=True)

    def _rebuild_player_render(self, player_id, include_try):
        comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
        self._clear_all_item_effects(comp)

        if include_try:
            dressed_keys = self.get_effective_dressed_keys(player_id)
        else:
            dressed_keys = self.manager.get_dressed_by_pid(player_id)

        for key in dressed_keys:
            item_data = self.manager.get_item(key)
            if item_data:
                self._apply_item_effects(comp, item_data)

        comp.RebuildPlayerRender()

    def _safe_remove(self, comp, method_name, key):
        if not key:
            return
        method = getattr(comp, method_name, None)
        if callable(method):
            try:
                method(key)
            except Exception:
                pass

    def _clear_all_item_effects(self, comp):
        for item_data in self.manager._all.values():
            render_name = item_data.get("render_name")
            if render_name:
                self._safe_remove(comp, "RemovePlayerRenderController", render_name)

    def _apply_item_effects(self, comp, item_data):
        render_name = item_data.get("render_name")
        render_condition = item_data.get("render_condition")
        if render_name and render_condition:
            comp.AddPlayerRenderController(render_name, render_condition)
