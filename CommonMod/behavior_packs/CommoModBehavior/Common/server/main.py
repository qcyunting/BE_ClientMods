# -*- coding: utf-8 -*-
"""
Created on 2025-11-03
服务端系统
"""
from utils import *
from .module.Template import TemplateModule


class Main(BaseServer):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        self.Template = None

    @Listen()
    def LoadServerAddonScriptsAfter(self, args):
        self.register_module()  # 注册模块

    def register_module(self):
        self.Template = TemplateModule()

    @Listen(event_type=Listen.client)
    def createPunctuation(self, args):
        self.BroadcastToAllClient("createPunctuation", args)

