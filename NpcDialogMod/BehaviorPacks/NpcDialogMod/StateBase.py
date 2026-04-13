# -*- coding: utf-8 -*-
from utils import *
import module
import module_registry
import main


class StateMode():
    """状态模式枚举类，定义所有可能的主状态"""
    on = "on"  # 启动
    off = "off"  # 关闭

class Main(ClientSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)

        self.fsm = FSM()

        self.ListenForEvent("Minecraft", "Engine", "LoadClientAddonScriptsAfter", self, self.LoadClientAddonScriptsAfter)
        self.ListenForEvent("Common", "main", "StartMod", self, self.start_mod)

    def LoadClientAddonScriptsAfter(self, args):
        main_state = self.fsm.add_state(main.Main)  # 添加状态
        self.fsm.add_state(OFF)  # 添加状态

        print "所有注册的模块: " + str(module_registry.plugin_registry)
        # 自动将所有已注册的插件添加为MainState的子状态
        for plugin_name, plugin_class in module_registry.plugin_registry.items():
            plugin_class.state_name = plugin_name
            main_state.add_sub_state(plugin_class)

        self.fsm.update_state(StateMode.off)  # 更新状态

    def start_mod(self, mod_list):
        if modName in mod_list:
            self.fsm.update_state(StateMode.on)
        else:
            self.fsm.update_state(StateMode.off)

class FSM:
    """有限状态机（Finite State Machine）类，管理状态切换和状态生命周期"""

    def __init__(self):
        """初始化状态机"""
        self.states = set()  # 所有已注册的状态集合
        self.now_state = set()  # 当前活跃的状态集合
        self.system = None

    def add_state(self, state_type, is_sub_state=False, parent_state=None, *args, **kwargs):
        """
        添加状态到状态机
        :param state_type: 状态类
        :param is_sub_state: 是否为子状态
        :param parent_state: 父状态实例（如果是子状态）
        :return: 创建的状态实例
        """
        if is_sub_state and parent_state:
            # 如果是子状态，添加到父状态中
            return parent_state.add_sub_state(state_type, *args, **kwargs)
        else:
            # 否则作为顶级状态添加到状态机
            state = state_type(modName, systemName)
            state.fsm = self  # 设置状态机的引用
            self.states.add(state)
            return state

    def update_state(self, new_state, *args, **kwargs):
        """
        更新当前状态
        :param new_state: 要切换到的状态名称
        """
        logger.info("FSM: state changed to {}".format(new_state))

        # 遍历所有状态，启用匹配的状态，禁用其他状态
        for state in self.states:
            if state.state_name == new_state:
                state._on_enable(*args, **kwargs)
                logger.debug("Enable state {}".format(state.state_name))
                self.now_state.add(state)
            else:
                state._on_disable()
                logger.debug("Disable state {}".format(state.state_name))
                self.now_state.discard(state)

    def get_state(self):
        """
        获取当前活跃的状态
        :return: 当前状态实例，如果没有活跃状态则返回None
        """
        return next(iter(self.now_state)) if self.now_state else None
