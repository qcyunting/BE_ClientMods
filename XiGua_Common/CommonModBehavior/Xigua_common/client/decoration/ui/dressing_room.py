# -*- coding: utf-8 -*-
from ...utils.listen_util import Listen
from ...utils.ui_utils import *
from ...utils import escape
escape = escape.Escape()
Gui = escape.importModule("gui")


class Main(BaseCustomScreen):
    def __init__(self, namespace, name, param):
        super(Main, self).__init__(namespace, name, param)
        self.system = param["system"]
        self.type_list = self.system.get_type_list()
        self.type_index = 0
        self.type_key = self.type_list[0] if self.type_list else ""

        self.tab_btn_selection_control = None
        self.item_grid = None
        self.tab_btn_lock = False
        self.isHasMode = False
        self.max_x = 0
        self.selected_key = None

        self._ensure_selection()

    def Create(self):
        self.tab_btn_selection_control = self.GetBaseUIControl(
            BP + "/stack_panel/tab_panel/tab_list/btn_background"
        ).asImage()
        self.item_grid = self.GetBaseUIControl(
            BP + "/stack_panel/item_grid/image/scroll_view"
        ).asScrollView().GetScrollViewContentControl().GetChildByPath("/grid").asGrid()
        self.move_tab_btn_selection_image(self.type_index)

    def _get_current_items(self):
        if not self.type_key:
            return []
        return self.system.get_items_for_type(self.type_key, self.isHasMode)

    def _ensure_selection(self):
        items = self._get_current_items()
        if not items:
            self.selected_key = None
            return
        keys = [key for key, _ in items]
        if self.selected_key not in keys:
            self.selected_key = keys[0]

    def _get_item_by_index(self, index):
        items = self._get_current_items()
        if 0 <= index < len(items):
            return items[index]
        return None, None

    def _get_selected_item(self):
        if not self.selected_key:
            return None, None
        for key, item_data in self._get_current_items():
            if key == self.selected_key:
                return key, item_data
        return None, None

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#tab_btn_click")
    def tab_btn_click(self, args):
        index = args["#collection_index"]
        if not self.tab_btn_lock:
            self.move_tab_btn_selection_image(index)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#item_btn_click")
    def item_btn_click(self, args):
        key, item_data = self._get_item_by_index(args["#collection_index"])
        if not key:
            return
        self.selected_key = key
        self.system.toggle_try_decoration(key)
        self.UpdateScreen()

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#use_button_click")
    def use_button_click(self, args):
        key, item_data = self._get_selected_item()
        if not key:
            return

        player_id = clientApi.GetLocalPlayerId()
        if self.system.manager.is_owned(key):
            if self.system.manager.is_equipped(player_id, key):
                self.system.unwear_one_decoration(key)
            else:
                self.system.wear_one_decoration(key)
        else:
            self.system.buy_one_decoration(key)
        self.UpdateScreen()

    @ViewBinder.binding(ViewBinder.BF_BindString, "#use_button_text")
    def return_use_button_text(self):
        key, item_data = self._get_selected_item()
        if not key:
            return "§8选择服装"
        if not self.system.manager.is_owned(key):
            return "§8购买"
        player_id = clientApi.GetLocalPlayerId()
        return "§8卸下" if self.system.manager.is_equipped(player_id, key) else "§8穿戴"

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged, "#isHasType")
    def OnHasTypeTabChecked(self, args):
        self.isHasMode = args["index"] == 1
        self._ensure_selection()
        self.update_grid()

    def update_grid(self):
        gui_size_x, gui_size_y = Gui.get_size(self.screen_name, BP)
        self.max_x = max(1, int(gui_size_x - 10 - 55 - 150 - 6 - 8) // 50)
        item_count = len(self._get_current_items())
        y = max(1, (item_count + self.max_x - 1) // self.max_x)
        self.item_grid.SetGridDimension((self.max_x, y))
        self.UpdateScreen()
        gameComp.AddTimer(0.1, lambda: self.UpdateScreen())

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_panel_visible")
    def return_item_panel_visible(self, index):
        key, item_data = self._get_item_by_index(index)
        return item_data is not None

    @ViewBinder.binding(ViewBinder.BF_BindString, "#item_name")
    def return_item_name(self):
        key, item_data = self._get_selected_item()
        return item_data.get("name", "") if item_data else ""

    @ViewBinder.binding(ViewBinder.BF_BindString, "#item_description")
    def return_item_description(self):
        key, item_data = self._get_selected_item()
        if not item_data:
            return "选择左侧的服装进行试穿、穿戴或购买"
        return item_data.get("description", "")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_panel_text")
    def return_item_panel_text(self, index):
        key, item_data = self._get_item_by_index(index)
        if not item_data:
            return ""
        return item_data.get("currency", "")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_icon_texture")
    def return_item_panel_icon(self, index):
        key, item_data = self._get_item_by_index(index)
        if not item_data:
            return ""
        return item_data.get("icon", "")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_bg_image")
    def return_item_panel_bg(self, index):
        key, item_data = self._get_item_by_index(index)
        if not item_data:
            return ""
        return item_data.get("bg", "")

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_new_visible")
    def return_item_panel_new_visible(self, index):
        key, item_data = self._get_item_by_index(index)
        return item_data.get("is_new") is True if item_data else False

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_hot_visible")
    def return_item_panel_hot_visible(self, index):
        key, item_data = self._get_item_by_index(index)
        return item_data.get("is_hot") is True if item_data else False

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_selection")
    def return_item_selection(self, index):
        key, item_data = self._get_item_by_index(index)
        return key == self.selected_key

    @ViewBinder.binding(ViewBinder.BF_BindInt, "#tab_list.item_count")
    def tab_list_count(self):
        return len(self.type_list)

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "tab_list", "#tab_text")
    def return_tab_text(self, index):
        if 0 <= index < len(self.type_list):
            return self.type_list[index]
        return ""

    def move_tab_btn_selection_image(self, to_index):
        if not self.type_list:
            return
        to_index = max(0, min(to_index, len(self.type_list) - 1))
        self.tab_btn_lock = True
        anim = {
            "namespace": "dressing_room",
            "move_tab_btn_selection": {
                "anim_type": "offset",
                "duration": 0.1,
                "from": [0, self.type_index * 15],
                "to": [0, to_index * 15]
            }
        }
        clientApi.RegisterUIAnimations(anim, True)
        self.tab_btn_selection_control.RemoveAnimation("offset")
        self.tab_btn_selection_control.SetAnimation("offset", "dressing_room", "move_tab_btn_selection")
        self.tab_btn_selection_control.PlayAnimation("offset")

        def anim_callback():
            self.tab_btn_lock = False
        self.tab_btn_selection_control.SetAnimEndCallback("move_tab_btn_selection", anim_callback)

        self.type_index = to_index
        self.type_key = self.type_list[to_index]
        self._ensure_selection()
        self.update_grid()

    @Listen(event_type=Listen.server)
    def buyItemResult(self, args):
        if not self.system.apply_buy_result(args):
            return
        self._ensure_selection()
        self.update_grid()

    def Destroy(self):
        self.system.flush_changes_to_server()
