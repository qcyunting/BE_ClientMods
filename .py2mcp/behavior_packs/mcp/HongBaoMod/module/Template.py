# coding=utf-8
"""
Created on 2025-11-03
模板模块
这里主要 提供一个模板模块
接口：
- 
"""
from ..utils import *
from ..module_registry import Module

@Module("Template")
class TemplateModule(BaseState):
    def __init__(self, namespace, systemName):
        super(TemplateModule, self).__init__(namespace, systemName)

    def on_enable(self):
        print "启用Template"

    def on_disable(self):
        print "禁用Template"

