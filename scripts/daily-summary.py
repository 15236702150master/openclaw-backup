#!/usr/bin/env python3
"""
每日摘要生成器
扫描今日对话，生成带序号的摘要列表
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SUMMARY_LOG = WORKSPACE / "memory" / "daily-summaries.json"

# 琐碎对话模式（跳过）
TRIVIAL_PATTERNS = [
    r"早.?[上中晚]?",
    r"谢谢 | 感谢 | thx",
    r"好的 | 好哒 | ok|好",
    r"明白 | 了解 | 懂了",
    r"哈哈 | 嘿嘿 | 嘻嘻",
    r"天气.*[?？]",
    r"几点了 | 什么时间",
    r"在吗 | 在嘛",
    r"嗯嗯 | 哦哦 | 啊啊",
]

# 重要对话模式（记录）
SIGNIFICANT_PATTERNS = [
    r"记住 | 记录 | 记下来",
    r"安装 | 卸载 | 删除 | 移除",
    r"配置 | 设置 | 修改 | 变更",
    r"决定 | 采用 | 方案 | 计划",
    r"项目 | 任务 | 工作 | deadline",
    r"买了 | 购买了 | 新.*[键盘鼠标屏幕]",
    r"喜欢 | 偏好 | 习惯",
    r"提醒我 | 待办 | 待办事项",
    r"技能 | 插件 | 扩展",
    r"重要 | 关键 | 必须",
]

# 分类关键词
CATEGORIES = {
    "技能配置": ["安装", "卸载", "技能", "插件", "扩展"],
    "系统配置": ["配置", "设置", "修改", "变更", "环境"],
    "待办/项目": ["项目", "任务", "工作", "截止", "deadline", "提醒"],
    "个人信息": ["买了", "喜欢", "偏好", "习惯", "新"],
    "重要决策": ["决定", "采用", "方案", "计划", "重要", "关键"],
}


def load_memory():
    """加载 MEMORY.md 内容"""
    if not MEMORY_FILE.exists():
        return ""
    with open(MEMORY_FILE, encoding="utf-8") as f:
        return f.read()


def is_trivial(message):
    """判断是否是琐碎对话"""
    for pattern in TRIVIAL_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def has_significance(message):
    """判断是否有记录价值"""
    for pattern in SIGNIFICANT_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def suggest_category(message):
    """建议分类"""
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in message:
                return category
    return "其他"


def is_already_recorded(item, memory_content):
    """检查是否已存在于 MEMORY.md"""
    if not memory_content:
        return False
    
    # 精确匹配
    if item in memory_content:
        return True
    
    # 关键词匹配（简化版）
    keywords = re.findall(r"[\u4e00-\u9fa5]{2,}", item)
    if not keywords:
        return False
    
    match_count = sum(1 for k in keywords if k in memory_content)
    if match_count >= len(keywords) * 0.6:
        return True
    
    return False


def extract_key_items(conversations):
    """从对话中提取关键事项"""
    items = []
    
    for conv in conversations:
        msg = conv.get("content", "")
        timestamp = conv.get("timestamp", "")
        sender = conv.get("sender", "unknown")
        
        # 跳过琐碎对话
        if is_trivial(msg):
            continue
        
        # 检查是否有记录价值
        if has_significance(msg):
            # 提取关键信息（简化：取前 100 字）
            key_info = msg[:100] + "..." if len(msg) > 100 else msg
            
            items.append({
                "content": key_info,
                "timestamp": timestamp,
                "sender": sender,
                "category": suggest_category(msg),
            })
    
    return items


def deduplicate_items(items):
    """去重相似事项"""
    unique = []
    seen = set()
    
    for item in items:
        # 简化去重：基于内容哈希
        key = item["content"][:50]
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    return unique


def generate_summary(items, memory_content):
    """生成摘要列表"""
    new_items = []
    recorded_items = []
    
    for i, item in enumerate(items, 1):
        item["id"] = i
        
        if is_already_recorded(item["content"], memory_content):
            recorded_items.append(item)
        else:
            new_items.append(item)
    
    return new_items, recorded_items


def format_summary(new_items, recorded_items, date):
    """格式化摘要输出"""
    output = []
    output.append(f"📅 每日摘要 - {date}")
    output.append("")
    output.append("━" * 32)
    
    # 新增事项
    if new_items:
        output.append("【新增事项】需要确认是否记录")
        output.append("")
        for item in new_items:
            output.append(f"⑳⑱⑯⑭⑫⑩⑧⑥④②①③⑤⑦⑨⑪⑬⑮⑰⑲"[item["id"]-1] if item["id"] <= 20 else f"{item['id']})")
            output.append(f"   {item['content']} [{item['category']}]")
        output.append("")
    else:
        output.append("【新增事项】无新事项")
        output.append("")
    
    output.append("━" * 32)
    
    # 已记录事项
    if recorded_items:
        output.append("【已记录事项】已存在于 MEMORY.md")
        output.append("")
        for item in recorded_items:
            output.append(f"✓ ⑳⑱⑯⑭⑫⑩⑧⑥④②①③⑤⑦⑨⑪⑬⑮⑰⑲"[item["id"]-1] if item["id"] <= 20 else f"{item['id']})")
            output.append(f"   {item['content']} [{item['category']}]")
        output.append("")
    else:
        output.append("【已记录事项】无")
        output.append("")
    
    output.append("━" * 32)
    output.append("")
    output.append("请回复需要记录的序号，例如：")
    output.append('"记录 ①②③" 或 "全部记录" 或 "都不记录"')
    
    return "\n".join(output)


def parse_user_response(response, new_items):
    """解析用户回复"""
    response = response.strip()
    
    # 全部记录
    if "全部" in response or "all" in response.lower():
        return [item["id"] for item in new_items]
    
    # 都不记录
    if "都不" in response or "跳过" in response or "no" in response.lower():
        return []
    
    # 提取序号
    selected = []
    
    # 匹配中文数字序号
    chinese_nums = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5,
                    "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10}
    
    for char in response:
        if char in chinese_nums:
            selected.append(chinese_nums[char])
    
    # 匹配阿拉伯数字
    arabic_nums = re.findall(r"\d+", response)
    for num in arabic_nums:
        selected.append(int(num))
    
    return list(set(selected))  # 去重


def save_summary_to_log(date, new_items, recorded_items, selected_ids):
    """保存摘要到日志"""
    SUMMARY_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    log_data = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "new_items_count": len(new_items),
        "recorded_items_count": len(recorded_items),
        "selected_ids": selected_ids,
        "new_items": new_items,
        "recorded_items": recorded_items,
    }
    
    # 读取现有日志
    logs = []
    if SUMMARY_LOG.exists():
        with open(SUMMARY_LOG, encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                pass
    
    # 添加新日志
    logs.append(log_data)
    
    # 保留最近 30 天
    logs = logs[-30:]
    
    with open(SUMMARY_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    print("=== 每日摘要生成器 ===")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
    print("")
    
    # 模拟对话数据（实际应从会话历史获取）
    # TODO: 集成到 OpenClaw 后，从这里获取真实对话
    mock_conversations = [
        {"content": "安装了 memory-manager 技能", "timestamp": "2026-03-04 09:00", "sender": "user"},
        {"content": "讨论了 Token 节省方案，预计节省 90%", "timestamp": "2026-03-04 09:15", "sender": "user"},
        {"content": "用户提到项目下周截止", "timestamp": "2026-03-04 10:00", "sender": "user"},
        {"content": "早上好", "timestamp": "2026-03-04 08:00", "sender": "user"},  # 琐碎
        {"content": "配置了定时清理任务，每天 03:00 执行", "timestamp": "2026-03-04 11:00", "sender": "user"},
        {"content": "谢谢", "timestamp": "2026-03-04 12:00", "sender": "user"},  # 琐碎
        {"content": "用户说买了新的机械键盘", "timestamp": "2026-03-04 14:00", "sender": "user"},
    ]
    
    # 提取关键事项
    items = extract_key_items(mock_conversations)
    items = deduplicate_items(items)
    
    print(f"提取到 {len(items)} 个关键事项")
    print("")
    
    # 加载 MEMORY.md
    memory_content = load_memory()
    
    # 生成摘要
    new_items, recorded_items = generate_summary(items, memory_content)
    
    print(f"新增事项：{len(new_items)}")
    print(f"已记录事项：{len(recorded_items)}")
    print("")
    
    # 格式化输出
    date = datetime.now().strftime("%Y-%m-%d")
    summary = format_summary(new_items, recorded_items, date)
    
    print(summary)
    print("")
    
    # 保存到日志
    save_summary_to_log(date, new_items, recorded_items, [])
    
    print("摘要已保存到日志")


if __name__ == "__main__":
    main()
