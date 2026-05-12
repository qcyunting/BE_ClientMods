# -*- coding: utf-8 -*-

DEFAULT_CATEGORY_ORDER = ["armor", "weapon", "potion", "food", "other"]  # type: list[str]


class ShopDataItem(object):
    """最内层商品等级模型。"""

    def __init__(self, item_data):  # type: (dict | None) -> None
        """初始化等级模型。"""
        self._raw = item_data or {}  # type: dict[str, object]

    def get_slot(self):  # type: () -> int
        """获取该等级条目的 slot。"""
        return int(self._raw.get("slot", 0))  # type: ignore

    def get_item(self):  # type: () -> str | None
        """获取 item 标识。"""
        return self._raw.get("item")  # type: ignore

    def get_price(self):  # type: () -> int | float | None
        """获取价格。"""
        return self._raw.get("price")  # type: ignore

    def get_name(self):  # type: () -> str | None
        """获取名称。"""
        return self._raw.get("name")  # type: ignore

    def get_data(self, slot=None):  # type: (int | None) -> "ShopDataItem" | None
        """
        兼容方法。该层只有一个对象本身：
        - slot 为空返回 self
        - slot 非空则仅当相同 slot 时返回 self
        """
        if slot is None:
            return self
        return self if self.get_slot() == slot else None

    def to_dict(self):  # type: () -> dict[str, object]
        """转为原始字典。"""
        return dict(self._raw)


class ShopProduct(object):
    """中间层商品模型（分类内按 slot 排序的商品）。"""

    def __init__(self, product_data):  # type: (dict | None) -> None
        """初始化商品模型。"""
        self._raw = product_data or {}  # type: dict[str, object]
        self._slot = int(self._raw.get("slot", 0))  # type: ignore
        self._max_level = int(self._raw.get("maxLevel", 0))  # type: ignore
        raw_data = self._raw.get("data", []) or []  # type: ignore
        self._items = sorted(  # type: list[ShopDataItem]
            [ShopDataItem(item) for item in raw_data],
            key=lambda item: item.get_slot(),
        )

    def get_slot(self):  # type: () -> int
        """获取商品 slot（中间层 slot）。"""
        return self._slot

    def get_max_level(self):  # type: () -> int
        """获取商品 maxLevel（可解锁最高等级）。"""
        return self._max_level

    def get_level_count(self):  # type: () -> int
        """获取等级条目数量。"""
        return len(self._items)

    def get_data_count(self):  # type: () -> int
        """获取等级条目数量（别名）。"""
        return self.get_level_count()

    def get_levels(self):  # type: () -> list[ShopDataItem]
        """获取该商品全部等级（按 slot 从小到大）。"""
        return list(self._items)

    def get_data(self):  # type: () -> list[ShopDataItem]
        """获取该商品全部等级（别名）。"""
        return self.get_levels()

    def get_level(self, level_slot):  # type: (int) -> ShopDataItem | None
        """按等级 slot 获取单条等级数据。"""
        for item in self._items:  # type: ShopDataItem
            if item.get_slot() == level_slot:
                return item
        return None

    def get_product(self, level_slot):  # type: (int) -> ShopDataItem | None
        """按等级 slot 获取单条等级数据（与 get_level 等价）。"""
        return self.get_level(level_slot)

    def is_level_unlocked(self, level_slot):  # type: (int) -> bool
        """判断指定等级是否已解锁（level_slot <= maxLevel）。"""
        return level_slot <= self._max_level

    def to_dict(self):  # type: () -> dict[str, object]
        """转为原始字典。"""
        return dict(self._raw)


class ShopCategory(object):
    """最外层分类模型。"""

    def __init__(self, key, index, category_data):  # type: (str, int, list[dict] | None) -> None
        """初始化分类模型。"""
        self._key = key  # type: str
        self._index = index  # type: int
        raw_products = category_data or []  # type: list[dict]
        self._products = sorted(  # type: list[ShopProduct]
            [ShopProduct(item) for item in raw_products],
            key=lambda product: product.get_slot(),
        )

    def get_key(self):  # type: () -> str
        """获取分类 key。"""
        return self._key

    def get_index(self):  # type: () -> int
        """获取分类索引。"""
        return self._index

    def get_product_count(self):  # type: () -> int
        """获取分类下商品数量。"""
        return len(self._products)

    def get_product(self, product_slot):  # type: (int) -> ShopProduct | None
        """按商品 slot 获取中间层商品。"""
        for product in self._products:  # type: ShopProduct
            if product.get_slot() == product_slot:
                return product
        return None

    def get_product_by_index(self, product_slot):  # type: (int) -> ShopProduct | None
        """按商品 slot 获取商品（别名）。"""
        return self.get_product(product_slot)

    def get_products(self):  # type: () -> list[ShopProduct]
        """获取分类下全部商品（按商品 slot）。"""
        return list(self._products)

    def get_products_count(self):  # type: () -> int
        """获取分类下商品数量（别名）。"""
        return self.get_product_count()

    def get_data(self):  # type: () -> list[ShopProduct]
        """获取分类下全部商品（别名）。"""
        return self.get_products()


