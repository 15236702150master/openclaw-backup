#!/usr/bin/env python3
"""
每日摘要生成器 - AI 版
使用 AI 模型分析对话历史，生成准确的摘要
"""

import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SUMMARY_LOG = WORKSPACE / "memory" / "daily-summaries.json"


def load_memory():
    """加载 MEMORY.md"""
    if not MEMORY_FILE.exists():
        return ""
    with open(MEMORY_FILE, encoding="utf-8") as f:
        return f.read()[:10000]  # 限制大小，节省 token


def get_today_conversations():
    """
    获取今日对话历史
    实际使用时通过 OpenClaw API 获取
    这里用示例数据演示
    """
    # TODO: 集成到 OpenClaw 后，从这里获取真实对话
    # 示例数据结构
    return [
        {"role": "user", "content": "帮我安装 memory-manager 技能", "timestamp": "09:00"},
        {"role": "assistant", "content": "好的，已安装 memory-manager 技能", "timestamp": "09:01"},
        {"role": "user", "content": "讨论了 Token 节省方案，预计能节省 90%", "timestamp": "09:15"},
        {"role": "user", "content": "早上好", "timestamp": "08:00"},  # 闲聊，应该被过滤
        {"role": "user", "content": "项目下周截止，记得提醒我", "timestamp": "10:00"},
        {"role": "user", "content": "谢谢", "timestamp": "12:00"},  # 闲聊
        {"role": "user", "content": "买了新的机械键盘，手感不错", "timestamp": "14:00"},
        {"role": "user", "content": "配置了每天 23:00 的每日摘要任务", "timestamp": "11:00"},
    ]


def analyze_with_ai(conversations):
    """
    使用 AI 分析对话，提取关键事项
    
    实际实现应该调用 sessions_spawn 或直接调用模型
    这里用示例输出演示
    """
    
    # 构建提示词
    prompt = """
你是一位专业的对话分析师。请分析以下对话历史，提取需要记录的重要信息。

## 判断标准

### 应该记录的信息
- 技能安装/卸载
- 配置变更
- 重要决策和讨论
- 项目/任务相关
- 个人信息（偏好、习惯、购买等）
- 待办和提醒设置

### 不应该记录的信息
- 日常问候（早上好、谢谢等）
- 临时查询（天气、时间等）
- 闲聊内容
- 已解答的简单问题

## 对话历史

"""
    
    # 格式化对话
    for conv in conversations:
        prompt += f"[{conv['timestamp']}] {conv['role']}: {conv['content']}\n"
    
    prompt += """
## 输出格式

请以 JSON 格式输出：
```json
{
  "items": [
    {
      "id": 1,
      "content": "事项内容",
      "category": "技能配置 | 系统配置 | 待办/项目 | 个人信息 | 重要决策 | 其他",
      "importance": "high|medium|low"
    }
  ]
}
```

## 开始分析
"""
    
    # TODO: 实际调用 AI 模型
    # response = call_llm_api(prompt)
    # return parse_json(response)
    
    # 示例输出（演示用）
    return {
        "items": [
            {
                "id": 1,
                "content": "安装了 memory-manager 技能",
                "category": "技能配置",
                "importance": "high"
            },
            {
                "id": 2,
                "content": "讨论了 Token 节省方案，预计节省 90%",
                "category": "重要决策",
                "importance": "high"
            },
            {
                "id": 3,
                "content": "项目下周截止，需要设置提醒",
                "category": "待办/项目",
                "importance": "high"
            },
            {
                "id": 4,
                "content": "配置了每日摘要任务，每天 23:00 执行",
                "category": "系统配置",
                "importance": "medium"
            },
            {
                "id": 5,
                "content": "买了新的机械键盘",
                "category": "个人信息",
                "importance": "low"
            }
        ]
    }


