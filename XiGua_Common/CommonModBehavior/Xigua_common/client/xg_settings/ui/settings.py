# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
import tab_button

class Settings(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Settings, self).__init__(screenName, screenNode)
        self.tab_button_instance = tab_button.TabButton(self, 0)

    def OnCreate(self):
        self.tab_button_instance.addStartAnimation(self.tab_button_instance.tab_selected_index)

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged, "#tab_toggle_btn")
    def tab_toggle_btn_click(self, args):
        self.tab_button_instance.onClick(args["index"])

    @ViewBinder.binding(ViewBinder.BF_BindInt, "#tab_index")
    def return_tab_index(self):
        return self.tab_button_instance.tab_selected_index