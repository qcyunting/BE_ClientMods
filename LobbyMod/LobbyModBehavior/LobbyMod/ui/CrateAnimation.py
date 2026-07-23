# coding=utf-8
import math
import time
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()


class Main(ScreenNode):
    SLOT_COUNT = 11
    SLOT_PITCH = 80.0
    SLOT_WIDTH = 74.0
    CENTER_X = 200.0
    MAX_ITEMS = 256
    ITEM_ALIASES = {
        "minecraft:snow": "minecraft:snow_layer",
        "minecraft:grass_block": "minecraft:grass",
        "minecraft:filled_map": "minecraft:map",
        "minecraft:oak_sign": "minecraft:sign"
    }
    LEGACY_COLORS = {
        "0": (0.0, 0.0, 0.0),
        "1": (0.0, 0.0, 0.667),
        "2": (0.0, 0.667, 0.0),
        "3": (0.0, 0.667, 0.667),
        "4": (0.667, 0.0, 0.0),
        "5": (0.667, 0.0, 0.667),
        "6": (1.0, 0.667, 0.0),
        "7": (0.667, 0.667, 0.667),
        "8": (0.333, 0.333, 0.333),
        "9": (0.333, 0.333, 1.0),
        "a": (0.333, 1.0, 0.333),
        "b": (0.333, 1.0, 1.0),
        "c": (1.0, 0.333, 0.333),
        "d": (1.0, 0.333, 1.0),
        "e": (1.0, 1.0, 0.333),
        "f": (1.0, 1.0, 1.0)
    }

    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        data = param.get("data", {}) if isinstance(param, dict) else {}
        self.data = data if isinstance(data, dict) else {}
        source_items = self.data.get("items", [])
        self.items = list(source_items[:self.MAX_ITEMS]) if isinstance(source_items, (list, tuple)) else []
        winner_index = int(self._number(self.data.get("winnerIndex"), 0))
        self.winner_index = max(0, min(winner_index, max(0, len(self.items) - 1)))
        self.landing_offset = max(-0.22, min(0.22, self._number(self.data.get("landingOffset"), 0.0)))
        self.spin_ms = max(2000.0, self._number(self.data.get("spinDurationMs"), 7000))
        self.result_ms = max(750.0, self._number(self.data.get("resultDurationMs"), 2000))
        self.started = 0.0
        self.closed = False
        self.slots = []
        self.slot_item_indices = [None] * self.SLOT_COUNT
        self.last_sound_index = -1
        self.result_sound_played = False
        self.audio = None
        self.title_control = None
        self.subtitle_control = None
        self.status_control = None
        self.result_control = None

    def Create(self):
        self.started = time.time()
        self.title_control = self.GetBaseUIControl("/root/title")
        self.subtitle_control = self.GetBaseUIControl("/root/subtitle")
        self.status_control = self.GetBaseUIControl("/root/status")
        self.result_control = self.GetBaseUIControl("/root/result")
        self.title_control.asLabel().SetText(self._format(self.data.get("title", u"\u7948\u613f")))
        self.subtitle_control.asLabel().SetText(self._format(self.data.get("subtitle", "")))
        self.status_control.asLabel().SetText(u"\u5f00\u542f\u4e2d...")
        self.status_control.SetVisible(True)
        self.result_control.SetVisible(False)
        for index in range(self.SLOT_COUNT):
            self.slots.append(self.GetBaseUIControl("/root/reel_frame/reel/slot%s" % index))
        try:
            self.audio = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
        except Exception:
            self.audio = None
        self._render(self._current_index(0.0))

    def Update(self):
        if self.closed or not self.started:
            return
        elapsed = (time.time() - self.started) * 1000.0
        if elapsed >= self.spin_ms + self.result_ms:
            self.closed = True
            clientApi.PopScreen()
            return

        current = self._current_index(elapsed)
        if elapsed < self.spin_ms:
            sound_index = int(math.floor(current))
            if sound_index > self.last_sound_index:
                self.last_sound_index = sound_index
                denominator = max(1.0, float(self.winner_index))
                pitch = 0.85 + min(0.35, current / denominator * 0.35)
                self._play_ui_sound("random.click", 0.32, pitch)
        elif not self.result_sound_played:
            self.result_sound_played = True
            self._show_result()
            self._play_ui_sound("random.levelup", 0.8, 1.05)

        self._render(current)

    def _current_index(self, elapsed):
        start_index = min(3.0, max(0.0, self.winner_index - 1.0))
        target_index = self.winner_index + self.landing_offset
        if elapsed >= self.spin_ms:
            return target_index
        progress = max(0.0, min(1.0, elapsed / self.spin_ms))
        eased = 1.0 - math.pow(1.0 - progress, 2.5)
        return start_index + (target_index - start_index) * eased

    def _show_result(self):
        self.subtitle_control.asLabel().SetText("")
        self.status_control.SetVisible(False)
        self.result_control.SetVisible(True)
        prefix = u"\u5b9a\u8f68\u83b7\u5f97 " if bool(self.data.get("guaranteed")) else u"\u83b7\u5f97 "
        winner = self._format(self.data.get("winnerColor", "&f")) + self._format(self.data.get("winnerName", ""))
        rarity_name = self.data.get("winnerRarity", "")
        text = prefix + winner
        if rarity_name:
            text += u"\n" + self._format(self.data.get("winnerColor", "&f")) + self._format(rarity_name)
        self.result_control.asLabel().SetText(text)

    def _render(self, current):
        if not self.items:
            return
        base = int(math.floor(current)) - self.SLOT_COUNT // 2
        for slot_index, control in enumerate(self.slots):
            item_index = base + slot_index
            if item_index < 0 or item_index >= len(self.items):
                control.SetVisible(False)
                self.slot_item_indices[slot_index] = None
                continue
            item = self.items[item_index]
            if not isinstance(item, dict):
                control.SetVisible(False)
                self.slot_item_indices[slot_index] = None
                continue
            control.SetVisible(True)
            x = self.CENTER_X + (item_index - current) * self.SLOT_PITCH - self.SLOT_WIDTH / 2.0
            control.SetPosition((x, 5.0))
            if self.slot_item_indices[slot_index] == item_index:
                continue
            self.slot_item_indices[slot_index] = item_index
            item_id = self._bedrock_item_id(item.get("material", "minecraft:chest"))
            try:
                control.GetChildByPath("/item_renderer").asItemRenderer().SetUiItem(item_id, 0)
            except Exception:
                control.GetChildByPath("/item_renderer").asItemRenderer().SetUiItem("minecraft:chest", 0)
            name = self._format(item.get("color", "&f")) + self._format(item.get("name", ""))
            control.GetChildByPath("/name").asLabel().SetText(name)
            stripe = control.GetChildByPath("/rarity_stripe").asImage()
            stripe.SetSpriteColor(self._legacy_rgb(item.get("color", "&f")))

    def _bedrock_item_id(self, material):
        value = self._to_text(material).lower()
        if ":" not in value:
            value = "minecraft:" + value
        return self.ITEM_ALIASES.get(value, value)

    def _legacy_rgb(self, value):
        text = self._to_text(value).lower()
        color = self.LEGACY_COLORS["f"]
        for index in range(len(text) - 1):
            if text[index] in (u"&", u"\u00a7"):
                color = self.LEGACY_COLORS.get(text[index + 1], color)
        return color

    def _to_text(self, value):
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

    def _format(self, value):
        return self._to_text(value).replace(u"&", u"\u00a7")

    def _number(self, value, fallback):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(fallback)

    def _play_ui_sound(self, name, volume, pitch):
        if self.audio is None:
            return
        try:
            self.audio.PlayCustomUIMusic(name, volume, pitch, False)
        except Exception:
            pass

    def Destroy(self):
        self.closed = True
        self.audio = None

    def OnActive(self):
        pass

    def OnDeactive(self):
        pass
