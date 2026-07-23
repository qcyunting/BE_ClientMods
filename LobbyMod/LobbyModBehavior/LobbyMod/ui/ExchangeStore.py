# coding=utf-8
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()


class Main(ScreenNode):
    MAX_CATEGORIES = 6
    MAX_ROWS = 128
    MAX_GOODS = 128
    ROW_PITCH = 38
    ITEM_ALIASES = {
        "minecraft:snow": "minecraft:snow_layer",
        "minecraft:grass_block": "minecraft:grass",
        "minecraft:filled_map": "minecraft:map",
        "minecraft:oak_sign": "minecraft:sign"
    }
    CATEGORY_ITEMS = {
        "effects": "minecraft:gunpowder",
        "effect": "minecraft:gunpowder",
        "chatcolor": "minecraft:book",
        "chat_color": "minecraft:book",
        "title": "minecraft:name_tag",
        "tag": "minecraft:name_tag",
        "currency": "minecraft:emerald",
        "exchange": "minecraft:emerald",
        "money": "minecraft:emerald"
    }

    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        param = param if isinstance(param, dict) else {}
        self.client = param.get("client")
        self.data = {}
        self.categories = []
        self.goods = []
        self.selected_category = ""
        self.selected_item = ""
        self.owned_only = False
        self.goods_scroll = None
        self.reset_scroll = True
        self.pending = False
        self.pending_frames = 0
        self.preview_item = ""
        self.preview_frames = 0
        self.notice_frames = 0
        self.detail_lore_visible = True
        self.created = False
        self._load_data(param.get("data", {}), False)

    def Create(self):
        self.created = True
        self._button("/root/window/header/close", self.close_shop)
        self._button("/root/window/content/goods/filter_all", self.select_all)
        self._button("/root/window/content/goods/filter_owned", self.select_owned)
        self._button("/root/window/content/detail/action", self.request_action)
        for index in range(self.MAX_CATEGORIES):
            self._button(
                "/root/window/content/categories/cat{}".format(index),
                self.select_category,
                {"index": index}
            )
        try:
            self.goods_scroll = self.GetBaseUIControl(
                "/root/window/content/goods/list"
            ).asScrollView()
            self._bind_good_rows()
        except Exception:
            self.goods_scroll = None
        self._layout_detail()
        self._render()


    def _layout_detail(self):
        detail = "/root/window/content/detail"
        try:
            height = self.GetBaseUIControl(detail).GetSize()[1]
        except Exception:
            return
        self.detail_lore_visible = height >= 190
        if height >= 240:
            return
        preview = self.GetBaseUIControl(detail + "/preview")
        preview.SetSize((preview.GetSize()[0], 52))
        lower = self.GetBaseUIControl(detail + "/lower_surface")
        lower.SetSize((lower.GetSize()[0], max(1, height - 58)))
        compact_y = {
            "/name": 62,
            "/store": 82,
            "/status_label": 99,
            "/status": 99,
            "/cooldown_label": 114,
            "/cooldown": 114,
            "/remaining_label": 129,
            "/remaining": 129,
            "/lore": 148
        }
        for child, y in compact_y.items():
            control = self.GetBaseUIControl(detail + child)
            position = control.GetPosition()
            control.SetPosition((position[0], y))
        lore = self.GetBaseUIControl(detail + "/lore")
        lore.SetSize((lore.GetSize()[0], max(1, height - 184)))

    def _button(self, path, callback, params=None):
        button = self.GetBaseUIControl(path).asButton()
        button.AddTouchEventParams(params or {})
        button.SetButtonTouchDownCallback(callback)
        return button

    def _load_data(self, raw, preserve):
        raw = raw if isinstance(raw, dict) else {}
        old_category = self.selected_category
        old_item = self.selected_item
        self.data = raw
        self.categories = []
        for entry in raw.get("categories", [])[:self.MAX_CATEGORIES]:
            if isinstance(entry, dict):
                category_id = self._text(entry.get("id", ""))
                if category_id:
                    self.categories.append({
                        "id": category_id,
                        "name": self._format(entry.get("name", u"\u5206\u7c7b")),
                        "icon": self._text(entry.get("icon", ""))
                    })
        self.goods = []
        for entry in raw.get("goods", [])[:self.MAX_GOODS]:
            if not isinstance(entry, dict):
                continue
            item_id = self._text(entry.get("id", ""))
            category_id = self._text(entry.get("category_id", ""))
            if not item_id or not category_id:
                continue
            lore = []
            source_lore = entry.get("lore", [])
            if isinstance(source_lore, (list, tuple)):
                for line in source_lore[:12]:
                    lore.append(self._format(line))
            self.goods.append({
                "id": item_id,
                "category_id": category_id,
                "name": self._format(entry.get("name", u"\u5546\u54c1")),
                "sub_name": self._format(entry.get("sub_name", "")),
                "material": self._bedrock_item_id(entry.get("material", "minecraft:chest")),
                "effect_id": self._text(entry.get("effect_id", "")),
                "store_title": self._format(entry.get("store_title", "")),
                "action": self._text(entry.get("action", "purchase")).lower(),
                "action_text": self._format(entry.get("action_text", u"\u8d2d\u4e70")),
                "owned": self._boolean(entry.get("owned")),
                "equipped": self._boolean(entry.get("equipped")),
                "status": self._format(entry.get("status", "")),
                "remaining": self._integer(entry.get("remaining"), -1),
                "cooldown": self._format(entry.get("cooldown", "")),
                "lore": lore
            })
        category_ids = [entry["id"] for entry in self.categories]
        requested_category = self._text(
            raw.get("selected_category")
            or raw.get("default_category")
            or raw.get("default_category_id")
            or ""
        )
        if preserve and old_category in category_ids:
            self.selected_category = old_category
        elif requested_category in category_ids:
            self.selected_category = requested_category
        else:
            self.selected_category = category_ids[0] if category_ids else ""
        requested_item = self._text(raw.get("selected_item_id", ""))
        valid_ids = [entry["id"] for entry in self._filtered_goods()]
        if preserve and old_item in valid_ids:
            self.selected_item = old_item
        elif requested_item in valid_ids:
            self.selected_item = requested_item
        else:
            self.selected_item = valid_ids[0] if valid_ids else ""
        self.reset_scroll = True
        self.pending = False
        self.pending_frames = 0

    def update_shop_data(self, raw):
        old_preview = self.preview_item
        self._load_data(raw, True)
        if old_preview:
            self._send("StopPreviewEffect", {})
            self.preview_item = ""
        if self.created:
            self._render()
        print("[LobbyMod][ExchangeStoreUI] update categories={} goods={}".format(
            len(self.categories), len(self.goods)
        ))

    def _filtered_goods(self):
        result = []
        for good in self.goods:
            if good["category_id"] != self.selected_category:
                continue
            if self.owned_only and not good["owned"]:
                continue
            result.append(good)
        return result

    def _selected_good(self):
        for good in self.goods:
            if good["id"] == self.selected_item:
                return good
        return None

    def _ensure_selection(self):
        goods = self._filtered_goods()
        ids = [entry["id"] for entry in goods]
        if self.selected_item not in ids:
            self.selected_item = ids[0] if ids else ""

    def select_category(self, args):
        params = args.get("AddTouchEventParams", {}) if isinstance(args, dict) else {}
        index = self._integer(params.get("index"), -1)
        if index < 0 or index >= len(self.categories):
            return
        self._stop_preview()
        self.selected_category = self.categories[index]["id"]
        self.selected_item = ""
        self.reset_scroll = True
        self._ensure_selection()
        self._render()

    def select_all(self, args):
        self.owned_only = False
        self.reset_scroll = True
        self._ensure_selection()
        self._render()

    def select_owned(self, args):
        self.owned_only = True
        self.reset_scroll = True
        self._ensure_selection()
        self._render()

    def select_good(self, args):
        params = args.get("AddTouchEventParams", {}) if isinstance(args, dict) else {}
        index = self._integer(params.get("index"), -1)
        goods = self._filtered_goods()
        if index < 0 or index >= len(goods):
            return
        next_id = goods[index]["id"]
        if next_id != self.selected_item:
            self._stop_preview()
            self.selected_item = next_id
        self._render()
    def request_action(self, args):
        good = self._selected_good()
        if good is None or self.pending:
            return
        self._stop_preview()
        self.pending = True
        self.pending_frames = 300
        self._send("RequestBuyItem", {"itemId": good["id"]})
        self._render_detail()

    def show_action_result(self, raw):
        raw = raw if isinstance(raw, dict) else {}
        success = self._boolean(raw.get("success"))
        action = self._text(raw.get("action", "purchase")).lower()
        message = self._format(raw.get("message", ""))
        if success:
            if action == "equip":
                message = u"\u00a7a\u7a7f\u6234\u6210\u529f"
            elif action == "unequip":
                message = u"\u00a7a\u5378\u4e0b\u6210\u529f"
            else:
                message = u"\u00a7a\u8d2d\u4e70\u6210\u529f"
        elif not message:
            message = u"\u00a7c\u64cd\u4f5c\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5"
        self.pending = False
        self.pending_frames = 0
        self.notice_frames = 180
        self.GetBaseUIControl("/root/window/notice").asLabel().SetText(message)
        self.GetBaseUIControl("/root/window/notice").SetVisible(True)
        self._render_detail()
        print("[LobbyMod][ExchangeStoreUI] RESULT success={} action={}".format(success, action))

    def _render(self):
        self._ensure_selection()
        self.GetBaseUIControl("/root/window/header/title").asLabel().SetText(
            self._format(self.data.get("title", u"\u5546\u57ce"))
        )
        self._render_categories()
        self._render_filters()
        self._render_goods()
        self._render_detail()
        self._update_preview()

    def _render_categories(self):
        for index in range(self.MAX_CATEGORIES):
            path = "/root/window/content/categories/cat{}".format(index)
            control = self.GetBaseUIControl(path)
            visible = index < len(self.categories)
            control.SetVisible(visible)
            if not visible:
                continue
            category = self.categories[index]
            selected = category["id"] == self.selected_category
            control.GetChildByPath("/surface").asImage().SetSpriteColor(
                (0.18, 0.42, 0.45) if selected else (0.16, 0.18, 0.21)
            )
            control.GetChildByPath("/label").asLabel().SetText(category["name"])
            item_id = self.CATEGORY_ITEMS.get(category["id"].lower(), "minecraft:chest")
            try:
                control.GetChildByPath("/icon").asItemRenderer().SetUiItem(item_id, 0)
            except Exception:
                pass

    def _render_filters(self):
        self.GetBaseUIControl("/root/window/content/goods/filter_all/surface").asImage().SetSpriteColor(
            (0.18, 0.42, 0.45) if not self.owned_only else (0.16, 0.18, 0.21)
        )
        self.GetBaseUIControl("/root/window/content/goods/filter_owned/surface").asImage().SetSpriteColor(
            (0.18, 0.42, 0.45) if self.owned_only else (0.16, 0.18, 0.21)
        )
        heading = u"\u5546\u54c1"
        for category in self.categories:
            if category["id"] == self.selected_category:
                heading = category["name"]
                break
        self.GetBaseUIControl("/root/window/content/goods/heading").asLabel().SetText(heading)

    def _render_goods(self):
        goods = self._filtered_goods()
        content = self._goods_content()
        if content is None:
            return
        try:
            viewport_height = max(1, self.goods_scroll.GetSize()[1])
            content_width = max(1, content.GetSize()[0])
            content.SetSize((content_width, max(viewport_height, len(goods) * self.ROW_PITCH)))
        except Exception:
            pass
        for row in range(self.MAX_ROWS):
            control = content.GetChildByPath("/row{}".format(row))
            visible = row < len(goods)
            control.SetVisible(visible)
            if not visible:
                continue
            button = control.asButton()
            button.AddTouchEventParams({"index": row})
            button.SetButtonTouchDownCallback(self.select_good)
            good = goods[row]
            selected = good["id"] == self.selected_item
            control.GetChildByPath("/surface").asImage().SetSpriteColor(
                (0.15, 0.25, 0.26) if selected else (0.145, 0.165, 0.19)
            )
            control.GetChildByPath("/edge").asImage().SetSpriteColor(
                (0.32, 0.82, 0.84) if selected else (0.27, 0.30, 0.34)
            )
            control.GetChildByPath("/name").asLabel().SetText(good["name"])
            control.GetChildByPath("/sub").asLabel().SetText(good["sub_name"])
            control.GetChildByPath("/flag").asLabel().SetText(self._flag(good))
            try:
                control.GetChildByPath("/icon").asItemRenderer().SetUiItem(good["material"], 0)
            except Exception:
                control.GetChildByPath("/icon").asItemRenderer().SetUiItem("minecraft:chest", 0)
        if self.reset_scroll and self.goods_scroll is not None:
            try:
                self.goods_scroll.SetScrollViewPercentValue(0)
            except Exception:
                pass
            self.reset_scroll = False
        self.GetBaseUIControl("/root/window/content/goods/empty").SetVisible(not bool(goods))

    def _goods_content(self):
        if self.goods_scroll is None:
            return None
        try:
            return self.goods_scroll.GetScrollViewContentControl()
        except Exception:
            return None

    def _bind_good_rows(self):
        content = self._goods_content()
        if content is None:
            return
        for index in range(self.MAX_ROWS):
            button = content.GetChildByPath("/row{}".format(index)).asButton()
            button.AddTouchEventParams({"index": index})
            button.SetButtonTouchDownCallback(self.select_good)
    def _render_detail(self):
        good = self._selected_good()
        detail = "/root/window/content/detail"
        has_good = good is not None
        self.GetBaseUIControl(detail + "/empty").SetVisible(not has_good)
        for child in ("/preview", "/name", "/store", "/status_label", "/status",
                      "/cooldown_label", "/cooldown", "/remaining_label", "/remaining",
                      "/action"):
            self.GetBaseUIControl(detail + child).SetVisible(has_good)
        self.GetBaseUIControl(detail + "/lore").SetVisible(has_good and self.detail_lore_visible)
        if not has_good:
            return
        preview_icon = self.GetBaseUIControl(detail + "/preview/fallback")
        preview_icon.SetVisible(True)
        try:
            preview_icon.asItemRenderer().SetUiItem(good["material"], 0)
        except Exception:
            preview_icon.asItemRenderer().SetUiItem("minecraft:chest", 0)
        self.GetBaseUIControl(detail + "/name").asLabel().SetText(good["name"])
        self.GetBaseUIControl(detail + "/store").asLabel().SetText(good["store_title"])
        self.GetBaseUIControl(detail + "/status").asLabel().SetText(good["status"] or "-")
        self.GetBaseUIControl(detail + "/cooldown").asLabel().SetText(good["cooldown"] or "-")
        remaining = u"\u4e0d\u9650" if good["remaining"] < 0 else self._text(good["remaining"])
        self.GetBaseUIControl(detail + "/remaining").asLabel().SetText(remaining)
        lore = u"\n".join([line for line in good["lore"] if line][:7])
        self.GetBaseUIControl(detail + "/lore").asLabel().SetText(lore)
        action = self.GetBaseUIControl(detail + "/action")
        action.asButton().SetTouchEnable(not self.pending)
        action.GetChildByPath("/label").asLabel().SetText(
            u"\u5904\u7406\u4e2d..." if self.pending else good["action_text"]
        )
        color = (0.64, 0.27, 0.30) if good["action"] == "unequip" else (
            (0.16, 0.50, 0.54) if good["action"] == "equip" else (0.18, 0.55, 0.34)
        )
        if self.pending:
            color = (0.25, 0.27, 0.30)
        action.GetChildByPath("/surface").asImage().SetSpriteColor(color)

    def _update_preview(self):
        good = self._selected_good()
        next_item = good["id"] if good is not None and good["effect_id"] else ""
        if next_item == self.preview_item:
            return
        self._stop_preview()
        if next_item:
            self.preview_item = next_item
            self.preview_frames = 160
            self._send("PreviewEffect", {"itemId": next_item})

    def _stop_preview(self):
        if self.preview_item:
            self._send("StopPreviewEffect", {})
            self.preview_item = ""
            self.preview_frames = 0

    def _send(self, event_name, data):
        if self.client is not None:
            self.client.send_event(event_name, data)

    def close_shop(self, args):
        self._stop_preview()
        clientApi.PopScreen()

    def Update(self):
        if self.pending_frames > 0:
            self.pending_frames -= 1
            if self.pending_frames == 0 and self.pending:
                self.pending = False
                self.notice_frames = 180
                notice = self.GetBaseUIControl("/root/window/notice")
                notice.asLabel().SetText(u"\u00a7c\u8bf7\u6c42\u8d85\u65f6\uff0c\u8bf7\u91cd\u8bd5")
                notice.SetVisible(True)
                self._render_detail()
        if self.notice_frames > 0:
            self.notice_frames -= 1
            if self.notice_frames == 0:
                self.GetBaseUIControl("/root/window/notice").SetVisible(False)
        if self.preview_item:
            self.preview_frames -= 1
            if self.preview_frames <= 0:
                self.preview_frames = 160
                self._send("PreviewEffect", {"itemId": self.preview_item})

    def _flag(self, good):
        if good["equipped"]:
            return u"\u00a76\u5df2\u7a7f\u6234"
        if good["owned"]:
            return u"\u00a7a\u5df2\u62e5\u6709"
        return u"\u00a7b" + good["action_text"]

    def _bedrock_item_id(self, value):
        item_id = self._text(value).lower()
        if not item_id:
            return "minecraft:chest"
        if ":" not in item_id:
            item_id = "minecraft:" + item_id
        return self.ITEM_ALIASES.get(item_id, item_id)

    def _format(self, value):
        return self._text(value).replace(u"&", u"\u00a7")

    def _text(self, value):
        try:
            text_type = unicode
        except NameError:
            text_type = str
        if value is None:
            return u""
        if isinstance(value, text_type):
            return value
        try:
            return text_type(value, "utf-8")
        except TypeError:
            return text_type(value)
        except Exception:
            return u""

    def _integer(self, value, fallback=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def _boolean(self, value):
        if isinstance(value, bool):
            return value
        return self._text(value).lower() in ("true", "1", "yes")

    def Destroy(self):
        self._stop_preview()

    def OnActive(self):
        pass

    def OnDeactive(self):
        pass

