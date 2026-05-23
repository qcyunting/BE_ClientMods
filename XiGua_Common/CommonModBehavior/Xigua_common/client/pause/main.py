# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *


class Pause(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Pause, self).__init__(namespace, systemName)

    @Listen()
    def UiInitFinished(self, args):
        """
        ui创建成功
        """
        self.NotifyToServer("UiInitFinished", dict())
