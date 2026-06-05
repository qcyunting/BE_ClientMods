# -*- coding: utf-8 -*-
from ...utils.ui_utils import *

class WatermarkUtils:
    def __init__(self, hud_instance):
        self.hud = hud_instance

    def set_test_server(self, args):
        self.hud.is_test_server = args.get("is_test_server", False)
        self.hud.screen.GetBaseUIControl(BP + "/root_panel_watermelon/test_watermark").SetVisible(self.hud.is_test_server)