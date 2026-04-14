# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *
from ..utils.listen_util import *

class Decoration(BaseSystem):
    def __init__(self, namespace, systemName):
        super(Decoration, self).__init__(namespace, systemName)
        self.modelId = 0

    @Listen()
    def UiInitFinished(self, args):
        pass