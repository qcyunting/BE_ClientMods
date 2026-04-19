# -*- coding: utf-8 -*-
from ...utils.listen_util import Listen
from ...utils.ui_utils import *
from ...utils import escape
escape = escape.Escape()
Gui = escape.importModule("gui")
from collections import defaultdict

class Main(BaseCustomScreen):
    def __init__(self, namespace, name, param):
        super(Main, self).__init__(namespace, name, param)
        self.system = param["system"]
        type_list = list(self.system.items_by_type.keys())
        if param.get("type", "") in type_list:
            self.type_index = type_list.index(param.get("type", ""))
        else:
            self.type_index = 0
        self.type_key = type_list[self.type_index]

        self.tab_btn_selection_control = None
        self.item_grid = None
        self.old_selection_item_index = 0
        self.tab_btn_lock = False
        self.isHasMode = False
        self.max_x = 0

    def Create(self):
        self.tab_btn_selection_control = self.GetBaseUIControl(BP + "/stack_panel/tab_panel/tab_list/btn_background").asImage()
        self.item_grid = self.GetBaseUIControl(BP + "/stack_panel/item_grid/image/scroll_view").asScrollView().GetScrollViewContentControl().GetChildByPath("/grid").asGrid()
        self.move_tab_btn_selection_image(self.type_index)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#tab_btn_click")
    def tab_btn_click(self, args):
        index = args["#collection_index"]
        if not self.tab_btn_lock:
            self.move_tab_btn_selection_image(index)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#item_btn_click")
    def item_btn_click(self, args):
        index = args["#collection_index"]
        self.old_selection_item_index = index
        self.system.show_one_decoration(self.get_selection_item_key())

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#use_button_click")
    def use_button_click(self, args):
        key = self.get_selection_item_key()
        if key in self.system.has_decoration:
            if key in self.system.all_dressed:
                self.system.unwear_one_decoration(key)
            else:
                self.system.wear_one_decoration(key)
        else:
            self.system.buy_one_decoration(key)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#use_button_text")
    def return_use_button_text(self):
        key = self.get_selection_item_key()
        return "§8卸下" if key in self.system.all_dressed else ("§8穿戴" if key in self.system.has_decoration else "§8购买")

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged, "#isHasType")
    def OnHasTypeTabChecked(self, args):
        if args["index"] == 0:
            self.isHasMode = False
        else:
            self.isHasMode = True
        self.update_grid()

    def update_grid(self):
        self.old_selection_item_index = 0
        gui_size_x, gui_size_y =  Gui.get_size(self.screen_name, BP)
        self.max_x = int(gui_size_x - 10 - 55 - 150 - 6 - 8) // 50
        if self.isHasMode:
            item_count = len(self.system.has_items_by_type.get(self.type_key, []))
        else:
            item_count = len(self.system.items_by_type.get(self.type_key, []))
        y = (item_count + self.max_x - 1) // self.max_x
        self.item_grid.SetGridDimension((self.max_x, y))
        self.UpdateScreen()
        gameComp.AddTimer(0.1, lambda: self.UpdateScreen())

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_panel_visible")
    def return_item_panel_visible(self, index):
        return self.get_item_data(index, "name") != ""

    @ViewBinder.binding(ViewBinder.BF_BindString, "#item_name")
    def return_item_name(self):
        return self.get_item_data(self.old_selection_item_index, "name")

    @ViewBinder.binding(ViewBinder.BF_BindString, "#item_description")
    def return_item_description(self):
        return self.get_item_data(self.old_selection_item_index, "description")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_panel_text")
    def return_item_panel_text(self, index):
        return self.get_item_data(index, "currency")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_icon_texture")
    def return_item_panel_icon(self, index):
        return self.get_item_data(index, "icon")

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "decoration_item_grid_binding", "#item_bg_image")
    def return_item_panel_bg(self, index):
        return self.get_item_data(index, "bg")

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_new_visible")
    def return_item_panel_new_visible(self, index):
        return self.get_item_data(index, "is_new") == True

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_hot_visible")
    def return_item_panel_hot_visible(self, index):
        return self.get_item_data(index, "is_hot") == True

    def get_item_data(self, index, data_key):
        if self.isHasMode:
            data = self.system.has_items_by_type
        else:
            data = self.system.items_by_type
        item_list = data.get(self.type_key, [])
        if index < len(item_list):
            return item_list[index][1].get(data_key, "")
        else:
            return ""

    def get_selection_item_key(self):
        if self.isHasMode:
            data = self.system.has_items_by_type
        else:
            data = self.system.items_by_type
        item_list = data.get(self.type_key, [])
        return item_list[self.old_selection_item_index][0]

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "decoration_item_grid_binding", "#item_selection")
    def return_item_selection(self, index):
        return self.old_selection_item_index == index

    @ViewBinder.binding(ViewBinder.BF_BindInt, "#tab_list.item_count")
    def tab_list_count(self):
        return len(self.system.items_by_type)

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "tab_list", "#tab_text")
    def return_tab_text(self, index):
        return self.system.items_by_type.keys()[index]

    def move_tab_btn_selection_image(self, to_index):
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
        print "注册动画", anim
        clientApi.RegisterUIAnimations(anim, True)
        self.tab_btn_selection_control.RemoveAnimation("offset")
        self.tab_btn_selection_control.SetAnimation("offset", "dressing_room", "move_tab_btn_selection")
        self.tab_btn_selection_control.PlayAnimation("offset")
        def anim_callback():
            print "动画播放结束"
            self.tab_btn_lock = False
        self.tab_btn_selection_control.SetAnimEndCallback("move_tab_btn_selection", anim_callback)
        self.type_index = to_index
        self.type_key = list(self.system.items_by_type.keys())[to_index]
        self.update_grid()

    @Listen(event_type=Listen.server)
    def buyItemResult(self, args):
        if args.get("success"):
            self.system.has_decoration = args.get("has", {})
            item_type_map = {key: value.get('type', 'unknown') for key, value in self.system.all_decoration.items()}

            has_classified = defaultdict(dict)
            for key, value in self.system.has_decoration.items():
                item_type = item_type_map.get(key, 'unknown')
                full_info = self.system.all_decoration.get(key, {}).copy()
                full_info.update(value)
                if full_info.get("isEquipped"):
                    self.all_dressed.append(key)
                has_classified[item_type][key] = full_info
            self.system.has_items_by_type = dict(has_classified)

            # 排序
            for item_type, items_dict in self.system.has_items_by_type.items():
                self.system.has_items_by_type[item_type] = sorted(items_dict.items(), key=lambda x: x[1]['index'])

    def Destroy(self):
        self.system.show_one_decoration("")
