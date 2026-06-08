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

        self.game_path = {
            "btn": "/image/s_panel/s_panel_%s/game%s/button",
            "btn_select": "/image/s_panel/s_panel_%s/game%s/button/default",
            "bg": "/image/s_panel/s_panel_%s/game%s/button/image",
            "name": "/image/s_panel/s_panel_%s/game%s/button/image/image/label",
            "name_all": "/image/s_panel/s_panel_%s/game%s/button/image/image",
            "online_tag": {
                "all": "/image/s_panel/s_panel_%s/game%s/button/image/image_tag",
                "label": "/image/s_panel/s_panel_%s/game%s/button/image/image_tag/label",
                "icon": "/image/s_panel/s_panel_%s/game%s/button/image/image_tag/image"
            },
            "paiwei": {
                "all": "/image/s_panel/s_panel_%s/game%s/button/image/paiwei",
                "icon": "/image/s_panel/s_panel_%s/game%s/button/image/paiwei/image",
                "text": "/image/s_panel/s_panel_%s/game%s/button/image/paiwei/label"
            },
            "ban": "/image/s_panel/s_panel_%s/game%s/image_ban"
        }

        self.game_gids = {}

        self.game_select_data = None


    def Create(self):
        """
        @description UI创建成功时调用
        """
        btn_close = self.GetBaseUIControl("/image/btn_close").asButton()
        btn_close.AddTouchEventParams()
        btn_close.SetButtonTouchDownCallback(self.btnclose)

        btn_join = self.GetBaseUIControl("/image/s_panel/s_panel_3/button").asButton()
        btn_join.AddTouchEventParams()
        btn_join.SetButtonTouchDownCallback(self.game_btn_join)
        btn_join.SetTouchEnable(False) #默认不可点击，需要选择后才可

        title = self.data.get("title")
        subtitle = self.data.get("subtitle")
        games = self.data.get("games")
        
        if title:
            label_title = self.GetBaseUIControl("/image/label").asLabel().SetText(title)
        if subtitle:
            label_subtitle = self.GetBaseUIControl("/image/label_sub").asLabel().SetText(subtitle)
        for idx,game in enumerate(games[:8] or []):
            game_idx = idx + 1
            if game_idx < 4:
                pidx = 1
            else:
                pidx = 2

            path = self.game_path
            gid = game.get("id")

            self.game_gids.setdefault(gid,{"game_idx":game_idx,"pidx":pidx})

            name = game.get("name")
            text = game.get("text")
            ui = game.get("ui")
            online = self.data.get("online",0)
            if online<5:
                online = "流畅"
            paiwei = game.get("paiwei")
            
            label_game_name = self.GetBaseUIControl(self._game_path(path["name"], pidx, game_idx)).asLabel().SetText(name or "")
            img_game = self.GetBaseUIControl(self._game_path(path["bg"], pidx, game_idx)).asImage()
            if ui:
                img_game.SetSprite(ui)

            if pidx==1:
                if paiwei:
                    self.GetBaseUIControl(self._game_path(path["paiwei"]["all"], pidx, game_idx)).SetVisible(True)
                    paiwei_icon = paiwei.get("icon")
                    paiwei_name = paiwei.get("name") or ""
                    paiwei_score = paiwei.get("score") or ""
                    if paiwei_icon:
                        self.GetBaseUIControl(self._game_path(path["paiwei"]["icon"], pidx, game_idx)).asImage().SetSprite(paiwei_icon)
                    self.GetBaseUIControl(self._game_path(path["paiwei"]["text"], pidx, game_idx)).asLabel().SetText("%s\n%s" % (paiwei_name, paiwei_score))
                else:
                    self.GetBaseUIControl(self._game_path(path["paiwei"]["all"], pidx, game_idx)).SetVisible(False)
            else:
                self.GetBaseUIControl(self._game_path(path["paiwei"]["all"], pidx, game_idx)).SetVisible(False)
            
            online_label = self.GetBaseUIControl(self._game_path(path["online_tag"]["label"], pidx, game_idx)).asLabel().SetText(online)
            
            btn_game = self.GetBaseUIControl(self._game_path(path["btn"], pidx, game_idx)).asButton()
            btn_game.AddTouchEventParams({"gid":gid})
            btn_game.SetButtonTouchDownCallback(self.game_select)
        if len(games[:8])<8:
            for i in range(8-len(games[:8])):
                game_idx = 8-i
                if game_idx < 4:
                    pidx = 1
                else:
                    pidx = 2
                self.GetBaseUIControl(self._game_path(path["ban"], pidx, game_idx)).SetVisible(True)
                self.GetBaseUIControl(self._game_path(path["ban"], pidx, game_idx)).asImage().SetSprite("textures/gameselect/black/qidai")
                self.GetBaseUIControl(self._game_path(path["name_all"], pidx, game_idx)).SetVisible(False)
                self.GetBaseUIControl(self._game_path(path["online_tag"]["all"], pidx, game_idx)).SetVisible(False)
                self.GetBaseUIControl(self._game_path(path["paiwei"]["all"], pidx, game_idx)).SetVisible(False)
                self.GetBaseUIControl(self._game_path(path["btn"], pidx, game_idx)).SetTouchEnable(False)

    def _game_path(self, path, pidx, game_idx):
        return path % (pidx, game_idx)

    def _optional_control(self, path):
        try:
            return self.GetBaseUIControl(path)
        except:
            return None

    
    def game_select(self,args):
        Params = args.get("AddTouchEventParams")
        gid = Params.get("gid")
        if Params:
            # 由原来的点击即可加入，变成选择后按钮进入
            # self.client.send_to_server(gid,{})
            # clientApi.PopScreen()
            self.game_rec_select(gid)
    
    def game_rec_select(self,gid):
        path = self.game_path
        gid_data = self.game_gids.get(gid)
        if gid_data:
            pidx = gid_data["pidx"]
            game_idx = gid_data["game_idx"]
            rec_select = "textures/gameselect/rec_select"
            if self.game_select_data:
                old_pidx = self.game_select_data.get("pidx")
                old_game_idx = self.game_select_data.get("game_idx")
                if old_pidx and old_game_idx:
                    self.GetBaseUIControl(self._game_path(path["btn_select"], old_pidx, old_game_idx)).asImage().SetSprite("")
            self.GetBaseUIControl(self._game_path(path["btn_select"], pidx, game_idx)).asImage().SetSprite(rec_select)
            self.game_select_data = {"gid":gid,"pidx":pidx,"game_idx":game_idx}
            btn_join = self.GetBaseUIControl("/image/s_panel/s_panel_3/button").asButton()
            btn_join.SetTouchEnable(True) #设置可点击
    
    def game_btn_join(self,args):
        gid = self.game_select_data.get("gid")
        print "game_btn_join",gid
        if gid!=None:
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
