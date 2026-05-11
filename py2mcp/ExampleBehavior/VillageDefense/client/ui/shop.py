# -*- coding: utf-8 -*-
import time

from ..utils.ui_utils import *
import tab_button
from .shop_data_tool import ShopDataTool
import uuid
from ..utils import escape
escape = escape.Escape()
Gui = escape.importModule("gui")


class Shop(BaseCustomScreen):
    def __init__(self, namespace, name, param):
        super(Shop, self).__init__(namespace, name, param)
        self.shop_data = param.get("data", {})
        self.tab_instance_index = param.get("tab_instance_index", 0)
        self.shop_tool = ShopDataTool(self.shop_data)
        self.tab_button_instance = tab_button.TabButton(self, self.tab_instance_index)
        self.shop_content_panel = None
        self.goods_count = 0
        self.goods_content = dict()
        self.product_cache = dict()
        self.all_is_render = False
        self.is_create = False

    @Listen(event_type=Listen.server)
    def refreshOpenShop(self, args):
        if self.is_create:
            self.shop_data = args
            self.shop_tool = ShopDataTool(self.shop_data)
            self.product_cache.clear()
            for name, childControl in self.goods_content.items():
                self.RemoveChildControl(childControl)
            if self.shop_content_panel is None:
                return
            self.update_shop_content(self.tab_button_instance.tab_selected_index)

    def Create(self):
        self.tab_button_instance.addStartAnimation(self.tab_button_instance.tab_selected_index)

        self.shop_content_panel = self.GetBaseUIControl(BP + "/content_panel/content/scrolling_panel").asScrollView().GetScrollViewContentControl()

        self.update_shop_content(self.tab_button_instance.tab_selected_index)

        self.is_create = True

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged, "#tab_toggle_btn")
    def tab_toggle_btn_click(self, args):
        if self.tab_button_instance.tab_selected_index == args["index"]:
            return
        self.tab_button_instance.onClick(args["index"])
        self.update_shop_content(self.tab_button_instance.tab_selected_index)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#goods_button_click")
    def goods_button_click(self, args):
        button_path = args.get("ButtonPath", "")
        match = re.search('/([0-9a-fA-F-]{36})/grid/goods_button([0-9]+)', button_path)
        if match is None:
            print "goods_button_click ignore:", button_path
            return

        product_uuid = match.group(1)
        goods_button_index = int(match.group(2))
        level_slot = max(0, goods_button_index - 1)
        cache_data = self.product_cache.get(product_uuid)
        if cache_data is None:
            print "goods_button_click not found cache:", product_uuid
            return

        product = cache_data.get("product")
        if product is None:
            print "goods_button_click not found product:", product_uuid
            return

        level_data = product.get_level(level_slot)
        if level_data is None:
            print "goods_button_click not found level:", product_uuid, level_slot
            return

        data = {
            "category_index": self.tab_button_instance.tab_selected_index,
            "product_slot": product.get_slot(),
            "level_slot": level_slot
        }
        self.NotifyToServer("goodsButtonClick", data)

    @Listen()
    def GridComponentSizeChangedClientEvent(self, args):
        if not self.all_is_render:
            self.render_grid_item()
            self.UpdateScreen()

    def update_shop_content(self, key_or_index):
        self.all_is_render = False
        for name, childControl in self.goods_content.items():
            self.RemoveChildControl(childControl)
        self.goods_content.clear()
        goods = self.shop_tool.get_products(key_or_index)
        gui_size_x, gui_size_y = Gui.get_size(self.screen_name, BP)
        x = max(1, int(gui_size_x - 24) // 80)
        self.product_cache.clear()
        for product in goods:
            name = str(uuid.uuid4())
            child = self.CreateChildControl("vd_shop.goods_panel", name, self.shop_content_panel)
            self.goods_content[name] = child
            y = max(1, (len(product.get_data()) + x - 1) // x)
            goods_grid = child.GetChildByPath("/grid").asGrid()
            goods_grid.SetGridDimension((x, y))

            self.product_cache[name] = {
                "content_count": x * y,
                "goods_grid": goods_grid,
                "product": product,
                "is_render": False
            }
        self.UpdateScreen()

    def render_grid_item(self):
        all_is_render = True
        for name, data in self.product_cache.items():
            content_count = data.get("content_count")
            goods_grid = data.get("goods_grid")
            product = data.get("product")
            is_render = data.get("is_render", False)
            if is_render:
                continue
            for i in range(content_count):
                item = product.get_level(i)
                item_control = goods_grid.GetChildByPath("/goods_button{}/button".format(i + 1))
                if item_control:
                    if item:
                        item_render = item_control.GetChildByPath("/item_renderer").asItemRenderer()
                        item_render.SetUiItem(item.get_item(), 0)
                        price = item.get_price()
                        text = (item.get_name() + "\n" + "§a" + str(price)) if price <= self.shop_tool.get_player_coin() else (item.get_name() + "\n" + "§c" + str(price))
                        item_control.GetChildByPath("/button_label").asLabel().SetText(text)

                        if not product.is_level_unlocked(i):
                            item_control.GetChildByPath("/lock").SetVisible(True)
                    else:
                        item_control.SetVisible(False)
                else:
                    all_is_render = False
        self.all_is_render = all_is_render
        self.UpdateScreen()

    def Destroy(self):
        self.is_create = False
        self.product_cache.clear()
        for name, childControl in self.goods_content.items():
            self.RemoveChildControl(childControl)
