---
name: daily-summary-ai
description: AI-powered daily summary generator. Uses LLM to analyze conversation history, extract key items, and generate numbered summary for user confirmation. Much more accurate than script-based extraction.
---

# Daily Summary AI

使用 AI 模型生成每日对话摘要，比脚本更准确地理解对话内容和重要性。

## 工作流程

```
每天 23:00
    ↓
获取今日对话历史
    ↓
调用 AI 模型分析对话
    ↓
生成带序号的摘要列表
    ↓
标注已记录/未记录
    ↓
发送给用户确认
    ↓
用户回复序号
    ↓
AI 分类记录到 MEMORY.md
```

---

## AI 提示词设计

### 对话分析提示词

```
你是一位专业的对话分析师。请分析以下对话历史，提取需要记录的重要信息。

## 任务要求

1. **提取关键事项**：识别对话中重要的、值得记录的信息
2. **判断重要性**：区分重要信息和日常闲聊
3. **分类建议**：为每个事项建议合适的分类
4. **去重检测**：识别可能重复的内容

## 判断标准

### 应该记录的信息
- 技能安装/卸载
- 配置变更
- 重要决策和讨论
- 项目/任务相关
- 个人信息（偏好、习惯、购买等）
- 待办和提醒设置
- 问题和解决方案

### 不应该记录的信息
- 日常问候（早上好、谢谢等）
- 临时查询（天气、时间等）
- 闲聊内容
- 已解答的简单问题
- 重复的信息

## 输出格式

请以 JSON 格式输出：

```json
{
  "items": [
    {
      "id": 1,
      "content": "安装了 memory-manager 技能",
      "category": "技能配置",
      "importance": "high",
      "timestamp": "2026-03-04 09:00",
      "reason": "技能配置变更，影响系统功能"
    },
    {
      "id": 2,
      "content": "讨论了 Token 节省方案，预计节省 90%",
      "category": "重要决策",
      "importance": "high",
      "timestamp": "2026-03-04 09:15",
      "reason": "重要技术决策，影响系统架构"
    }
  ],
  "summary": "今日讨论了系统架构优化，安装了记忆管理技能，确定了 Token 节省方案。",
  "total_items": 2,
  "high_importance": 2,
  "medium_importance": 0,
  "low_importance": 0
}
```

## 对话历史

{conversation_history}

## 开始分析
```

---

## 已记录检测提示词

```
请判断以下事项是否已存在于 MEMORY.md 中。

## MEMORY.md 内容

{memory_content}

## 待检测事项

{items}

## 判断标准

- **已记录**：事项的核心信息已存在于 MEMORY.md
- **部分记录**：相关信息存在但不完整
- **未记录**：完全新的信息

## 输出格式

```json
{
  "results": [
    {
      "item_id": 1,
      "content": "安装了 memory-manager 技能",
      "status": "recorded",
      "reason": "MEMORY.md 中已有'memory-manager 技能已安装'的记录",
      "original_record": "memory-manager：记忆管理和清理（2026-03-04）"
    },
    {
      "item_id": 2,
      "content": "讨论了 Token 节省方案",
      "status": "new",
      "reason": "MEMORY.md 中无相关记录"
    }
  ]
}
```

## 开始检测
```

---

## 分类记录提示词

```
请根据用户选择的序号，将以下事项分类记录到 MEMORY.md。

## 用户选择

记录的序号：{selected_ids}

## 待记录事项

{selected_items}

## MEMORY.md 当前结构

{memory_structure}

## 分类规则

- **技能配置** → 添加到"## 技能配置"章节
- **系统配置** → 添加到"## 系统配置"章节
- **待办/项目** → 添加到"## 待办事项"章节
- **个人信息** → 添加到"## 个人信息"章节
- **重要决策** → 添加到"## 重要决策"章节
- **其他** → 添加到"## 其他"章节

## 输出格式

请输出更新后的 MEMORY.md 内容（仅更新的部分）：

```markdown
## 技能配置
- 新增：安装了 memory-manager 技能 (2026-03-04)

## 重要决策
- 新增：采用事件驱动架构，Token 节省 90% (2026-03-04)
```

## 开始分类
```

---

## 实现方式

### 方法 1: Sub-agent 模式

