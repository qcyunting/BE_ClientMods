# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from HyperClashModScripts.modCommon.modConfig import ModName

ScreenNode = clientApi.GetScreenNodeCls()

class ShopUI(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.clientSystem = clientApi.GetSystem(ModName, "ShopSystem")
        self.shopData = param if param else {}
        self.selectedItemId = None
        self.currentTab = None
        self.entityId = None
        self.levelId = clientApi.GetLevelId()

        # 路径映射
        # 指向 common.scrolling_panel 模板内部的真实内容路径
        
        self.mPaths = {
            "detail_icon": "/left/image/icon/item",
            "detail_title": "/left/image/des/stack_panel/title",
            "detail_desc": "/left/image/des/stack_panel/des",
            "btn_buy": "/left/image/des/btn_group/buy",
            "btn_sell": "/left/image/des/btn_group/sell",
            "close_btn": "/right/image/btn_close",  # 关闭按钮
            
            # 指向深层的 Grid
            "goods_grid": "/right/image/top/scroll_view",
            "history_grid": "/right/image/buttom/grid",
            "tab_panel": "/right/stack_panel_tab"
        }

    def Create(self):
        print "==== ShopUI Create ===="
        try:
            # 确保 ScrollView 可见
            scroll = self.GetBaseUIControl("/right/image/top/scroll_view")
            if scroll: scroll.SetVisible(True)

            if self.shopData:
                self.currentTab = self.shopData.get("current_tab", "")
                self.selectedItemId = self.shopData.get("selected_item_id", "")
                self.entityId = self.shopData.get("entityId", "")

                comp = clientApi.GetEngineCompFactory().CreateGame(self.levelId)
                comp.AddTimer(0.1,self.delay_init)
                
                
            
            self._bindButtonEvents()
            
        except Exception as e:
            print "[ShopUI] Error in Create:", e
    
    def delay_init(self):
        self._renderCategories()
        self._renderGoods()
        self._renderHistory()
        self._renderDetail()

    def _renderGoods(self):
        # 渲染商品

        goods = self.shopData.get("goods", [])
        gridPath = self.mPaths["goods_grid"]
        
        # 获取控件并转换为 Grid
        ScrollView = self.GetBaseUIControl(gridPath).asScrollView()
        ScrollViewCtrl = ScrollView.GetScrollViewContentControl()
        gridCtrl = ScrollViewCtrl
        if gridCtrl:
            gridCtrl = gridCtrl.asGrid()
        
        if not gridCtrl:
            print "[ShopUI] Error: Goods Grid not found at", gridPath
            return
        
        total_goods = len(goods)
        # 计算行数 (每行3个)
        rows = (total_goods + 2) // 3
        gridCtrl.SetGridDimension((3, rows))
        
        print "[ShopUI] Rendering {} goods in {} rows".format(total_goods, rows)

        goodid = 0
        for good in goods:
            goodid+=1
            if goodid>3:
                x = goodid % 3
            else:
                x = goodid - 1
            y = goodid//3
            gridchild = gridCtrl.GetGridItem(x, y)
            self._updateGoodsItem(gridchild,good)


    def _updateGoodsItem(self, gridchild, item):
        # 更新商品格子内容
        def getbaseui(path):
            gridchild.GetChildByPath(path)
        base = "/item/button/image"
        
        nameCtrl = getbaseui(base + "/label")
        if nameCtrl: nameCtrl.asLabel().SetText(item.get("name", ""))
        
        priceCtrl = getbaseui(base + "/lable_coin")
        if priceCtrl: priceCtrl.asLabel().SetText(str(item.get("price", 0)))
        
        iconCtrl = getbaseui(base + "/icon/item")
        if iconCtrl: iconCtrl.asImage().SetSprite(self._getItemTexture(item.get("icon")))
        
        # 绑定点击
        btnCtrl = getbaseui("/item/button").asButton()
        btnCtrl.AddTouchEventParams({"iid":item.get("id")})
        def cb(args):
            iid = args["AddTouchEventParams"].get("iid")
            self._onItemClick(iid)
        btnCtrl.SetButtonTouchDownCallback(cb)

    def _renderHistory(self):
        # 渲染购买记录
        try:
            history = self.shopData.get("history", [])
            gridPath = self.mPaths["history_grid"]
            
            gridCtrl = self.GetBaseUIControl(gridPath)
            if gridCtrl: gridCtrl = gridCtrl.asGrid()
            
            if not gridCtrl: return
            gridCtrl.RemoveAllChildren()

            for i, item in enumerate(history):
                childName = "hist_{}".format(i)
                self.Clone("shop.item_mini", gridPath, childName)
                
                itemPath = "{}/{}".format(gridPath, childName)
                
                self.GetBaseUIControl(itemPath + "/label").asLabel().SetText(item.get("name", ""))
                self.GetBaseUIControl(itemPath + "/image/icon/item").asImage().SetSprite(self._getItemTexture(item.get("icon")))
                
                bgCtrl = self.GetBaseUIControl(itemPath + "/image")
                if bgCtrl:
                    bgCtrl.SetTouchEnable(True)
                    def _touch(args):
                        if args["TouchEvent"] == 1:
                            self._onItemClick(item.get("id"))
                    bgCtrl.SetTouchEventHandler(_touch)
                    
        except Exception as e:
            print "[ShopUI] Error in _renderHistory:", e

    def _bindButtonEvents(self):
        # 绑定底部按钮
        for btnName, func in [("btn_buy", self._onBuyClick), ("btn_sell", self._onSellClick)]:
            btn = self.GetBaseUIControl(self.mPaths[btnName])
            if btn and btn.asButton():
                btn.asButton().AddTouchEventParams({"isSwallow": True})
                btn.asButton().SetButtonTouchUpCallback(func)
                
        # 绑定关闭按钮
        closeBtn = self.GetBaseUIControl(self.mPaths["close_btn"])
        if closeBtn and closeBtn.asButton():
            closeBtn.asButton().AddTouchEventParams({"isSwallow": True})
            closeBtn.asButton().SetButtonTouchUpCallback(self._onCloseClick)

    def _onCloseClick(self, args):
        print "[ShopUI] Close clicked"
        clientApi.PopScreen()

    def _renderCategories(self):
        categories = self.shopData.get("categories", [])
        tabNames = ["tab1", "tab2", "tab3", "tab4", "tab5", "tab6"]
        for i, tabName in enumerate(tabNames):
            tabPath = self.mPaths["tab_panel"] + "/" + tabName
            tabCtrl = self.GetBaseUIControl(tabPath)
            if not tabCtrl: continue
            
            if i < len(categories):
                cat = categories[i]
                self.GetBaseUIControl(tabPath + "/button_label").asLabel().SetText(cat.get("name"))
                img = self.GetBaseUIControl(tabPath + "/image").asImage()
                if cat.get("id") == self.currentTab:
                    img.SetSprite("textures/ui/TabTopFrontLeftMost")
                else:
                    img.SetSprite("textures/ui/TabTopBack")
                
                btn = tabCtrl.asButton()
                btn.AddTouchEventParams({"isSwallow": True})
                def mk_cb(cid): return lambda x: self._onTabClick(cid)
                btn.SetButtonTouchUpCallback(mk_cb(cat.get("id")))
                tabCtrl.SetVisible(True)
            else:
                tabCtrl.SetVisible(False)

    def _renderDetail(self):
        detail = self.shopData.get("selected_detail")
        if not detail:
            self.GetBaseUIControl(self.mPaths["detail_title"]).asLabel().SetText("")
            self.GetBaseUIControl(self.mPaths["detail_desc"]).asLabel().SetText("")
            return
            
        self.GetBaseUIControl(self.mPaths["detail_title"]).asLabel().SetText(detail.get("name", ""))
        self.GetBaseUIControl(self.mPaths["detail_desc"]).asLabel().SetText("\n".join(detail.get("lore", [])))
        self.GetBaseUIControl(self.mPaths["detail_icon"]).asImage().SetSprite(self._getItemTexture(detail.get("icon")))
        
        self.GetBaseUIControl(self.mPaths["btn_buy"] + "/button_label").asLabel().SetText(" 购买({})".format(detail.get("price")))
        self.GetBaseUIControl(self.mPaths["btn_sell"] + "/button_label").asLabel().SetText(" 出售({})".format(detail.get("sell_price")))

    def _getItemTexture(self, name):
        if not name: return "textures/items/barrier"
        name = name.lower()
        name = name.replace("golden_", "gold_").replace("wooden_", "wood_")
        if "block" in name or "ore" in name or "stone" in name or "grass" in name:
            return "textures/blocks/" + name
        return "textures/items/" + name

    def _onTabClick(self, cid):
        if cid == self.currentTab: return
        self.clientSystem.NotifyToServer("RequestSwitchCategory", {"entityId": self.entityId, "categoryId": cid})

    def _onItemClick(self, iid):
        self.selectedItemId = iid
        self.clientSystem.NotifyToServer("RequestSelectItem", {"entityId": self.entityId, "itemId": iid})

    def _onBuyClick(self, args):
        if self.selectedItemId:
            self.clientSystem.NotifyToServer("RequestBuyItem", {"entityId": self.entityId, "itemId": self.selectedItemId})

    def _onSellClick(self, args):
        if self.selectedItemId:
            self.clientSystem.NotifyToServer("RequestSellItem", {"entityId": self.entityId, "itemId": self.selectedItemId})

    def UpdateShopData(self, data):
        self.shopData = data
        self.Create()

    def UpdateItemDetail(self, detail):
        if detail:
            self.shopData["selected_detail"] = detail
            self._renderDetail()

    def Destroy(self):
        if self.clientSystem: self.clientSystem.shopUI = None