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

requestUidUsername_data = {
    "uid": {
        "username": str(),
        "lv": int(),
        "state": str(),
        "headImageUrl": str(),
        "frameImageUrl": str()
    }
}
