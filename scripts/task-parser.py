#!/usr/bin/env python3
"""
定时任务解析器
解析用户自然语言，创建 OpenClaw cron 任务
"""

import re
import subprocess
import sys
from datetime import datetime, timedelta


def parse_time_expression(time_str):
    """
    解析时间表达式
    支持：
    - 明天下午 3 点
    - 1 小时后
    - 30 分钟后
    - 今天下午 5 点
    """
    now = datetime.now()
    
    # 相对时间（优先检查）
    match = re.search(r'(\d+)\s*分钟', time_str)
    if match:
        return f"{match.group(1)}m"
    
    match = re.search(r'(\d+)\s*小时', time_str)
    if match:
        return f"{match.group(1)}h"
    
    # 绝对时间
    time_patterns = [
        # 明天下午 3 点
        (r'明天 (上午 | 下午 | 晚上)?(\d+)(点 | 时)?', 1),
        # 今天下午 5 点
        (r'今天 (上午 | 下午 | 晚上)?(\d+)(点 | 时)?', 0),
        # 下周一
        (r'下周 [一二三四五六日]', 7),
    ]
    
    for pattern, days_add in time_patterns:
        match = re.search(pattern, time_str)
        if match:
            target_date = now + timedelta(days=days_add)
            
            # 提取具体时间
            time_match = re.search(r'(上午 | 下午 | 晚上)?(\d+)(点 | 时)?', time_str)
            if time_match:
                period = time_match.group(1) or "上午"
                hour = int(time_match.group(2))
                
                # 转换 12 小时制到 24 小时制
                if period == "下午" and hour < 12:
                    hour += 12
                elif period == "晚上" and hour < 12:
                    hour += 12
                elif period == "上午" and hour == 12:
                    hour = 0
                
                target_date = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                return target_date.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    # 默认返回 1 小时后
    return "+1h"


def extract_reminder_content(message):
    """提取提醒内容"""
    # 移除时间相关词汇
    content = re.sub(r'(提醒我 | 记得 | 明天 | 今天 | 下午 | 上午 | 晚上 | \d+点)', '', message)
    content = content.strip()
    
    # 添加 emoji
    if "会议" in content or "开会" in content:
        emoji = "📅"
    elif "喝水" in content or "休息" in content:
        emoji = "💧"
    elif "报告" in content or "提交" in content:
        emoji = "✅"
    else:
        emoji = "⏰"
    
    return f"{emoji} {content}"


def generate_task_name(content, user="用户"):
    """生成任务名称"""
    # 简化内容
    short_content = re.sub(r'[^\w\u4e00-\u9fff]', '', content)[:20]
    date_str = datetime.now().strftime("%Y%m%d")
    
    return f"{short_content}-{user}-{date_str}"


def create_cron_task(time_expr, content, user="用户", test=False):
    """创建 cron 任务"""
    at_time = parse_time_expression(time_expr)
    task_name = generate_task_name(content, user)
    reminder_msg = extract_reminder_content(content)
    
    # 构建命令
    cmd = [
        "openclaw", "cron", "add",
        "--name", task_name,
        "--at", at_time,
        "--session", "isolated",
        "--message", reminder_msg,
        "--announce",
        "--channel", "dingtalk",
        "--delete-after-run"
    ]
    
    if test:
        cmd.append("--json")
    
    print(f"创建任务：{task_name}")
    print(f"执行时间：{at_time}")
    print(f"提醒内容：{reminder_msg}")
    print()
    
    # 执行命令
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 任务创建成功！")
        if test:
            print(result.stdout)
        return True
    else:
        print(f"❌ 任务创建失败：{result.stderr}")
        return False


def main():
    """命令行界面"""
    if len(sys.argv) < 3:
        print("用法：task-parser.py <时间> <内容> [用户]")
        print("\n示例:")
        print("  task-parser.py '明天下午 3 点' '开会准备材料' '吴震宇'")
        print("  task-parser.py '1 小时后' '喝水休息'")
        sys.exit(1)
    
    time_expr = sys.argv[1]
    content = sys.argv[2]
    user = sys.argv[3] if len(sys.argv) > 3 else "用户"
    
    create_cron_task(time_expr, content, user, test=True)


if __name__ == "__main__":
    main()
