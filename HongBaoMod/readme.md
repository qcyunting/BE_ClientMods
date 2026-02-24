# {Mod名称}

{一句话简介}

## 介绍

{详细描述mod的功能、特点和使用场景}

## 实现逻辑

### 架构概述

本mod采用**有限状态机(FSM)**模式设计，主要包含以下核心组件：

- **ClientSystem**: 客户端系统入口，负责初始化和事件分发
- **FSM**: 有限状态机，管理状态切换和生命周期
- **BaseState**: 状态基类，提供状态的基础功能
- **具体状态**: 继承BaseState的具体业务状态实现

### 核心流程

```
客户端启动 → LoadClientAddonScriptsAfter → 注册FSM状态 → 监听事件
```

### 事件系统

使用装饰器 `@Listen()` 监听Minecraft游戏事件：

```python
from utils import Listen

class YourState(BaseState):
    @Listen("Minecraft", "Engine")  # 监听Minecraft引擎事件
    def on_event(self, args):
        pass
    
    @Listen("client")  # 监听客户端自定义事件
    def on_client_event(self, args):
        pass
```

## 提供的接口

### 客户端API组件

本mod通过 `clientApi.GetEngineCompFactory()` 提供以下组件：

| 组件 | 获取方式 | 用途 |
|------|----------|------|
| Game | `CF.CreateGame(levelId)` | 游戏级别操作 |
| Pos | `CF.CreatePos(playerId)` | 获取/设置玩家位置 |
| Rot | `CF.CreateRot(playerId)` | 获取/设置玩家旋转 |
| TextBoard | `CF.CreateTextBoard(playerId)` | 文本显示 |
| Music | `CF.CreateCustomAudio(levelId)` | 音频播放 |
| Name | `CF.CreateName(playerId)` | 玩家名称操作 |
| Item | `CF.CreateItem(playerId)` | 物品操作 |

### 全局变量

| 变量 | 说明 |
|------|------|
| `LevelId` | 当前等级ID |
| `PlayerId` | 本地玩家ID |
| `PlayerName` | 本地玩家名称 |
| `modName` | mod名称(在config.py中配置) |
| `systemName` | 系统名称(在config.py中配置) |
| `version` | mod版本号 |

### 状态管理接口

```python
# 在FSM中切换状态
self.fsm.update_state(StateMode.on)  # 切换到开启状态

# 获取当前状态
current_state = self.fsm.get_state()

# 添加子状态
self.add_sub_state(SubStateClass)

# 切换子状态
self.start_sub_state("sub_state_name")
```

### 事件监听接口

```python
# 监听事件
self.ListenForEvent(namespace, system, event, self, callback)

# 取消监听
self.UnListenForEvent(namespace, system, event, self, callback)

# 取消所有监听
self.UnListenAllEvents()
```

## 注意事项

1. **状态切换**: 状态切换时会自动调用 `_on_disable()` 清理旧状态的监听器，确保无事件残留
2. **弱引用**: 系统使用弱引用避免循环引用导致的内存泄漏
3. **子状态**: 子状态继承父状态的FSM引用，可通过 `parent_state` 访问父状态
4. **事件优先级**: 监听事件时可设置优先级(1-5)，数字越小优先级越高
5. **线程安全**: 客户端mod在主线程执行，注意避免阻塞操作
6. **资源清理**: 在 `on_disable` 中清理创建的资源(如定时器、自定义UI等)

## 使用方法

### 1. 修改配置

编辑 `behavior_packs/LobbyModBehavior/LobbyMod/config.py`:

```python
modName = "YourModName"      # 修改为你的mod名称
version = "1.0.0"            # 修改版本号
systemName = "your_system"   # 修改系统名称
```

### 2. 定义状态

在 `main.py` 或新建状态文件中创建状态类:

```python
from utils import BaseState, Listen

class YourState(BaseState):
    state_name = "your_state"  # 必须定义
    
    def on_enable(self):
        # 状态启用时执行的逻辑
        pass
    
    def on_disable(self):
        # 状态禁用时执行的逻辑
        pass
    
    @Listen("Minecraft", "Engine")
    def on_player_join(self, args):
        # 监听玩家加入事件
        pass
```

### 3. 注册状态

在 `StateBase.py` 的 `LoadClientAddonScriptsAfter` 方法中注册状态:

```python
def LoadClientAddonScriptsAfter(self, args):
    self.fsm.add_state(YourState)
    self.fsm.update_state("your_state")
```

### 4. 构建与安装

1. 打包behavior_packs和resource_packs
2. 将打包文件放入游戏的 `com.mojang/behavior_packs` 目录
3. 在游戏设置中启用该行为包

## 目录结构

```
LobbyMod/
├── behavior_packs/
│   └── LobbyModBehavior/
│       └── LobbyMod/
│           ├── config.py          # mod配置
│           ├── main.py            # 主状态实现
│           ├── modMain.py         # mod入口
│           ├── StateBase.py       # 状态基类和FSM
│           ├── utils.py           # 工具函数
│           └── ui/                # UI相关
│               ├── __init__.py
│               ├── Template.py
│               └── utils.py
├── resource_packs/
│   └── LobbyModResource/
│       └── manifest.json
├── worlds/
│   └── level/
│       ├── world_behavior_packs.json
│       └── world_resource_packs.json
└── readme.md
```

## 常见问题

**Q: 如何调试mod?**
A: 使用 `logger.info()` 或 `print()` 输出日志，检查游戏日志或控制台输出。

**Q: 如何添加新的游戏事件监听?**
A: 在状态类中使用 `@Listen` 装饰器，参考Minecraft Bedrock API文档。

**Q: mod无法加载怎么办?**
A: 检查manifest.json配置是否正确，确保行为包已正确添加到世界配置中。

## 更新日志

### 2026-02-19 13:28:57
- 基于ExampleMod（状态机）模板创建包: HongBaoMod

### 2026-02-18 16:19:39
- 基于HongBaoMod（状态机）模板创建包: LobbyMod

### v0.0.1
- 初始版本
- 基础状态机框架

---

{作者名称} © {年份}
