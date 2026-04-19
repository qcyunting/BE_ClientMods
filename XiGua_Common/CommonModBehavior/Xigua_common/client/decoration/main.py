# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from ..utils.listen_util import *
from collections import defaultdict

class Decoration(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Decoration, self).__init__(namespace, systemName)
        self._current_show_key = ""
        self.all_decoration = {}
        self.has_decoration = {}
        self.items_by_type = {}
        self.has_items_by_type = {}
        self.all_dressed = []
        self.try_on_by_location = {}

    @Listen()
    def UiInitFinished(self, args):
        clientApi.RegisterUI(modName, "dressing_room", base_clsPath + "decoration.ui.dressing_room.Main", "dressing_room.main")

    @Listen(event_type=Listen.server)
    def openDressingRoom(self, args):
        self.all_decoration = args.get("all", {})
        self.has_decoration = args.get("has", {})

        item_type_map = {key: value.get('type', 'unknown') for key, value in self.all_decoration.items()}

        classified = defaultdict(dict)
        for key, value in self.all_decoration.items():
            item_type = value.get('type', 'unknown')
            classified[item_type][key] = value
        self.items_by_type = dict(classified)

        for item_type, items_dict in self.items_by_type.items():
            self.items_by_type[item_type] = sorted(items_dict.items(), key=lambda x: x[1]['index'])

        has_classified = defaultdict(dict)
        for key, value in self.has_decoration.items():
            item_type = item_type_map.get(key, 'unknown')
            full_info = self.all_decoration.get(key, {}).copy()
            full_info.update(value)
            if full_info.get("isEquipped"):
                self.all_dressed.append(key)
            has_classified[item_type][key] = full_info
        self.has_items_by_type = dict(has_classified)

        # 排序
        for item_type, items_dict in self.has_items_by_type.items():
            self.has_items_by_type[item_type] = sorted(items_dict.items(), key=lambda x: x[1]['index'])

        data = {"system": self}
        clientApi.PushScreen(modName, "dressing_room", data)

    def show_one_decoration(self, key):
        """临时展示单个装饰品，展示下一个会清除上一个"""
        if key == self._current_show_key:
            self._clear_show()
            return
        self._clear_show()
        if not key:
            self._current_show_key = None
            return
        item_data = self.all_decoration.get(key)
        if not item_data:
            print "装饰品不存在: " + key
            return

        self._current_show_key = key
        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
        for model_key, model_name in item_data.get('model', {}).items():
            if None not in [model_key, model_name]:
                comp.AddPlayerGeometry(model_key, model_name)
        for texture_key, texture_path in item_data.get('texture', {}).items():
            if None not in [texture_key, texture_path]:
                comp.AddPlayerTexture(texture_key, texture_path)
        for anim_key, anim_name in item_data.get('animation', {}).items():
            if None not in [anim_key, anim_name]:
                comp.AddPlayerAnimation(anim_key, anim_name)
            for anim_controller_key, anim_controller_name in item_data.get('animation_controller', {}).items():
                if None not in [anim_controller_key, anim_controller_name]:
                    comp.AddPlayerAnimationController(anim_controller_key, anim_controller_name)
                    comp.AddActorScriptAnimate("minecraft:player", anim_controller_key)
        for render_key, condition in item_data.get('render', {}).items():
            if None not in [render_key, condition]:
                comp.AddPlayerRenderController(render_key, condition)

        comp.RebuildPlayerRender()

    def _clear_show(self):
        """清除当前展示的装饰品效果"""
        if not self._current_show_key:
            return

        playerId = clientApi.GetLocalPlayerId()
        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)

        item_data = self.all_decoration.get(self._current_show_key)
        if item_data:
            for model_key in item_data.get('model', {}):
                if model_key is not None:
                    comp.RemovePlayerGeometry(model_key)
            for render_key in item_data.get('render', {}):
                if render_key is not None:
                    comp.RemovePlayerRenderController(render_key)

        self._apply_dressed_items()

        comp.RebuildPlayerRender()
        self._current_show_key = None

    def _apply_dressed_items(self):
        """应用所有已穿戴的装饰品"""
        playerId = clientApi.GetLocalPlayerId()
        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)

        for key in self.all_dressed:
            item_data = self.all_decoration.get(key)
            if not item_data:
                continue
            for model_key, model_name in item_data.get('model', {}).items():
                if None not in [model_key, model_name]:
                    comp.AddPlayerGeometry(model_key, model_name)
            for texture_key, texture_path in item_data.get('texture', {}).items():
                if None not in [texture_key, texture_path]:
                    comp.AddPlayerTexture(texture_key, texture_path)
            for anim_key, anim_name in item_data.get('animation', {}).items():
                if None not in [anim_key, anim_name]:
                    comp.AddPlayerAnimation(anim_key, anim_name)
            for anim_controller_key, anim_controller_name in item_data.get('animation_controller', {}).items():
                if None not in [anim_controller_key, anim_controller_name]:
                    comp.AddPlayerAnimationController(anim_controller_key, anim_controller_name)
                    comp.AddActorScriptAnimate("minecraft:player", anim_controller_key)
            for render_key, condition in item_data.get('render', {}).items():
                if None not in [render_key, condition]:
                    comp.AddPlayerRenderController(render_key, condition)

        comp.RebuildPlayerRender()

    def wear_one_decoration(self, key):
        """穿戴装饰品（永久）"""
        if key in self.all_dressed:
            print "已经穿戴过了: " + key
            return
        item_data = self.all_decoration.get(key)
        if not item_data:
            print "装饰品不存在: " + key
            return

        self.all_dressed.append(key)

        if self._current_show_key:
            self._clear_show()
        else:
            self._apply_dressed_items()
        self.NotifyToServer("wearOneDecoration", {"key": key})

    def unwear_one_decoration(self, key):
        """脱掉装饰品"""
        if key not in self.all_dressed:
            print "未穿戴: " + key
            return

        self.all_dressed.remove(key)

        if self._current_show_key:
            self._clear_show()
        else:
            self._reapply_all_dressed()
        self.NotifyToServer("unwearOneDecoration", {"key": key})

    def _reapply_all_dressed(self):
        """重新应用所有已穿戴装饰品（先清除全部再应用）"""
        playerId = clientApi.GetLocalPlayerId()
        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
        for key in self.all_dressed:
            item_data = self.all_decoration.get(key)
            if not item_data:
                continue
            for model_key, model_name in item_data.get('model', {}).items():
                if None not in [model_key, model_name]:
                    comp.AddPlayerGeometry(model_key, model_name)
            for texture_key, texture_path in item_data.get('texture', {}).items():
                if None not in [texture_key, texture_path]:
                    comp.AddPlayerTexture(texture_key, texture_path)
            for anim_key, anim_name in item_data.get('animation', {}).items():
                if None not in [anim_key, anim_name]:
                    comp.AddPlayerAnimation(anim_key, anim_name)
            for anim_controller_key, anim_controller_name in item_data.get('animation_controller', {}).items():
                if None not in [anim_controller_key, anim_controller_name]:
                    comp.AddPlayerAnimationController(anim_controller_key, anim_controller_name)
                    comp.AddActorScriptAnimate("minecraft:player", anim_controller_key)
            for render_key, condition in item_data.get('render', {}).items():
                if None not in [render_key, condition]:
                    comp.AddPlayerRenderController(render_key, condition)

        comp.RebuildPlayerRender()

    def buy_one_decoration(self, key):
        self.NotifyToServer("buyOneDecoration", {"key": key})

    def render_layer_decoration(self):
        """示例"""
        comp = CF.CreateActorRender(playerId) # 创建actorRender组件
        # 修改玩家模型、新增翅膀和披风
        comp.AddPlayerGeometry("custom_cape", "geometry.cape") # 新增自定义披风
        comp.AddPlayerGeometry("dragon_wings", "geometry.dragon_wings") # 新增翅膀

        comp.AddPlayerTexture("dragon_wings", "textures/decorations/dragon_wings/dragon_wings_autumn")  # 新增翅膀贴图
        comp.AddPlayerTexture("custom_cape", "textures/decorations/cape/15th_anniversary_cape")  # 新增披风贴图

        # 新增动作部分
        comp.AddPlayerAnimation('dragon_wings','animation.dragon_wings.idle') # 新增翅膀动画

        # 新增玩家渲染控制器部分
        comp.AddPlayerRenderController("controller.render.player.custom_cape",
                                       "!variable.is_first_person && !query.is_spectator"
        )
        comp.AddPlayerRenderController("controller.render.player.dragon_wings",
                                       "!variable.is_first_person && !query.is_spectator"
        )

        # 新增动画控制器部分
        comp.AddPlayerAnimationController('dragon_wings', 'controller.animation.decoration.dragon_wings')  # 新增动画控制器
        comp.AddActorScriptAnimate("minecraft:player", "dragon_wings")  # 执行新的动画控制器

        # 保存部分
        comp.RebuildPlayerRender() # 保存上面的所有操作并立刻显示上面修改的所有内容