```python
# 每天 23:00 触发
def generate_daily_summary():
    # 1. 获取今日对话历史
    history = get_today_conversations()
    
    # 2. 调用 AI 分析
    analysis = sessions_spawn(
        task=f"""分析今日对话，提取重要事项：
        {history}
        
        输出 JSON 格式的摘要列表。""",
        runtime="subagent",
        mode="run"
    )
    
    # 3. 检测已记录事项
    memory = load_memory()
    check = sessions_spawn(
        task=f"""判断以下事项是否已记录：
        事项：{analysis.items}
        MEMORY.md: {memory}
        
        标注每个事项的状态（已记录/未记录）""",
        runtime="subagent",
        mode="run"
    )
    
    # 4. 生成摘要发送给用户
    summary = format_summary(check.results)
    send_to_user(summary)
    
    # 5. 等待用户回复
    # 6. 用户回复后，调用 AI 分类记录
```

### 方法 2: 直接调用模型

```python
# 使用当前会话的模型
def analyze_with_llm(prompt, history):
    response = model.generate(
        prompt=prompt,
        context=history,
        temperature=0.3,  # 低温度，更稳定
        max_tokens=2000
    )
    return parse_json(response)
```

---

## Token 优化

### 1. 对话历史压缩

```
原始对话：100 条消息，~20k tokens
↓ 预处理（去除闲聊）
有效对话：30 条消息，~6k tokens
↓ AI 分析
摘要列表：10 条事项，~1k tokens
节省：95%
```

### 2. 分批处理

```
如果对话历史过长（>50k tokens）：
- 按时间分段（上午/下午/晚上）
- 每段单独分析
- 合并结果
```

### 3. 缓存机制

```
如果今天已生成过摘要：
- 缓存结果
- 用户询问时直接返回
- 不重复调用 AI
```

---

## 优势对比

| 特性 | 脚本版 | AI 版 |
|------|--------|------|
| 准确性 | ❌ 关键词匹配 | ✅ 语义理解 |
| 重要性判断 | ❌ 规则匹配 | ✅ 上下文理解 |
| 去重能力 | ❌ 字符串匹配 | ✅ 语义去重 |
| 分类准确性 | ❌ 关键词分类 | ✅ 理解内容分类 |
| 灵活性 | ❌ 固定规则 | ✅ 自适应 |
| Token 消耗 | ✅ 低 | ⚠️ 中等（但值得） |

---

## 错误处理

### AI 分析失败

```
如果 AI 调用失败：
1. 重试 1 次
2. 通知用户"今日摘要生成失败，请稍后重试"
3. 记录错误日志
4. 建议用户手动回顾
```

### 输出格式错误

```
如果 AI 输出不是有效 JSON：
1. 尝试修复 JSON
2. 如果修复失败，请求 AI 重新输出
3. 记录错误日志
```

---

## 配置选项

```json
{
  "daily-summary": {
    "enabled": true,
    "schedule": "23:00",
    "model": "bailian/qwen3.5-plus",
    "maxTokens": 2000,
    "temperature": 0.3,
    "waitUserConfirm": true,
    "timeout": "2h",
    "cache": true
  }
}
```

---

## 示例对话

### 用户视角

```
AI [23:00]:
📅 每日摘要 - 2026-03-04

【新增事项】
① 安装了 memory-manager 技能 [技能配置]
② 讨论了 Token 节省方案，决定采用事件驱动架构 [重要决策]
③ 用户提到项目下周截止，需要提醒 [待办/项目]
④ 配置了每日摘要任务，23:00 执行 [系统配置]
⑤ 用户说买了新的机械键盘 [个人信息]

【已记录事项】
✓ ⑥ 安装了 auto-install-skill 技能 (上午已记录)

请回复需要记录的序号

用户 [23:15]:
记录 ①②③⑤

AI [23:16]:
✅ 已记录：
① → 技能配置
② → 重要决策
③ → 待办/项目
⑤ → 个人信息

⏭️ 已跳过：
④ (用户未选择)

📝 MEMORY.md 已更新
```

---

## 相关技能

- **memory-manager**: 记忆管理
- **todo-manager**: 待办管理

---

**设计原则：** AI 理解，用户确认，准确记录
