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
        self.next_locked = False
        self.next_requesting = False
        self.LevelId = clientApi.GetLevelId()


    def Create(self):
        self.CreateStatus = True

        root = self.GetBaseUIControl("/image")
        if root:
            root.SetVisible(False)

        self.SetData(self.data)

        


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
        self.next_locked = True
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
                self.next_locked = False
                self._cancel_delay_timer()
            else:
                l.SetText("§7下一页(%ss)" % str(self.delay_next))

        comp = clientApi.GetEngineCompFactory().CreateGame(self.LevelId)
        self.Timer_delay_next = comp.AddRepeatedTimer(1.0, btn_countdown, indexB=index)

    def _disable_button(self, btn_index):
        pathA = "/stack_panel_btn/button%s" % (btn_index + 1)
        ctrl = self.GetBaseUIControl(pathA)
        btn = ctrl.asButton() if ctrl else None
        if btn:
            btn.SetTouchEnable(False)

    def _close_screen(self):
        self._cancel_delay_timer()
        if self.client and getattr(self.client, "ui_npcdialog", None) is self:
            self.client.ui_npcdialog = None
            
    def SetData(self,args):

        dialogue_id = args.get("dialogue_id")
        npc_name = args.get("npc_name")
        npc_icon = args.get("npc_icon")
        text = args.get("text")
        step_index = int(args.get("step_index",0))
        buttons = args.get("buttons")

        if not self.CreateStatus:
            # UI未创建完成
            self.tasks = []
            self.tasks.append(
                lambda: self.SetData(dialogue_id)
            )
            return
        # if self.dialogue_id==dialogue_id and self.step_index==step_index:
        #     # 重复发同一个对话
        #     return
        try:
            self.dialogue_id = dialogue_id
            self.step_index = step_index

            self.delay_next = 3
            self.next_locked = False
            self.next_requesting = False
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
                if btn is None:
                    return

                btn.SetTouchEnable(False)
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
                else:
                    btn.SetTouchEnable(True)

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
            self._disable_button(btn_index)
            if self.next_locked or self.next_requesting:
                return
            self.next_requesting = True
            self.client.NotifyToServerF("RequestNextPage", {})
            clientApi.PopScreen()
        elif btn_type == "close":
            # 关闭
            self._disable_button(btn_index)
            self.client.NotifyToServerF("RequestClose", {})
            self._close_screen()
            clientApi.PopScreen()
        elif btn_type == "finish":
            # 完成
            self._disable_button(btn_index)
            self.client.NotifyToServerF("RequestFinish", {})
            self._close_screen()
            clientApi.PopScreen()
        elif btn_type == "claim_reward":
            # 领取奖励
            self._disable_button(btn_index)
            self.client.NotifyToServerF("RequestClaimReward", {})
            clientApi.PopScreen()


    def btn_close_event(self,args):
        # 关闭
        self.client.NotifyToServerF("RequestClose", {})
        self._close_screen()


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
