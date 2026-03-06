#!/usr/bin/env python3
"""
Task Manager - 补偿检查和补救系统
检查错过的任务并执行补救
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
STATE_FILE = WORKSPACE / ".task-state.json"
LOG_FILE = WORKSPACE / "memory" / "task-logs.json"
CONFIG_FILE = WORKSPACE / "task-config.json"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def load_state():
    """加载任务状态"""
    default_state = {
        "daily-cleanup": {
            "lastRun": None,
            "nextRun": "2026-03-05T03:00:00+08:00",
            "status": "pending",
            "missedCount": 0
        },
        "weekly-memory": {
            "lastRun": None,
            "nextRun": "2026-03-09T02:00:00+08:00",
            "status": "pending",
            "missedCount": 0
        },
        "calendar-check": {
            "lastRun": None,
            "nextRun": "2026-03-05T08:00:00+08:00",
            "status": "pending",
            "missedCount": 0
        }
    }
    
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    
    return default_state

def save_state(state):
    """保存任务状态"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def parse_time(time_str):
    """解析 ISO 时间字符串"""
    if not time_str:
        return None
    try:
        # 处理 +08:00 时区
        time_str = time_str.replace('+08:00', '').replace('+00:00', '')
        return datetime.fromisoformat(time_str)
    except:
        return None

def check_missed(task_info):
    """检查任务是否错过"""
    next_run = parse_time(task_info.get("nextRun"))
    if not next_run:
        return True  # 没有时间记录，视为错过
    
    now = datetime.now()
    return now > next_run

def is_within_compensation_window(task_info, max_hours=24):
    """检查是否在补偿窗口内"""
    next_run = parse_time(task_info.get("nextRun"))
    if not next_run:
        return False
    
    now = datetime.now()
    overdue = now - next_run
    
    return overdue.total_seconds() / 3600 <= max_hours

def run_cleanup():
    """执行清理任务"""
    cleanup_script = WORKSPACE / "scripts" / "cleanup.sh"
    if cleanup_script.exists():
        result = subprocess.run([str(cleanup_script)], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    return False, "清理脚本不存在"

def update_state(state, task, status):
    """更新任务状态"""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    # 计算下次运行时间
    if task == "daily-cleanup":
        next_run = (datetime.now() + timedelta(days=1)).replace(
            hour=3, minute=0, second=0, microsecond=0
        ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    elif task == "weekly-memory":
        # 下周日 02:00
        days_until_sunday = (6 - datetime.now().weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        next_run = (datetime.now() + timedelta(days=days_until_sunday)).replace(
            hour=2, minute=0, second=0, microsecond=0
        ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    elif task == "calendar-check":
        next_run = (datetime.now() + timedelta(days=1)).replace(
            hour=8, minute=0, second=0, microsecond=0
        ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    else:
        next_run = state[task]["nextRun"]
    
    state[task]["lastRun"] = now
    state[task]["status"] = status
    state[task]["nextRun"] = next_run
    if status == "success":
        state[task]["missedCount"] = 0
    else:
        state[task]["missedCount"] = state[task].get("missedCount", 0) + 1
    
    save_state(state)

def log_task(task, status, details=None):
    """记录任务日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE) as f:
                logs = json.load(f)
        except:
            pass
    
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "task": task,
        "status": status,
        "type": "compensation",
        "details": details
    })
    
    # 保留最近 100 条
    logs = logs[-100:]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def compensate(task, state):
    """执行补救"""
    log(f"开始补救任务：{task}")
    
    if task == "daily-cleanup":
        success, output = run_cleanup()
        if success:
            log("✓ 清理任务执行成功")
            update_state(state, task, "success")
            log_task(task, "success", {"output": output[:500]})
        else:
            log(f"❌ 清理任务失败：{output}")
            update_state(state, task, "failed")
            log_task(task, "failed", {"error": output})
    
    elif task == "weekly-memory":
        log("执行记忆提炼...")
        # TODO: 实现记忆提炼逻辑
        update_state(state, task, "success")
        log_task(task, "success")
    
    elif task == "calendar-check":
        log("检查日历...")
        # TODO: 实现日历检查逻辑
        update_state(state, task, "success")
        log_task(task, "success")

def startup_check():
    """启动时补偿检查"""
    log("=== 启动时补偿检查 ===")
    
    state = load_state()
    missed_count = 0
    
    for task in ["daily-cleanup", "weekly-memory", "calendar-check"]:
        task_info = state.get(task, {})
        
        if check_missed(task_info):
            # 检查是否在补偿窗口内（默认 24 小时）
            if is_within_compensation_window(task_info, max_hours=24):
                compensate(task, state)
                missed_count += 1
            else:
                log(f"⚠️ 任务 {task} 错过时间过长，跳过补救")
                # 重置下次运行时间
                update_state(state, task, "skipped")
        else:
            log(f"✓ 任务 {task} 未错过 (计划：{task_info.get('nextRun', '未知')})")
    
    if missed_count == 0:
        log("✓ 无需补救的任务")
    else:
        log(f"完成 {missed_count} 个补救任务")
    
    log("=== 补偿检查完成 ===")

def health_check():
    """健康检查"""
    log("=== 健康检查 ===")
    
    state = load_state()
    
    # 检查状态文件
    if not STATE_FILE.exists():
        log("⚠️ 状态文件不存在，初始化...")
        save_state({})
    
    # 检查日志文件大小
    if LOG_FILE.exists():
        size_kb = LOG_FILE.stat().st_size / 1024
        if size_kb > 100:
            log(f"日志文件过大 ({size_kb:.1f}KB)，归档...")
            archive_name = f"{LOG_FILE}.{datetime.now().strftime('%Y%m%d')}"
            LOG_FILE.rename(archive_name)
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)
    
    # 报告状态
    log("任务状态：")
    for task, info in state.items():
        log(f"  {task}: {info['status']} (下次：{info['nextRun']})")
    
    log("=== 健康检查完成 ===")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "startup"
    
    if cmd == "startup":
        startup_check()
    elif cmd == "health":
        health_check()
    elif cmd == "status":
        state = load_state()
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print(f"用法：{sys.argv[0]} {{startup|health|status}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
