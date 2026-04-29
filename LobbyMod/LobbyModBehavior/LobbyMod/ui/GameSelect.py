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

        self.LevelId = clientApi.GetLevelId()

        self.game_path = {"btn":"/image/s_panel/s_panel_%s/game%s/button",
                           "bg":"/image/s_panel/s_panel_%s/game%s/button/image",
                           "name":"/image/s_panel/s_panel_%s/game%s/button/image/image/label",
                           "paiwei":{"all":"/image/s_panel/s_panel_%s/game%s/button/image/paiwei",
                                     "icon":"/image/s_panel/s_panel_%s/game%s/button/image/paiwei/image",
                                     "text":"/image/s_panel/s_panel_%s/game%s/button/image/paiwei/label"
                                     }}


    def Create(self):
        """
        @description UI创建成功时调用
        """
        btn_close = self.GetBaseUIControl("/image/btn_close").asButton()
        btn_close.AddTouchEventParams()
        btn_close.SetButtonTouchDownCallback(self.btnclose)

        title = self.data.get("title")
        subtitle = self.data.get("subtitle")
        games = self.data.get("games")
        
        if title:
            label_title = self.GetBaseUIControl("/image/label").asLabel().SetText(title)
        if subtitle:
            label_subtitle = self.GetBaseUIControl("/image/label_sub").asLabel().SetText(subtitle)
        for idx,game in enumerate(games):
            if idx+1<4:
                pidx = 1
            else:
                pidx = 2

            path = self.game_path
            gid = game.get("id")
            name = game.get("name")
            text = game.get("text")
            ui = game.get("ui")
            paiwei = game.get("paiwei")
            
            label_game_name = self.GetBaseUIControl(path["name"] % (pidx,idx+1)).asLabel().SetText(name)
            img_game = self.GetBaseUIControl(path["bg"] % (pidx,idx+1)).asImage().SetSprite(ui)
            if pidx==1:
                if paiwei:
                    paiwei_icon = paiwei.get("icon")
                    paiwei_name = paiwei.get("name")
                    paiwei_score = paiwei.get("score")
                else:
                    img_paiwei = self.GetBaseUIControl(path["paiwei"]["all"] % (pidx,idx+1)).SetVisible(False)
            
            btn_game = self.GetBaseUIControl(path["btn"] % (pidx,idx+1)).asButton()
            btn_game.AddTouchEventParams({"gid":gid})
            btn_game.SetButtonTouchDownCallback(self.game_select)

    
    def game_select(self,args):
        Params = args.get("AddTouchEventParams")
        gid = Params.get("gid")
        if Params:
            # 需插件修复后填写
            self.client.send_to_server(gid,{})
            clientApi.PopScreen()

    def btnclose(self,args):
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