class ShopDataTool(object):
    """商店 JSON 到对象的便捷访问工具。"""

    def __init__(self, shop_data, category_order=None):  # type: (dict[str, object] | None, list[str] | None) -> None
        """初始化工具类。入参为完整 shop json。"""
        self._raw = shop_data or {}  # type: dict[str, object]
        raw_category_keys = [key for key in self._raw.keys() if key != "player_coin"]  # type: list[str]
        order = list(category_order or DEFAULT_CATEGORY_ORDER)  # type: list[str]
        ordered_keys = [key for key in order if key in raw_category_keys] + [key for key in raw_category_keys if key not in order]  # type: list[str]

        self._category_keys = ordered_keys  # type: list[str]
        self._index_to_key = {idx: key for idx, key in enumerate(self._category_keys)}  # type: dict[int, str]
        self._key_to_index = {key: idx for idx, key in self._index_to_key.items()}  # type: dict[str, int]
        self._categories = {
            key: ShopCategory(key, self._key_to_index[key], self._raw.get(key, []))  # type: ignore
            for key in self._category_keys
        }
        self._player_coin = self._raw.get("player_coin", 0)  # type: ignore

    def get_player_coin(self):  # type: () -> int
        """获取 player_coin。"""
        return self._player_coin  # type: ignore

    def get_category_keys(self):  # type: () -> list[str]
        """获取全部分类 key。"""
        return list(self._category_keys)

    def get_category_mapping(self):  # type: () -> dict[str, int]
        """获取分类 key->index 映射。"""
        return dict(self._key_to_index)

    def get_key_by_index(self, index):  # type: (int) -> str | None
        """按分类 index 获取分类 key。"""
        return self._index_to_key.get(index)

    def get_index_by_key(self, key):  # type: (str) -> int | None
        """按分类 key 获取 index。"""
        return self._key_to_index.get(key)

    def get_category(self, key_or_index):  # type: (str | int) -> ShopCategory | None
        """按分类 key 或 index 获取分类模型。"""
        key = self.get_key_by_index(key_or_index) if isinstance(key_or_index, int) else key_or_index
        if key is None:
            return None
        return self._categories.get(key)

    def get_category_data(self, key_or_index):  # type: (str | int) -> list[ShopProduct]
        """兼容方法名：返回分类下全部商品。"""
        return self.get_products(key_or_index)

    def get_products(self, key_or_index):  # type: (str | int) -> list[ShopProduct]
        """返回某分类下全部商品。"""
        category = self.get_category(key_or_index)
        if category is None:
            return []
        return category.get_products()

    def get_product(self, key_or_index, product_slot):  # type: (str | int, int) -> ShopProduct | None
        """返回某分类下某商品。"""
        category = self.get_category(key_or_index)
        if category is None:
            return None
        return category.get_product(product_slot)

    def get_levels(self, key_or_index, product_slot):  # type: (str | int, int) -> list[ShopDataItem]
        """返回某分类某商品的全部等级。"""
        product = self.get_product(key_or_index, product_slot)
        if product is None:
            return []
        return product.get_data()

    def get_data(self, key_or_index, product_slot, level_slot):  # type: (str | int, int, int) -> ShopDataItem | None
        """返回最内层对象：分类 -> 商品 -> 等级。"""
        product = self.get_product(key_or_index, product_slot)
        if product is None:
            return None
        return product.get_level(level_slot)

    def get_level(self, key_or_index, product_slot, level_slot):  # type: (str | int, int, int) -> ShopDataItem | None
        """返回某分类某商品某等级（同 get_data）。"""
        return self.get_data(key_or_index, product_slot, level_slot)
