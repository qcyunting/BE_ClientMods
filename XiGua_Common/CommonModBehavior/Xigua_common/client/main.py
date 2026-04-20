# -*- coding: utf-8 -*-
from utils.ClientSystem_utils import *
from utils import escape
escapeInstance = escape.instance

NativeScreenManager = clientApi.GetNativeScreenManagerCls()

class Main(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.game_info_text = playerName
        self.GaussianBlurValue = 0
        self.GaussianBlurTimer = None
        # 注册代理UI
        self.regScreenProxy()

    @Listen(event_type=Listen.server)
    def startMod(self, args):
        print("startMod", args)
        self.BroadcastEvent("StartMod", args["all_mod"])

    @Listen(event_type=Listen.server)
    def SetGameInfoText(self, args):
        """
        设置游戏信息文本
        """
        self.game_info_text = args["text"]

    @Listen()
    def UiInitFinished(self, args):
        """
        ui创建创建成功
        """

        self.NotifyToServer('UiInitFinished', dict())

    @Listen()
    def OnKeyPressInGame(self, args):
        if args["isDown"] == "1":
            if args["key"] == "18":
                CF.CreateCamera(levelId).DepartCamera()
        else:
            if args["key"] == "18":
                CF.CreateCamera(levelId).UnDepartCamera()


    def test_shop(self):
        network_proxy = escapeInstance.importModule("network_proxy")
        mc_game_ctrl = escapeInstance.importModule("mc_game_ctrl")

        if mc_game_ctrl.instance.is_in_lobby_game:
            gameId = mc_game_ctrl.instance.getCurGameInfo()['res_id']
            serverType = 1
        elif mc_game_ctrl.instance.is_in_network_game:
            gameId = mc_game_ctrl.instance.getCurGameInfo()['id']
            serverType = 2
        else:
            logger.info('NeteaseShop no support this game type')
            return
        gameId = str(gameId)
        diamond = 0
        points = 0
        def store_query_currency_success_callback(args):
            entity = args["entity"]
            diamond = entity["pay_diamond"] + entity["free_diamond"]
            points = entity["current_cash"] + entity["last_cash"]
        def store_query_currency_fail_callback(args):
            print "返回失败", args
        # 1. 查询货币
        network_proxy.store_query_currency(store_query_currency_success_callback, store_query_currency_fail_callback)
        """返回示例
        {'message': '正常返回', 'code': 0, 'details': '', 'entity': {'pay_diamond': 99999, 'bind_diamond': '100', 'current_cash': 16099839, 'last_cash': 0, 'free_diamond': 0, 'currency_time': 1774527574, 'last_cash_time': '202401', 'current_cash_time': '202603'}}
        """
        def success_callback(args):
            print "返回成功", args
        def fail_callback(args):
            print "返回失败", args

        goods = {}
        def store_query_groups_success_callback(args):
            entities = args["entities"]
            for i in entities:
                group_id = i["group_id"]
                name = i["name"]
                goods[group_id] = name
                print "所有分类", group_id, name
                network_proxy.store_search_by_group(game_id=gameId, group_id=group_id, offset=0, length=50, group_name=name, mc_type=serverType, callback=success_callback, except_callback=fail_callback)

        def store_query_groups_fail_callback(args):
            print "返回失败", args
        # 2. 查询商品分组
        """
        offset = 偏移量
        length = 每页长度
        """
        network_proxy.store_query_groups(game_id=gameId, offset=0, length=50, callback=store_query_groups_success_callback, except_callback=store_query_groups_fail_callback)
        """返回示例
        {'code': 0, 'entities': [{'group_id': '4677569137654129296', 'name': 'test_1771765859'}], 'message': '正常返回', 'total': 1, 'details': ''}
        """

        # 3. 按分组搜索商品
        """
        mc_type = 0(本地游戏) / 1(联机大厅) / 2(网络游戏)
        """
        print "mc_type:", serverType
        network_proxy.store_search_by_group(game_id="4677569137654129296", group_id="4677569137654129296", offset=0, length=50, group_name="test_1771765859", mc_type=serverType, callback=success_callback, except_callback=fail_callback)
        """返回示例
        {'code': 0, 'entities': [{'group_id': '4677569137654129296', 'name': 'test_1771765859'}], 'message': '正常返回', 'total': 1, 'details': ''}
        """

        # 4. 获取商品详情
        network_proxy.store_get_item_details("4686001246373889702", success_callback, fail_callback)

        # 5. 购买商品
        network_proxy.store_buy_item("4686001246373889702", 5, 2, success_callback, fail_callback)

        # 6. 购买结果查询
        #network_proxy.store_buy_item_result("1", buy_type, success_callback, fail_callback)

        # 7. RPC调用 - 服务端通知
        #rpc.CServerRpc().UrgeShipEvent()  # 催促发货
        #rpc.CServerRpc().StoreBuySuccServerEvent()  # 购买成功通知
        #rpc.CServerRpc().lobbyGoodBuySucServerEvent(event_data)  # 大厅商品购买成功

    def regScreenProxy(self):
        screen_list = {
            "hud.hud_screen": "Xigua_common.client.ui.hud_proxys.Main",
            "pause.pause_screen": "Xigua_common.client.ui.pause_ui_proxys.Main"
        }
        clientApi.HideChangePersonGui(True)  # 隐藏切换人称的按钮
        clientApi.HidePauseGUI(True)  # 隐藏暂停按钮
        clientApi.HideChatGUI(True)
        clientApi.HideFoldGUI(True)
        clientApi.HideVoiceGUI(True)
        for screenName, proxyClassName in screen_list.items():
            NativeScreenManager.instance().RegisterScreenProxy(
                screenName, proxyClassName
            )

    @Listen()
    def PushScreenEvent(self, args):
        if args.get("screenName") in ["toast_screen", "in_game_play_screen", "hud_screen"]:
            return
        gameComp.CancelTimer(self.GaussianBlurTimer)
        CF.CreatePostProcess(levelId).SetEnableGaussianBlur(True)
        self.GaussianBlurValue = 1
        CF.CreatePostProcess(levelId).SetGaussianBlurRadius(self.GaussianBlurValue)

    @Listen()
    def PopScreenAfterClientEvent(self, args):
        if args.get("screenName") in ["hud_screen"]:
            self.GaussianBlurTimer = gameComp.AddRepeatedTimer(0.01, self.clearGaussianBlur)

    def clearGaussianBlur(self):
        self.GaussianBlurValue -= 0.4
        if self.GaussianBlurValue < 0:
            self.GaussianBlurValue = 0
            CF.CreatePostProcess(levelId).SetEnableGaussianBlur(False)
            gameComp.CancelTimer(self.GaussianBlurTimer)
            return
        CF.CreatePostProcess(levelId).SetGaussianBlurRadius(self.GaussianBlurValue)

