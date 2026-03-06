#!/usr/bin/env python3
"""
模型路由器 - 根据任务复杂度推荐合适的模型
自动检测通信模式，强制使用 Haiku 节省 token
"""

import re
import sys

# 通信模式关键词（强制 Haiku，从不用 Sonnet/Opus）
COMMUNICATION_KEYWORDS = [
    # 问候
    "hi", "hey", "hello", "yo",
    "早上好", "下午好", "晚上好",
    # 感谢
    "thanks", "thank you", "thx",
    "谢谢", "感谢",
    # 确认
    "ok", "okay", "sure", "got it",
    "好的", "好的", "明白了", "懂了",
    # 简短回应
    "yes", "no", "yep", "nope",
    "是", "不是", "对",
    # 测试
    "测试", "test", "在吗", "你好吗"
]

# 背景任务（推荐 Haiku）
BACKGROUND_TASKS = [
    r"\b(检查 | 监控 | scan|check|monitor)\b",
    r"\b(解析 | 提取 | parse|extract)\b",
    r"\b(日志 | logs|log)\b",
    r"\b(提醒 | reminder|cron|定时)\b",
    r"\b(心跳 | heartbeat)\b",
    r"\b(清理 | cleanup|clean)\b",
]

# 简单任务（推荐 Haiku）
SIMPLE_TASKS = [
    r"\b(读取 | 打开 | read|open)\b",
    r"\b(查找 | 搜索 | find|search)\b",
    r"\b(列出 | 显示 | list|show)\b",
    r"\b(复制 | 移动 | copy|move)\b",
    r"\b(删除 | 删除 | delete|remove)\b",
]

# 中等任务（推荐 Sonnet）
MEDIUM_TASKS = [
    r"\b(写 | 创建 | 生成 | write|create|generate)\b",
    r"\b(函数 | 代码 | function|code)\b",
    r"\b(分析 | 分析 | analyze)\b",
    r"\b(总结 | 摘要 | summarize)\b",
    r"\b(编辑 | 修改 | edit|modify)\b",
]

# 复杂任务（推荐 Opus）
COMPLEX_TASKS = [
    r"\b(设计 | 架构 | design|architecture)\b",
    r"\b(优化 | 重构 | optimize|refactor)\b",
    r"\b(调试 | 解决 | debug|solve)\b",
    r"\b(研究 | 调查 | research|investigate)\b",
]

# 模型配置
MODELS = {
    "haiku": {
        "name": "bailian/qwen3-coder-next",
        "cost_per_mtok": 0.002,
        "description": "快速便宜，简单任务"
    },
    "sonnet": {
        "name": "bailian/qwen3.5-plus",
        "cost_per_mtok": 0.03,
        "description": "平衡，默认选择"
    },
    "opus": {
        "name": "bailian/qwen3-max-2026-01-23",
        "cost_per_mtok": 0.15,
        "description": "复杂推理，谨慎使用"
    }
}


def classify_task(prompt):
    """分类任务并推荐模型"""
    prompt_lower = prompt.lower()
    
    # 1. 检查通信模式（强制 Haiku）
    # 只在短消息中检查通信模式
    if len(prompt) < 30:
        for keyword in COMMUNICATION_KEYWORDS:
            if keyword.lower() in prompt_lower:
                # 确保是整个词匹配，不是部分匹配
                if re.search(rf"\b{re.escape(keyword)}\b", prompt_lower, re.IGNORECASE) or keyword in prompt:
                    return {
                        "tier": "haiku",
                        "model": MODELS["haiku"]["name"],
                        "reason": "通信模式 - 强制 Haiku",
                        "confidence": 0.95,
                        "cost_savings": "93% vs Sonnet, 98% vs Opus"
                    }
    
    # 2. 检查复杂任务（优先检查，推荐 Opus）
    for pattern in COMPLEX_TASKS:
        if re.search(pattern, prompt_lower):
            return {
                "tier": "opus",
                "model": MODELS["opus"]["name"],
                "reason": "复杂任务 - 推荐 Opus",
                "confidence": 0.75,
                "note": "谨慎使用，成本高"
            }
    
    # 3. 检查中等任务（推荐 Sonnet）
    for pattern in MEDIUM_TASKS:
        if re.search(pattern, prompt_lower):
            return {
                "tier": "sonnet",
                "model": MODELS["sonnet"]["name"],
                "reason": "中等任务 - 推荐 Sonnet",
                "confidence": 0.80,
                "cost_savings": "80% vs Opus"
            }
    
    # 4. 检查背景任务（推荐 Haiku）
    for pattern in BACKGROUND_TASKS:
        if re.search(pattern, prompt_lower):
            return {
                "tier": "haiku",
                "model": MODELS["haiku"]["name"],
                "reason": "背景任务 - 推荐 Haiku",
                "confidence": 0.90,
                "cost_savings": "93% vs Sonnet"
            }
    
    # 5. 检查简单任务（推荐 Haiku）
    for pattern in SIMPLE_TASKS:
        if re.search(pattern, prompt_lower):
            return {
                "tier": "haiku",
                "model": MODELS["haiku"]["name"],
                "reason": "简单任务 - 推荐 Haiku",
                "confidence": 0.85,
                "cost_savings": "93% vs Sonnet"
            }
    
    # 6. 默认：Sonnet（平衡）
    return {
        "tier": "sonnet",
        "model": MODELS["sonnet"]["name"],
        "reason": "默认 - 平衡选择",
        "confidence": 0.70,
        "note": "无法分类，使用默认模型"
    }


def main():
    if len(sys.argv) < 2:
        print("用法：model-router.py <用户提示> [当前模型]")
        print("\n示例:")
        print("  model-router.py \"谢谢\"")
        print("  model-router.py \"帮我写个函数\"")
        print("  model-router.py \"设计一个微服务架构\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    current_model = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = classify_task(prompt)
    
    print(f"\n📊 模型路由建议")
    print(f"{'='*50}")
    print(f"用户提示：{prompt}")
    print(f"推荐模型：{result['model']}")
    print(f"任务类型：{result['tier']}")
    print(f"理由：{result['reason']}")
    print(f"置信度：{result['confidence']*100:.0f}%")
    
    if "cost_savings" in result:
        print(f"节省：{result['cost_savings']}")
    
    if "note" in result:
        print(f"注意：{result['note']}")
    
    if current_model:
        if current_model != result['model']:
            print(f"\n⚠️  建议切换：{current_model} → {result['model']}")
        else:
            print(f"\n✅ 当前模型已合适")
    
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
