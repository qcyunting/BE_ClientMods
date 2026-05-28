# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
import math


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
    def OnCreate(self):
        pass

    def OnDestroy(self):
        pass
