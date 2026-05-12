# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from ..utils import escape

escapeInstance = escape.instance


def test_shop():
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

    network_proxy.store_query_currency(store_query_currency_success_callback, store_query_currency_fail_callback)
    """
    返回示例
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
            print "所有分组", group_id, name
            network_proxy.store_search_by_group(game_id=gameId, group_id=group_id, offset=0, length=50, group_name=name, mc_type=serverType, callback=success_callback, except_callback=fail_callback)

    def store_query_groups_fail_callback(args):
        print "返回失败", args

    network_proxy.store_query_groups(game_id=gameId, offset=0, length=50, callback=store_query_groups_success_callback, except_callback=store_query_groups_fail_callback)
    """
    返回示例
    {'code': 0, 'entities': [{'group_id': '4677569137654129296', 'name': 'test_1771765859'}], 'message': '正常返回', 'total': 1, 'details': ''}
    """

    print "mc_type:", serverType
    network_proxy.store_search_by_group(game_id="4677569137654129296", group_id="4677569137654129296", offset=0, length=50, group_name="test_1771765859", mc_type=serverType, callback=success_callback, except_callback=fail_callback)
    """
    返回示例
    {'code': 0, 'entities': [{'group_id': '4677569137654129296', 'name': 'test_1771765859'}], 'message': '正常返回', 'total': 1, 'details': ''}
    """

    network_proxy.store_get_item_details("4686001246373889702", success_callback, fail_callback)
    network_proxy.store_buy_item("4686001246373889702", 5, 2, success_callback, fail_callback)
    #network_proxy.store_buy_item_result("1", buy_type, success_callback, fail_callback)
