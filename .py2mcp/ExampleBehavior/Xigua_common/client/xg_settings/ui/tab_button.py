# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
from mod.client.ui.screenNode import ScreenNode

class TabButton(object):
    def __init__(self, screen_proxy, tab_selected_index=0):
        self.screen_node = screen_proxy.screen  # type: Type[ScreenNode]
        self.tab_selected_index = tab_selected_index

    def onClick(self, index):
        if index == self.tab_selected_index:
            return
        self.addStartAnimation(index)
        self.addEndAnimation(self.tab_selected_index)
        self.tab_selected_index = index

    def addStartAnimation(self, index):
        animation = {
            "namespace": "xg_settings",
            "top_bar_toggle_selected_anim": {
                "anim_type": "size",
                "duration": 0.1,
                "from": [0, 2],
                "to": [34, 2],
                "next": "",
            }
        }
        clientApi.RegisterUIAnimations(animation)
        def callback():
            pass
        for control in ["checked", "checked_hover", "unchecked", "unchecked_hover"]:
            selected_bar = self.screen_node.GetBaseUIControl(BP + "/tab_panel/top_bar_toggle_btn_{}/{}/selected".format(index, control)).asImage()  # 获取选中的控件
            selected_bar.RemoveAnimation("size")  # 先删除之前残留的动画
            selected_bar.SetAnimEndCallback("top_bar_toggle_selected_anim", callback)  # 设置动画播放结束的回调函数
            selected_bar.SetAnimation("size", "xg_settings", "top_bar_toggle_selected_anim", True)  # 添加动画

    def addEndAnimation(self, index):
        animation = {
            "namespace": "xg_settings",
            "top_bar_toggle_selected_anim": {
                "anim_type": "size",
                "duration": 0.1,
                "from": [34, 2],
                "to": [0, 2],
                "next": "",
            }
        }
        clientApi.RegisterUIAnimations(animation)
        def callback():
            pass
        for control in ["checked", "checked_hover", "unchecked", "unchecked_hover"]:
            selected_bar = self.screen_node.GetBaseUIControl(BP + "/tab_panel/top_bar_toggle_btn_{}/{}/selected".format(index, control)).asImage()  # 获取选中的控件
            selected_bar.RemoveAnimation("size")  # 先删除之前残留的动画
            selected_bar.SetAnimEndCallback("top_bar_toggle_selected_anim", callback)  # 设置动画播放结束的回调函数
            selected_bar.SetAnimation("size", "xg_settings", "top_bar_toggle_selected_anim", True)  # 添加动画

