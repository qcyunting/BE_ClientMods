# -*- coding: utf-8 -*-
#
from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi

@Mod.Binding(name = 'customEntityMod', version = "1.0")
class MyMod(object):

	def __init__(self):
		pass

	@Mod.InitClient()
	def initClient(self):
		testClient = clientApi.RegisterSystem('customEntityMod', 'customEntityClientSystem', "customEntityModScripts.customEntityClientSystem.CustomEntityClientSystem")