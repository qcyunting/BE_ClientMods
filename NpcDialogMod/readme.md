# NpcDialog 模块说明

## 1. 功能概述

`NpcDialog` 用于在客户端显示 NPC 对话 UI，并根据服务端下发的数据展示：

- NPC 名称
- NPC 头像
- 对话文本
- 操作按钮
- 对话步骤控制

---

## 2. 相关文件

- `NpcDialogMod/BehaviorPacks/NpcDialogMod/module/NpcDialog.py`
  - 模块入口
  - 接收服务端事件
  - 打开对话界面
  - 处理关闭、翻页、领奖等请求

- `NpcDialogMod/BehaviorPacks/NpcDialogMod/ui/NpcDialog.py`
  - 对话界面 UI
  - 负责渲染标题、正文、头像和按钮
  - 负责按钮点击回调

---

## 3. 模块入口

### `NpcDialogModule.on_enable()`

启用模块时会：

- 注册服务端事件监听 `OpenDialogue`
- 监听客户端事件：
  - `UiInitFinished`
  - `OnKeyPressInGame`
- 注册 UI：
  - namespace: `modName`
  - screen id: `npcdialog`
  - ui class: `NpcDialog.Main`

---

## 4. 打开对话

### `OpenDialogue(args)`

服务端发送 `OpenDialogue` 后，客户端会读取以下字段：

- `dialogue_id`：对话唯一标识
- `npc_name`：NPC 名称
- `npc_icon`：NPC 头像资源名
- `text`：对话内容
- `step_index`：当前步骤
- `buttons`：按钮列表

### 对话打开条件

当以下字段都存在时才会打开：

- `dialogue_id`
- `npc_name`
- `npc_icon`
- `text`
- `buttons`

并且 `step_index >= 0`

---

## 5. UI 渲染逻辑

### `Main.Create()`

UI 创建完成后：

- 标记 `CreateStatus = True`
- 执行之前缓存的 `tasks`

### `Main.SetData(...)`

如果 UI 还没创建完成：

- 数据会先进入 `tasks` 队列
- 等 `Create()` 后再执行

如果 UI 已创建：

- 更新标题
- 更新正文
- 更新 NPC 图标
- 隐藏全部按钮
- 按 `buttons` 内容显示前 5 个按钮
- 设置按钮图标和文字

---

## 6. 按钮类型

当前支持的按钮类型：

- `next`：下一页
- `close`：关闭
- `finish`：完成
- `claim_reward`：领取奖励

### 按钮回调

按钮点击后会向服务端发送：

- `RequestNextPage`
- `RequestClose`
- `RequestFinish`
- `RequestClaimReward`

---

## 7. 关闭方式

支持两种关闭方式：

1. 点击 `close` 按钮
2. 按 `Esc` 键

关闭时会：

- 发送 `RequestClose`
- 清空 `self.ui_npcdialog`
- 调用 `clientApi.PopScreen()`

---

## 8. NPC 图标规则

### `npc_icon_default_fun(icon)`

图标处理规则：

- 如果 `icon` 包含 `/`，视为路径
- 如果路径以 `/` 开头，会去掉首字符 `/`
- 否则会检查是否在默认图标列表中
- 不合法时回退为 `STEVE`
- 最终转换为：
  - `textures/npc/<icon.lower()>`

---

## 9. 注意事项

- `SetData()` 在 UI 未创建前会缓存任务，避免空界面调用
- 按钮最多显示 5 个
- 当前实现中部分位置存在重复调用或调试输出，正式环境建议清理
- 如果同一 `dialogue_id` 和 `step_index` 重复到达，UI 会忽略重复刷新

---

## 10. 接口摘要

### 客户端接收服务端事件

- `OpenDialogue`

### 客户端发送给服务端

- `RequestNextPage`
- `RequestClose`
- `RequestFinish`
- `RequestClaimReward`

---

## 11. 使用示例

服务端下发示例数据：

```json
{
  "dialogue_id": "dlg_001",
  "npc_name": "村民",
  "npc_icon": "STEVE",
  "text": "你好，冒险者。",
  "step_index": 0,
  "buttons": ["next", "close"]
}
```

## 12. 版本说明

该文档对应当前 `NpcDialog` 实现逻辑，后续如果按钮类型、图标规则或事件名变更，需要同步更新本文档。