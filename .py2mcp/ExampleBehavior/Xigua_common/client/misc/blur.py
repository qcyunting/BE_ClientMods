# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *


class GaussianBlurController(object):
    def __init__(self):
        self.value = 0
        self.timer = None

    def on_push_screen_event(self, args):
        if args.get("screenName") in ["toast_screen", "in_game_play_screen", "hud_screen"]:
            return
        self._cancel_timer()
        CF.CreatePostProcess(levelId).SetEnableGaussianBlur(True)
        self.value = 1
        CF.CreatePostProcess(levelId).SetGaussianBlurRadius(self.value)

    def on_pop_screen_after_client_event(self, args):
        if args.get("screenName") in ["hud_screen"]:
            self._cancel_timer()
            self.timer = gameComp.AddRepeatedTimer(0.01, self.clear)

    def clear(self):
        self.value -= 0.4
        if self.value < 0:
            self.value = 0
            CF.CreatePostProcess(levelId).SetEnableGaussianBlur(False)
            self._cancel_timer()
            return
        CF.CreatePostProcess(levelId).SetGaussianBlurRadius(self.value)

    def _cancel_timer(self):
        if self.timer is not None:
            gameComp.CancelTimer(self.timer)
            self.timer = None
