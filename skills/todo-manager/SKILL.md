---
name: todo-manager
description: Manage todos and reminders with natural language. Set reminders for specific times, view pending tasks, and mark as complete. All reminders are user-initiated, not scheduled.
---

# Todo Manager

待办和提醒管理系统，采用**按需记录、智能提醒**的策略。

## 核心原则

### ✅ 做什么
- 用户随时说"提醒我 X" → 立即设置
- 基于事件触发（会议前 10 分钟、任务截止前 1 小时）
- 提醒时间由用户指定或 AI 建议

### ❌ 不做什么
- 不每天早上定时检查待办
- 不自动猜测提醒时间
- 不批量推送待办列表

---

## 使用方法

### 设置提醒

**简单提醒：**
```
用户：提醒我下午 3 点开会
AI：好的，已设置今天 15:00 的提醒（提前 10 分钟通知）

用户：明天记得交报告
AI：好的，明天几点截止？
用户：下午 5 点
AI：已设置明天 16:00 提醒（提前 1 小时）
```

**复杂提醒：**
```
用户：下周一有面试
AI：好的，需要什么时候提醒？
用户：周日晚上提醒我准备
AI：已设置下周日 20:00 的提醒
```

**周期性提醒：**
```
用户：每周五下午写周报
AI：好的，已设置每周五 15:00 的周期性提醒
```

### 查看待办

```
用户：我有什么待办？
→ 列出所有未完成的待办

用户：今天有什么安排？
→ 列出今天的待办和提醒

用户：这周的待办列表
→ 列出本周所有待办
```

### 完成/取消

```
用户：报告已经交了
→ 标记为完成

用户：取消下午的会议提醒
→ 删除该提醒

用户：会议改到明天了
→ 更新时间并确认
```

---

## 提醒策略

### 默认提前量

| 类型 | 默认提前量 | 可调整 |
|------|------------|--------|
| 会议/约会 | 10 分钟 | ✅ |
| 任务截止 | 1 小时 | ✅ |
| 生日/纪念日 | 1 天 | ✅ |
| 周期性事件 | 按需 | ✅ |

### 提醒方式

**立即通知（心跳检查时）：**
```
⏰ 提醒：下午 3 点开会
📍 地点：会议室 A
📝 备注：带笔记本电脑
```

**待办列表（用户询问时）：**
```
📋 今日待办 (3)
├─ 09:00 团队晨会
├─ 15:00 项目汇报
└─ 17:00 提交周报
```

---

## 数据存储

### 待办文件：memory/todos.json

```json
{
  "todos": [
    {
      "id": "todo-001",
      "title": "项目汇报",
      "scheduledTime": "2026-03-05T15:00:00+08:00",
      "reminderTime": "2026-03-05T14:50:00+08:00",
      "status": "pending",
      "createdAt": "2026-03-04T09:30:00+08:00",
      "notes": "带笔记本电脑"
    }
  ],
  "completed": [
    {
      "id": "todo-000",
      "title": "提交简历",
      "completedAt": "2026-03-04T10:00:00+08:00"
    }
  ]
}
```

### 记忆记录

重要的待办完成后，询问用户：
```
✅ 任务完成：项目汇报
需要记录到 MEMORY.md 吗？
- 记录为："2026-03-05：完成项目汇报"
- 或跳过（临时任务）
```

---

## Token 节省优化

### 1. 按需加载
- 用户不问待办 → 不加载 todos.json
- 用户问"今天有什么" → 只加载今天的待办
- 用户问"所有待办" → 加载全部

### 2. 精简存储
```json
// 优化前（冗余）
{
  "title": "项目汇报",
  "description": "今天下午 3 点在会议室 A 进行项目汇报，需要带笔记本电脑和投影仪",
  "time": "2026-03-05T15:00:00+08:00"
}

// 优化后（精简）
{
  "title": "项目汇报",
  "time": "2026-03-05T15:00:00+08:00",
  "notes": "会议室 A，带电脑"
}
```

