# coding=utf-8
"""
Created on 2025-11-03
红包模块
这里主要 提供一个红包客户端支持
接口：
- 
"""
from ..utils import *
from ..module_registry import Module

@Module("HongBao")
class HongBaoModule(BaseState):
    def __init__(self, namespace, systemName):
        super(HongBaoModule, self).__init__(namespace, systemName)

    def on_enable(self):
        print "启用HongBao"

    def on_disable(self):
        print "禁用HongBao"



