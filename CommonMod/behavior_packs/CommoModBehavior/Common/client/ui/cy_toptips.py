# -*- coding: utf-8 -*-
"""
Created on 2026-02-15
顶部提示UI系统
这里主要 提供一个顶部提示ui操作
"""
from utils import *


class Main(BaseCustomScreen):
    def __init__(self, namespace, name, param):
        super(Main, self).__init__(namespace, name, param)
        self.mPlayerId = clientApi.GetLocalPlayerId()
        self.mLevelId = clientApi.GetLevelId()
        self.data = param.get('data', {})
        self.client = param.get('client', None)

    def Create(self): # 当界面加载完成后
        self.setdata()
    def setdata(self):
        argss = self.client.ui_toptips_args
        tip1 = argss.get("tip1",None)
        tip2 = argss.get("tip2",None)
        tip3 = argss.get("tip3",None)
        if tip1:
            self.GetBaseUIControl("/stack_panel_toptips/image_tips1").asImage().SetVisible(True)
            self.GetBaseUIControl("/stack_panel_toptips/image_tips1/label").asLabel().SetText(tip1)
        if tip2:
            self.GetBaseUIControl("/stack_panel_toptips/image_tips2").asImage().SetVisible(True)
            self.GetBaseUIControl("/stack_panel_toptips/image_tips2/label").asLabel().SetText(tip2)
        if tip3:
            self.GetBaseUIControl("/stack_panel_toptips/image_tips3").asImage().SetVisible(True)
            self.GetBaseUIControl("/stack_panel_toptips/image_tips3/label").asLabel().SetText(tip3)

    def update_args(self):
        self.setdata()
    def OnActive(self):  # UI重新回到栈顶时调用
        pass

    def OnDeactive(self):  # 栈顶UI有其他UI入栈时调用
        pass

    def Destroy(self):  # 销毁时调用
        pass
