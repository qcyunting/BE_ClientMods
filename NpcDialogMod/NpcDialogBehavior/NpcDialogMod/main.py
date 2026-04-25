# -*- coding: utf-8 -*-
"""
Created on 2026-02-15
客户端系统
"""
from utils import *


class Main(BaseState):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)


    def on_enable(self):
        logger.info(modName + "_MOD启动")

    def on_disable(self):
        logger.info(modName + "_MOD关闭")