def check_recorded_status(items, memory_content):
    """
    使用 AI 判断事项是否已记录
    
    实际实现应该调用 AI 模型
    """
    
    # TODO: 调用 AI 判断
    # prompt = f"""
    # 判断以下事项是否已存在于 MEMORY.md 中：
    # 
    # MEMORY.md: {memory_content[:5000]}
    # 
    # 事项：{items}
    # 
    # 输出每个事项的状态（recorded/new）
    # """
    
    # 示例输出（演示用）
    results = []
    for item in items:
        # 简单演示：假设第 1 项已记录
        if item["id"] == 1:
            item["status"] = "recorded"
            item["record_location"] = "## 技能配置 - memory-manager 技能"
        else:
            item["status"] = "new"
        results.append(item)
    
    return results


def format_summary(items):
    """格式化摘要输出"""
    new_items = [i for i in items if i["status"] == "new"]
    recorded_items = [i for i in items if i["status"] == "recorded"]
    
    output = []
    output.append("📅 每日摘要 - " + datetime.now().strftime("%Y-%m-%d"))
    output.append("")
    output.append("━" * 32)
    
    # 新增事项
    if new_items:
        output.append("【新增事项】需要确认是否记录")
        output.append("")
        for item in new_items:
            icon = "①②③④⑤⑥⑦⑧⑨⑩"[item["id"]-1] if item["id"] <= 10 else f"{item['id']}."
            output.append(f"{icon} {item['content']} [{item['category']}]")
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
            icon = "①②③④⑤⑥⑦⑧⑨⑩"[item["id"]-1] if item["id"] <= 10 else f"{item['id']}."
            output.append(f"✓ {icon} {item['content']} [{item['category']}]")
            output.append(f"   记录位置：{item.get('record_location', '未知')}")
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
    import re
    arabic_nums = re.findall(r"\d+", response)
    for num in arabic_nums:
        selected.append(int(num))
    
    return list(set(selected))


def record_to_memory(selected_ids, items):
    """
    使用 AI 分类记录到 MEMORY.md
    
    实际实现应该调用 AI 生成更新内容
    """
    
    selected_items = [i for i in items if i["id"] in selected_ids]
    
    # TODO: 调用 AI 生成更新内容
    # prompt = f"""
    # 将以下事项分类记录到 MEMORY.md：
    # 
    # 事项：{selected_items}
    # 
    # 当前 MEMORY.md 结构：
    # {load_memory()[:5000]}
    # 
    # 输出更新后的 MEMORY.md 内容
    # """
    
    # 示例：手动更新（实际应该用 AI）
    memory = load_memory()
    
    for item in selected_items:
        if item["category"] == "技能配置":
            memory += f"\n- {item['content']} ({datetime.now().strftime('%Y-%m-%d')})"
        elif item["category"] == "重要决策":
            memory += f"\n- {item['content']} ({datetime.now().strftime('%Y-%m-%d')})"
    
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write(memory)
    
    return True


def save_summary_log(date, items, selected_ids):
    """保存摘要日志"""
    SUMMARY_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    log_data = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "total_items": len(items),
        "selected_ids": selected_ids,
        "items": items,
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
    print("=== 每日摘要生成器（AI 版）===")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
    print("")
    
    # 1. 获取今日对话
    print("获取今日对话...")
    conversations = get_today_conversations()
    print(f"获取到 {len(conversations)} 条对话")
    print("")
    
    # 2. AI 分析
    print("AI 分析对话...")
    analysis = analyze_with_ai(conversations)
    items = analysis["items"]
    print(f"提取到 {len(items)} 个关键事项")
    print("")
    
    # 3. 检测已记录事项
    print("检测已记录事项...")
    memory = load_memory()
    items = check_recorded_status(items, memory)
    
    new_count = sum(1 for i in items if i["status"] == "new")
    recorded_count = sum(1 for i in items if i["status"] == "recorded")
    print(f"新增：{new_count}, 已记录：{recorded_count}")
    print("")
    
    # 4. 生成摘要
    summary = format_summary(items)
    print(summary)
    print("")
    
    # 5. 保存日志
    save_summary_log(
        datetime.now().strftime("%Y-%m-%d"),
        items,
        []
    )
    
    print("摘要已保存到日志")
    print("")
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
