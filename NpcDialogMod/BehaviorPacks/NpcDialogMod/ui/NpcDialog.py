# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from collections import OrderedDict

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


class Main(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.mPlayerId = clientApi.GetLocalPlayerId()
        self.mLevelId = clientApi.GetLevelId()
        self.data = param.get('data', {})
        self.client = param.get('client', None)

        self.btn_change = {"next":"§a下一页",
                           "close":"§c关闭",
                           "finish":"§b完成",
                           "claim_reward":"§d领取奖励"}


    def Create(self):
        """
        @description UI创建成功时调用
        """
        self.btn_close = self.GetBaseUIControl("/bg/btn_close").asButton()
        self.btn_close.AddTouchEventParams()
        self.btn_close.SetButtonTouchDownCallback(self.btn_close_event)

    def SetData(self,dialogue_id,npc_name,npc_icon,text,step_index,buttons):
        self.GetBaseUIControl("/bg/stack_panel_btn/btn_1").SetScreenVisible(False)
        self.GetBaseUIControl("/bg/stack_panel_btn/btn_2").SetScreenVisible(False)
        self.GetBaseUIControl("/bg/stack_panel_btn/btn_3").SetScreenVisible(False)

        self.lable_title = self.GetBaseUIControl("/bg/panel_head/label").asLabel()
        self.lable_title.SetText(npc_name)

        self.lable_text = self.GetBaseUIControl("/bg/panel_dialog/bg_content/label").asLabel()
        self.lable_text.SetText(text)
        self.lable_text.resetAnimation()

        self.image_npc = self.GetBaseUIControl("/bg/panel_dialog/bg_npc/image").asImage()
        self.image_npc.SetSprite(npc_icon)

        if len(buttons)>0:
            self.GetBaseUIControl("/bg/stack_panel_btn/btn_1").SetScreenVisible(True)
            self.btn_1 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_1").asButton()
            self.btn_1.AddTouchEventParams({"index":0,"type":buttons[0]})
            self.btn_1.SetButtonTouchDownCallback(self.btn_down_cb)

            self.lable_btn_1 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_1/button_label").asLabel()
            self.lable_btn_1.SetText(self.btn_change.get(buttons[0]))

        if len(buttons)>1:
            self.GetBaseUIControl("/bg/stack_panel_btn/btn_2").SetScreenVisible(True)
            self.btn_2 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_2").asButton()
            self.btn_2.AddTouchEventParams({"index":1,"type":buttons[1]})
            self.btn_2.SetButtonTouchDownCallback(self.btn_down_cb)

            self.lable_btn_2 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_2/button_label").asLabel()
            self.lable_btn_2.SetText(self.btn_change.get(buttons[1]))

        if len(buttons)>2:
            self.GetBaseUIControl("/bg/stack_panel_btn/btn_3").SetScreenVisible(True)
            self.btn_3 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_3").asButton()
            self.btn_3.AddTouchEventParams({"index":2,"type":buttons[2]})
            self.btn_3.SetButtonTouchDownCallback(self.btn_down_cb)

            self.lable_btn_3 = self.GetBaseUIControl("/bg/stack_panel_btn/btn_3/button_label").asLabel()
            self.lable_btn_3.SetText(self.btn_change.get(buttons[2]))
    
    def btn_down_cb(self,args):
        Params = args["AddTouchEventParams"]
        btn_index = Params["index"]
        btn_type = Params["type"]
        if btn_type == "next":
            # 下一页
            self.client.NotifyToServer("RequestNextPage", {})
        elif btn_type == "close":
            # 关闭
            self.client.NotifyToServer("RequestClose", {})
            self.client.ui_npcdialog = None
            clientApi.PopScreen()
        elif btn_type == "finish":
            # 完成
            self.client.NotifyToServer("RequestFinish", {})
        elif btn_type == "claim_reward":
            # 领取奖励
            self.client.NotifyToServer("RequestClaimReward", {})

    def btn_close_event(self,args):
        # 关闭
        self.client.NotifyToServer("RequestClose", {})
        self.client.ui_npcdialog = None
        clientApi.PopScreen()


    def Destroy(self):
        """
        @description UI销毁时调用
        """
        pass

    def OnActive(self):
        """
        @description UI重新回到栈顶时调用
        """
        pass

    def OnDeactive(self):
        """
        @description 栈顶UI有其他UI入栈时调用
        """
        pass

    def Update(self):
        pass
