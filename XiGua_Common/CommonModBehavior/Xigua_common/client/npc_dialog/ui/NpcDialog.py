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
        
        self.dialogue_id = None
        self.step_index = None

        self.tasks = []
        self.CreateStatus = False

        self.delay_next = None
        self.Timer_delay_next = None
        self.LevelId = clientApi.GetLevelId()


    def Create(self):
        self.CreateStatus = True

        root = self.GetBaseUIControl("/image")
        if root:
            root.SetVisible(False)

        tasks = self.tasks[:]
        self.tasks = []
        for F in tasks:
            F()


    def _cancel_delay_timer(self):
        if self.Timer_delay_next is not None:
            try:
                comp = clientApi.GetEngineCompFactory().CreateGame(self.LevelId)
                comp.CancelTimer(self.Timer_delay_next)
            except:
                pass
            self.Timer_delay_next = None

    def delay_nextF(self, index, delay):
        self.delay_next = int(delay)
        self._cancel_delay_timer()

        pathB = "/stack_panel_btn/button%s/button_label" % (index + 1)
        pathA = "/stack_panel_btn/button%s" % (index + 1)

        ctrl_label = self.GetBaseUIControl(pathB)
        ctrl_btn = self.GetBaseUIControl(pathA)
        if ctrl_label is None or ctrl_btn is None:
            return
        btn_lable = ctrl_label.asLabel()
        btn = ctrl_btn.asButton()
        if btn_lable is None or btn is None:
            return

        # 立即生效，避免“慢一拍”
        btn.SetTouchEnable(False)
        btn_lable.SetText("§7下一页(%ss)" % str(self.delay_next))

        def btn_countdown(indexB):
            if not self.CreateStatus:
                self._cancel_delay_timer()
                return

            pathB2 = "/stack_panel_btn/button%s/button_label" % (indexB + 1)
            pathA2 = "/stack_panel_btn/button%s" % (indexB + 1)
            c_label = self.GetBaseUIControl(pathB2)
            c_btn = self.GetBaseUIControl(pathA2)
            if c_label is None or c_btn is None:
                self._cancel_delay_timer()
                return

            l = c_label.asLabel()
            b = c_btn.asButton()
            if l is None or b is None:
                self._cancel_delay_timer()
                return

            self.delay_next -= 1
            if self.delay_next <= 0:
                l.SetText("§a下一页")
                b.SetTouchEnable(True)
                self._cancel_delay_timer()
            else:
                l.SetText("§7下一页(%ss)" % str(self.delay_next))

        comp = clientApi.GetEngineCompFactory().CreateGame(self.LevelId)
        self.Timer_delay_next = comp.AddRepeatedTimer(1.0, btn_countdown, indexB=index)


    def Destroy(self):
        self.CreateStatus = False
        self._cancel_delay_timer()
        if self.client and getattr(self.client, "ui_npcdialog", None) is self:
            self.client.ui_npcdialog = None


    def SetData(self,dialogue_id,npc_name,npc_icon,text,step_index,buttons):
        if not self.CreateStatus:
            # UI未创建完成
            self.tasks = []
            self.tasks.append(
                lambda: self.SetData(dialogue_id, npc_name, npc_icon, text, step_index, buttons)
            )
            return
        # if self.dialogue_id==dialogue_id and self.step_index==step_index:
        #     # 重复发同一个对话
        #     return
        try:
            self.dialogue_id = dialogue_id
            self.step_index = step_index

            self.delay_next = 3
            self._cancel_delay_timer()
            for i in range(5):
                path = "/stack_panel_btn/button%s" % (i+1)
                self.GetBaseUIControl(path).SetVisible(False)
            
            self.lable_title = self.GetBaseUIControl("/image/label_title").asLabel()
            self.lable_title.SetText(npc_name)

            self.lable_text = self.GetBaseUIControl("/image/label_text").asLabel()
            self.lable_text.SetText(text)

            self.image_npc = self.GetBaseUIControl("/image/image_icon").asImage()
            self.image_npc.SetSprite(npc_icon)

            def btn_set(index,type):
                pathA = "/stack_panel_btn/button%s" % (index+1)
                self.GetBaseUIControl(pathA).SetVisible(True)
                ctrl = self.GetBaseUIControl(pathA)
                btn = ctrl.asButton() if ctrl else None
                if btn:
                    btn.SetTouchEnable(False)

                btn.SetTouchEnable(True)
                btn.AddTouchEventParams({"index":index,"type":type})
                btn.SetButtonTouchDownCallback(self.btn_down_cb)

                pathB = "/stack_panel_btn/button%s/button_label" % (index+1)
                btn_lable = self.GetBaseUIControl(pathB).asLabel()
                btn_lable.SetText(self.btn_change.get(type))

                pathC = "/stack_panel_btn/button%s/image" % (index+1)
                btn_image = self.GetBaseUIControl(pathC).asImage()
                btn_image.SetSprite("textures/npcdialog/" + type)

                if type=="next":
                    self.delay_nextF(index,3)

            for index,type in enumerate(buttons[:5]):
                btn_set(index,type)

            # 设置显隐动画
            self.image_dialog = self.GetBaseUIControl("/image").asImage()
            self.image_dialog.resetAnimation()
            self.stack_panel_btn = self.GetBaseUIControl("/stack_panel_btn").asStackPanel()
            self.image_dialog.resetAnimation()
            root = self.GetBaseUIControl("/image")
            if root:
                root.SetVisible(True)
                

        except Exception as e:
            print "[ERROR]SetData",e
            
    
    def btn_down_cb(self,args):
        Params = args["AddTouchEventParams"]
        btn_index = Params["index"]
        btn_type = Params["type"]
        if btn_type == "next":
            # 下一页
            pathA = "/stack_panel_btn/button%s" % (btn_index + 1)
            btn = self.GetBaseUIControl(pathA).asButton()
            if btn:
                btn.SetTouchEnable(False)
            self.client.NotifyToServerF("RequestNextPage", {})
        elif btn_type == "close":
            # 关闭
            self.client.NotifyToServerF("RequestClose", {})
            self.client.ui_npcdialog = None
            clientApi.PopScreen()
        elif btn_type == "finish":
            # 完成
            self.client.NotifyToServerF("RequestFinish", {})
        elif btn_type == "claim_reward":
            # 领取奖励
            self.client.NotifyToServerF("RequestClaimReward", {})

    def btn_close_event(self,args):
        # 关闭
        self.client.NotifyToServerF("RequestClose", {})
        self.client.ui_npcdialog = None
        clientApi.PopScreen()


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
