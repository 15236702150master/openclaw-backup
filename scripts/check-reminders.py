#!/usr/bin/env python3
"""
待办提醒检查脚本
检查 todos.json 中的待办事项，返回需要提醒的内容
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
TODOS_FILE = WORKSPACE / "memory" / "todos.json"

def check_reminders():
    """检查待办并返回提醒列表"""
    if not TODOS_FILE.exists():
        return []
    
    with open(TODOS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    
    now = datetime.now()
    reminders = []
    
    for todo in data.get("todos", []):
        # 解析提醒时间
        reminder_time_str = todo.get("reminderTime", "")
        if not reminder_time_str:
            continue
        
        # 处理时区
        reminder_time_str = reminder_time_str.replace("+08:00", "").replace("+00:00", "")
        try:
            reminder_time = datetime.fromisoformat(reminder_time_str)
        except:
            continue
        
        # 检查是否到提醒时间（前后 5 分钟窗口）
        time_diff = (now - reminder_time).total_seconds()
        if 0 <= time_diff <= 300 and todo.get("status") == "pending":
            reminders.append({
                "id": todo.get("id"),
                "title": todo.get("title", "待办事项"),
                "notes": todo.get("notes", ""),
                "scheduledTime": todo.get("scheduledTime", ""),
                "type": todo.get("type", "general")
            })
    
    return reminders

def format_reminder_message(reminders):
    """格式化提醒消息"""
    if not reminders:
        return None
    
    messages = []
    for r in reminders:
        emoji = {
            "health_reminder": "💧",
            "meeting": "📅",
            "task": "✅",
            "deadline": "⏰",
            "general": "📌"
        }.get(r.get("type", "general"), "📌")
        
        msg = f"{emoji} {r['title']}"
        if r.get("notes"):
            msg += f" - {r['notes']}"
        
        messages.append(msg)
    
    return "\n".join(messages)

if __name__ == "__main__":
    reminders = check_reminders()
    
    if reminders:
        message = format_reminder_message(reminders)
        print(message)
        # 输出 JSON 供 cron 任务使用
        print("\n---JSON---")
        print(json.dumps({"reminders": reminders}, ensure_ascii=False, indent=2))
    else:
        print("暂无待办提醒")
