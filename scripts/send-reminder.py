#!/usr/bin/env python3
"""
定时提醒发送器
在指定时间发送提醒到 DingTalk
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path
import subprocess

WORKSPACE = Path("/root/.openclaw/workspace")
TODOS_FILE = WORKSPACE / "memory" / "todos.json"
DINGTALK_CONFIG = WORKSPACE.parent / "openclaw.json"


def get_dingtalk_webhook():
    """获取 DingTalk webhook URL（从配置或环境变量）"""
    # 简单方案：使用 openclaw message 命令
    return None


def send_dingtalk_message(message):
    """发送消息到 DingTalk"""
    try:
        # 使用 openclaw message 命令
        cmd = [
            "openclaw",
            "message",
            "send",
            "--channel", "dingtalk",
            "--target", "cidLVGAn3OiNoE0RfQCA5GE4g==",
            "--message", message
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✓ 消息已发送：{message[:50]}...")
            return True
        else:
            print(f"✗ 发送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 异常：{e}")
        return False


def check_and_send_reminders():
    """检查待办并发送提醒"""
    if not TODOS_FILE.exists():
        print("暂无待办文件")
        return
    
    with open(TODOS_FILE, encoding='utf-8') as f:
        data = json.load(f)
    
    now = datetime.now()
    reminders_sent = []
    
    for todo in data.get("todos", []):
        if todo.get("status") != "pending":
            continue
        
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
        
        # 在提醒时间窗口内（-5 分钟到 +30 分钟）
        if -300 <= time_diff <= 1800:
            emoji = {
                "health_reminder": "💧",
                "meeting": "📅",
                "task": "✅",
                "deadline": "⏰",
                "general": "📌"
            }.get(todo.get("type", "general"), "📌")
            
            message = f"{emoji} 提醒：{todo['title']}"
            if todo.get("notes"):
                message += f"\n📝 {todo['notes']}"
            message += f"\n⏰ 计划时间：{reminder_time.strftime('%H:%M')}"
            
            print(f"发送提醒：{message}")
            
            if send_dingtalk_message(message):
                reminders_sent.append(todo["id"])
                # 标记为已提醒（但不完成）
                todo["last_reminded"] = now.isoformat()
    
    # 保存更新
    if reminders_sent:
        with open(TODOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ 已发送 {len(reminders_sent)} 个提醒")
    else:
        print("\n暂无需要提醒的待办")
    
    return len(reminders_sent)


def main():
    """主函数"""
    print(f"=== 待办提醒检查 ===")
    print(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    count = check_and_send_reminders()
    
    print()
    print(f"=== 检查完成 ===")
    print(f"发送提醒数：{count}")


if __name__ == "__main__":
    main()
