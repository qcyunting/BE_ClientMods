# -*- coding: utf-8 -*-
#
import mod.client.extraClientApi as clientApi

compFactory = clientApi.GetEngineCompFactory()

class CustomEntityClientSystem(clientApi.GetClientSystemCls()):

	def __init__(self, namespace, name):
		super(CustomEntityClientSystem, self).__init__(namespace, name)
		self.mRotatingDict = {} # entityId:boolean
		# 控制松鼠动画切换的变量
		self.queryIsMoving = 'query.mod.is_moving'
		comp = compFactory.CreateQueryVariable(clientApi.GetLevelId())
		result = comp.Register(self.queryIsMoving, 0.0)
		# 控制松鼠渲染控制器变化的变量
		self.queryIsEnchanted = 'query.mod.is_enchanted'
		result = comp.Register(self.queryIsEnchanted, 0.0)

		self.ListenEvent()
	
	def ListenEvent(self):
		self.ListenForEvent('customEntityMod', 'customEntityServerSystem', "ChangeMaterial",
		                    self, self.OnChangeMaterial)

	def OnChangeMaterial(self, args):
		entityId = args['entityId']
		comp = compFactory.CreateEngineType(entityId)
		strType = comp.GetEngineTypeStr()
		if strType == 'netease:squirrel':
			if entityId not in self.mRotatingDict:
				self.mRotatingDict[entityId] = True
				self.ModifySquirrelRender(entityId)
				comp = compFactory.CreateQueryVariable(entityId)
				result = comp.Set(self.queryIsMoving, 1.0)
				result = comp.Set(self.queryIsEnchanted, 1.0)
			else:
				self.ResetSquirrelRender(entityId)
				del self.mRotatingDict[entityId]
				comp = compFactory.CreateQueryVariable(entityId)
				result = comp.Set(self.queryIsMoving, 0.0)
				result = comp.Set(self.queryIsEnchanted, 0.0)
	
	# 修改松鼠（对该类生物都生效）的渲染控制
	def ModifySquirrelRender(self, entityId):
		comp = compFactory.CreateActorRender(entityId)
		actorIdentifier = 'netease:squirrel'
		# 删除默认的渲染控制器
		result = comp.RemoveActorRenderController(actorIdentifier, 'controller.render.squirrel')
		# 增加squirrel.render_controllers.json中定义的但是没有被使用的渲染控制器
		result = comp.AddActorRenderController(actorIdentifier, 'controller.render.squirrel_more')
		# 重建渲染控制器
		result = comp.RebuildActorRender(actorIdentifier)
	
	# 重置松鼠（对该类生物都生效）的渲染控制位默认值
	def ResetSquirrelRender(self, entityId):
		comp = compFactory.CreateActorRender(entityId)
		actorIdentifier = 'netease:squirrel'
		# 增加默认的渲染控制器
		result = comp.AddActorRenderController(actorIdentifier, 'controller.render.squirrel')
		# 删除新增的渲染控制器
		result = comp.RemoveActorRenderController(actorIdentifier, 'controller.render.squirrel_more')
		# 重建渲染控制器
		result = comp.RebuildActorRender(actorIdentifier)
	