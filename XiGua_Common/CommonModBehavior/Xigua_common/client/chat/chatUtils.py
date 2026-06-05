# -*- coding: utf-8 -*-
import json
from ..utils import escape
import time
instance = escape.Escape()
network_proxy = instance.importModule("network_proxy")
utility = instance.importModule("utility")
gui = instance.importModule("gui")
player_tips_screen_controller = instance.importModule("player_tips_screen_controller")


def download_player_head_image(pid, uid):
    player_tips_screen_controller.instance().request_head_image_from_web(pid, uid)

def set_sprite(ScreenName, FullPath, filePath):
    gui.set_sprite(ScreenName, FullPath, filePath, "RawPath")

def set_user_head(ScreenName, FullPath, uid):
    headFilePath = utility.get_stream_temp_folder(uid + 'head_image.png')
    gui.set_sprite(ScreenName, FullPath, headFilePath, "RawPath")

def set_user_frame(ScreenName, FullPath, uid):
    frameFilePath = utility.get_stream_temp_folder(uid + 'frame_image.png')
    gui.set_sprite(ScreenName, FullPath, frameFilePath, "RawPath")

def requestUidUsername(uids, callback):
    if not uids:
        return
    onResponse = lambda data, callback=callback: requestUidUsernameCallback(data, callback)
    network_proxy.cs_get_user_detail_batch(uids, onResponse, with_game_state=True)
    return

def requestUidUsernameCallback(data, callback):
    handleData = {}
    if data:
        entities = data.get('entities')
        if entities:
            for entity in entities:
                id = str(entity['id'])
                handleData[id] = {}
                username = entity['nickname']
                headImageType = entity.get('headImageType', 0)
                handleData[id]['username'] = username
                if headImageType == 0:
                    handleData[id]['headImageUrl'] = entity['headImage']
                elif headImageType == 1:
                    handleData[id]['headImageUrl'] = entity['static_url']
                handleData[id]['frameImageUrl'] = entity['frame_id']
    callback and callback(handleData)
requestUidUsername_data = {
    "uid": {
        "username": str(),
        "headImageUrl": str(),
        "frameImageUrl": str()
    }
}