### 3. 自动清理
- 完成的待办 → 移到 completed 数组
- 超过 30 天的已完成 → 删除
- 过期的未完成 → 标记为"已过期"

### 4. 对话压缩
```
长对话设置提醒后：
[提醒设置] 下午 3 点开会 → 已设置 14:50 提醒
= 1 行，~40 tokens

而非保存完整对话历史
= 10 行，~500 tokens
```

---

## 实现示例

### Python 脚本：todo-manager.py

```python
#!/usr/bin/env python3
"""待办和提醒管理器"""

import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
TODOS_FILE = WORKSPACE / "memory" / "todos.json"

def load_todos():
    if not TODOS_FILE.exists():
        return {"todos": [], "completed": []}
    with open(TODOS_FILE) as f:
        return json.load(f)

def save_todos(data):
    TODOS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TODOS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_todo(title, scheduled_time, reminder_time=None, notes=""):
    """添加待办"""
    data = load_todos()
    
    if reminder_time is None:
        # 默认提前 10 分钟
        reminder_time = scheduled_time - timedelta(minutes=10)
    
    todo = {
        "id": f"todo-{len(data['todos']) + 1:03d}",
        "title": title,
        "scheduledTime": scheduled_time.isoformat(),
        "reminderTime": reminder_time.isoformat(),
        "status": "pending",
        "createdAt": datetime.now().isoformat(),
        "notes": notes
    }
    
    data["todos"].append(todo)
    save_todos(data)
    return todo

def list_todos(date=None):
    """列出待办"""
    data = load_todos()
    
    if date:
        # 筛选指定日期的待办
        filtered = []
        for todo in data["todos"]:
            todo_date = todo["scheduledTime"][:10]
            if todo_date == date:
                filtered.append(todo)
        return filtered
    
    return data["todos"]

def complete_todo(todo_id):
    """标记为完成"""
    data = load_todos()
    
    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            todo["status"] = "completed"
            todo["completedAt"] = datetime.now().isoformat()
            data["completed"].append(todo)
            data["todos"].pop(i)
            break
    
    save_todos(data)

def delete_todo(todo_id):
    """删除待办"""
    data = load_todos()
    
    data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
    save_todos(data)

def cleanup_old_todos(days=30):
    """清理旧待办"""
    data = load_todos()
    
    cutoff = datetime.now() - timedelta(days=days)
    data["completed"] = [
        t for t in data["completed"]
        if datetime.fromisoformat(t["completedAt"]) > cutoff
    ]
    
    save_todos(data)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：todo-manager.py <command> [args]")
        print("命令：add, list, complete, delete, cleanup")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        title = sys.argv[2]
        time_str = sys.argv[3]
        time = datetime.fromisoformat(time_str)
        todo = add_todo(title, time)
        print(f"已添加待办：{todo['title']} ({todo['id']})")
    
    elif cmd == "list":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        todos = list_todos(date)
        for todo in todos:
            print(f"{todo['id']}: {todo['title']} @ {todo['scheduledTime']}")
    
    elif cmd == "complete":
        todo_id = sys.argv[2]
        complete_todo(todo_id)
        print(f"已完成：{todo_id}")
    
    elif cmd == "delete":
        todo_id = sys.argv[2]
        delete_todo(todo_id)
        print(f"已删除：{todo_id}")
    
    elif cmd == "cleanup":
        cleanup_old_todos()
        print("已清理旧待办")
```

---

## 与记忆系统的集成

### 完成后记录
```
任务完成 → 询问"需要记录吗？"
   ├─ 是 → 写入 MEMORY.md
   └─ 否 → 仅标记完成，不记录
```

### 重要事件
```
重要事件（面试、汇报等）完成后：
自动建议："这是重要事件，需要记录到 MEMORY.md 吗？"
```

---

## 相关技能

- **memory-manager**: 记忆管理和清理
- **calendar-integration**: 日历集成（可选）

---

**设计原则：** 按需记录，智能提醒，不干扰用户
