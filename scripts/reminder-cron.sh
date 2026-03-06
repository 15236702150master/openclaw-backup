#!/bin/bash
# 每分钟检查待办并发送提醒

cd /root/.openclaw/workspace

# 检查待办
python3 << 'PYTHON'
import json
from datetime import datetime
from pathlib import Path

TODOS_FILE = Path("memory/todos.json")

if not TODOS_FILE.exists():
    exit(0)

with open(TODOS_FILE, encoding='utf-8') as f:
    data = json.load(f)

now = datetime.now()
reminders = []

for todo in data.get("todos", []):
    if todo.get("status") != "pending":
        continue
    
    reminder_time_str = todo.get("reminderTime", "").replace("+08:00", "").replace("+00:00", "")
    try:
        reminder_time = datetime.fromisoformat(reminder_time_str)
    except:
        continue
    
    # 检查是否在提醒时间窗口内（前后 5 分钟）
    time_diff = (now - reminder_time).total_seconds()
    
    if 0 <= time_diff <= 300:  # 0-5 分钟内
        emoji = {"health_reminder": "💧", "meeting": "📅", "task": "✅"}.get(todo.get("type", "general"), "📌")
        msg = f"{emoji} 提醒：{todo['title']}"
        if todo.get("notes"):
            msg += f"\n📝 {todo['notes']}"
        reminders.append(msg)
        
        # 标记为已提醒
        todo["last_reminded"] = now.isoformat()

if reminders:
    with open(TODOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 打印提醒（cron 会捕获输出）
    for msg in reminders:
        print(f"REMINDER: {msg}")
PYTHON
