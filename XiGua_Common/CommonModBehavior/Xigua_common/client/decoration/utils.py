# coding=utf-8


class ItemsManager(object):

    def __init__(self, all_items, has_items, dressed):
        self._all = {}
        self._has = {}
        self._dressed = {}
        self._try_key = None
        self.set_all(all_items)
        self.set_has(has_items)
        self.set_dressed(dressed)

    def set_all(self, all_items):
        self._all = all_items if isinstance(all_items, dict) else {}

    def _resolve_key(self, key):
        if key in self._all:
            return key
        key_tokens = sorted(str(key).split("_"))
        for current_key in self._all.keys():
            if sorted(str(current_key).split("_")) == key_tokens:
                return current_key
        return None

    def set_has(self, has_items):
        source = has_items if isinstance(has_items, dict) else {}
        result = {}
        for key, data in source.items():
            resolved_key = self._resolve_key(key)
            if resolved_key:
                result[resolved_key] = data if isinstance(data, dict) else {}
        self._has = result

    def set_dressed(self, dressed):
        source = dressed if isinstance(dressed, dict) else {}
        result = {}
        for pid, keys in source.items():
            result[pid] = self._normalize_dressed_keys(keys)
        self._dressed = result

    def set_player_dressed(self, pid, keys):
        self._dressed[pid] = self._normalize_dressed_keys(keys)

    def _normalize_dressed_keys(self, keys):
        valid_keys = []
        slot_to_index = {}
        for key in keys if isinstance(keys, list) else []:
            resolved_key = self._resolve_key(key)
            if not resolved_key:
                continue

            slot = self.get_item_slot(resolved_key)
            if not slot:
                if resolved_key not in valid_keys:
                    valid_keys.append(resolved_key)
                continue

            if slot in slot_to_index:
                valid_keys[slot_to_index[slot]] = resolved_key
                continue

            slot_to_index[slot] = len(valid_keys)
            valid_keys.append(resolved_key)

        return valid_keys

    def set_trying(self, key):
        self._try_key = key if key in self._all else None

    def clear_trying(self):
        self._try_key = None

    def get_trying_key(self):
        return self._try_key

    def get_item(self, key):
        return self._all.get(key)

    def get_item_slot(self, key):
        item = self.get_item(key)
        if not item:
            return None
        return item.get("slot")

    def get_type_list(self):
        order_map = {}
        for key, data in self._all.items():
            item_type = data.get("type", "unknown")
            item_index = data.get("index", 999999)
            if item_type not in order_map or item_index < order_map[item_type]:
                order_map[item_type] = item_index
        return [item_type for item_type, _ in sorted(order_map.items(), key=lambda item: item[1])]

    def _sort_items(self, items):
        return sorted(items, key=lambda item: item[1].get("index", 999999))

    def get_items_by_type(self, item_type, owned_only=False):
        result = []
        for key, data in self._all.items():
            if data.get("type") != item_type:
                continue
            if owned_only and key not in self._has:
                continue
            result.append((key, data))
        return self._sort_items(result)

    def get_all_items_group_by_type(self):
        result = {}
        for item_type in self.get_type_list():
            result[item_type] = self.get_items_by_type(item_type, False)
        return result

    def get_has_items_group_by_type(self):
        result = {}
        for item_type in self.get_type_list():
            items = self.get_items_by_type(item_type, True)
            if items:
                result[item_type] = items
        return result

    def get_owned_keys(self):
        return list(self._has.keys())

    def ensure_owned(self, key, has_info=None):
        key = self._resolve_key(key)
        if not key:
            return
        self._has[key] = has_info if isinstance(has_info, dict) else {}

    def is_owned(self, key):
        return key in self._has

    def is_equipped(self, pid, key):
        return key in self._dressed.get(pid, [])

    def is_trying(self, key):
        return self._try_key == key

    def get_dressed_by_pid(self, pid):
        return list(self._dressed.get(pid, []))

    def get_equipped_key_by_slot(self, pid, slot):
        for key in self._dressed.get(pid, []):
            item = self.get_item(key)
            if item and item.get("slot") == slot:
                return key
        return None
