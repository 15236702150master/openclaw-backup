---
name: daily-summary
description: Generate daily conversation summaries at 23:00 with numbered items for user to select what to remember. Shows what's already recorded vs new items. User selects which items to save to MEMORY.md.
---

# Daily Summary

每日对话摘要技能，每天晚上 23:00 自动生成过去 24 小时的对话摘要，用户选择需要记录的内容。

## 工作流程

```
每天 23:00
    ↓
自动扫描今日对话
    ↓
生成带序号的摘要列表
    ↓
标注已记录/未记录
    ↓
发送给用户确认
    ↓
用户选择序号
    ↓
分类记录到 MEMORY.md
```

---

## 摘要格式

### 输出模板

```
📅 每日摘要 - 2026-03-04

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【新增事项】需要确认是否记录

① 安装了 memory-manager 技能 [技能管理]
② 讨论了 Token 节省方案，预计节省 90% [重要决策]
③ 用户提到项目下周截止 [待办/项目]
④ 配置了定时清理任务，每天 03:00 执行 [配置变更]
⑤ 用户说买了新的机械键盘 [个人信息]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【已记录事项】已存在于 MEMORY.md

✓ ⑥ 安装了 auto-install-skill 技能 (2026-03-04 上午)
✓ ⑦ 配置了 WSL2 环境 (2026-03-03)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【未分类对话】可能是琐事

• 讨论了天气
• 闲聊
• 临时查询（已解答）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请回复需要记录的序号，例如：
"记录 ①②③⑤" 或 "全部记录" 或 "都不记录"
```

---

## 分类规则

### 自动分类建议

| 类型 | 关键词 | 建议分类 |
|------|--------|----------|
| 技能安装/卸载 | "安装"、"卸载"、"技能" | 技能配置 |
| 配置变更 | "配置"、"设置"、"修改" | 系统配置 |
| 项目相关 | "项目"、"截止"、" deadline" | 待办/项目 |
| 个人信息 | "买了"、"喜欢"、"偏好" | 个人信息 |
| 重要决策 | "决定"、"采用"、"方案" | 重要决策 |
| 临时查询 | "天气"、"搜索"、"查找" | 临时信息（不记录） |

---

## 已记录检测

### 检测方法

```python
def is_already_recorded(item, memory_md):
    """检查是否已存在于 MEMORY.md"""
    
    # 1. 精确匹配
    if item in memory_md:
        return True
    
    # 2. 语义相似（简化版：关键词匹配）
    keywords = extract_keywords(item)
    match_count = sum(1 for k in keywords if k in memory_md)
    if match_count >= len(keywords) * 0.7:
        return True
    
    # 3. 检查最近 7 天的日志
    recent_logs = get_recent_logs(days=7)
    if item in recent_logs:
        return True
    
    return False
```

### 标注方式

```
已记录：✓ ① 安装了某技能 (2026-03-04 上午)
未记录：② 讨论了某方案
```

---

## 用户交互

### 用户回复格式

```
记录 ①②③          → 记录指定序号
全部记录            → 记录所有新增事项
都不记录/跳过       → 全部跳过
记录 ①③，跳过 ②     → 部分记录
记录 ① 到技能配置    → 指定分类记录
```

### AI 确认回复

```
✅ 已记录：
① 安装了 memory-manager 技能 → 技能配置
② Token 节省方案 → 重要决策
③ 项目下周截止 → 待办/项目
⑤ 买了新键盘 → 个人信息

⏭️ 已跳过：
④ 定时清理任务配置 (用户选择跳过)

📝 MEMORY.md 已更新
```

---

## 实现细节

### 对话历史扫描

```python
def scan_today_conversations():
    """扫描今日对话"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 获取今日对话历史
    history = get_session_history(
        since=f"{today} 00:00:00",
        until=f"{today} 23:59:59"
    )
    
    # 提取关键对话
    items = []
    for msg in history:
        if is_trivial(msg):
            continue  # 跳过闲聊
        
        if has_significance(msg):
            items.append(extract_item(msg))
    
    return items
```

### 重要性判断

```python
def has_significance(msg):
    """判断是否有记录价值"""
    
    # 跳过这些
    trivial_patterns = [
        "早上好", "谢谢", "好的", "明白了",
        "天气", "几点了", "随机查询"
    ]
    
    # 记录这些
    significant_patterns = [
        "记住", "安装", "卸载", "配置",
        "决定", "项目", "买了", "喜欢",
        "提醒我", "待办"
    ]
    
    for pattern in trivial_patterns:
        if pattern in msg:
            return False
    
    for pattern in significant_patterns:
        if pattern in msg:
            return True
    
    return False  # 默认不记录，等用户确认
```

### 分类记录

```python
def record_to_memory(items, categories):
    """分类记录到 MEMORY.md"""
    
    memory_md = load_memory()
    
    for item in items:
        category = categories.get(item.id, "其他")
        
        if category == "技能配置":
            memory_md["skills"].append(item.content)
        elif category == "系统配置":
            memory_md["config"].append(item.content)
        elif category == "待办/项目":
            memory_md["todos"].append(item.content)
        elif category == "个人信息":
            memory_md["personal"].append(item.content)
        elif category == "重要决策":
            memory_md["decisions"].append(item.content)
        else:
            memory_md["other"].append(item.content)
    
    save_memory(memory_md)
```

---

## 定时任务配置

### 每天 23:00 执行

```json
{
  "daily-summary": {
    "schedule": "0 23 * * *",
    "enabled": true,
    "delivery": "main-session",
    "waitUserConfirm": true,
    "timeout": "2h"  // 等待用户确认到 01:00
  }
}
```

### 用户未回复的处理

```
23:00 发送摘要
    ↓
等待用户回复（最多 2 小时）
    ↓
01:00 前用户回复 → 按回复记录
01:00 用户未回复 → 询问"需要我记录吗？"
    ↓
仍无回复 → 暂不记录，等用户下次主动提及
```

---

## Token 节省优化

### 1. 智能扫描

```python
# 只扫描今日对话，不加载全部历史
today_history = get_history(
    since="today 00:00",
    limit=100  # 最多 100 条
)
```

### 2. 摘要压缩

```
原始对话：50 条消息，~10k tokens
摘要列表：10 条关键事项，~1k tokens
节省：90%
```

### 3. 按需加载

```
生成摘要时：只加载今日对话
用户确认后：才加载 MEMORY.md
```

### 4. 独立 Session

```
定时任务用独立 session 执行
不消耗主会话 token
完成后销毁
```

---

## 错误处理

### 摘要生成失败

```
如果扫描失败：
1. 记录错误日志
2. 通知用户"今日摘要生成失败"
3. 建议用户手动回顾
```

### 用户回复解析失败

```
如果无法解析用户回复：
1. 询问澄清"您想记录哪些序号？"
2. 提供示例格式
3. 等待用户重新回复
```

### MEMORY.md 写入失败

```
如果写入失败：
1. 重试 3 次
2. 通知用户"记录失败，请手动保存"
3. 保存待记录内容到临时文件
```

---

## 示例对话

### 场景 1：用户选择部分记录

```
AI [23:00]:
📅 每日摘要 - 2026-03-04

【新增事项】
① 安装了 memory-manager 技能
② 讨论了 Token 节省方案
③ 用户说项目下周截止
④ 买了新的机械键盘

【已记录】
✓ ⑤ 配置了清理任务 (上午)

请回复需要记录的序号

用户 [23:15]:
记录 ①②④

AI [23:16]:
✅ 已记录：
① → 技能配置
② → 重要决策
④ → 个人信息

⏭️ 已跳过：
③ (用户未选择)

📝 MEMORY.md 已更新
```

### 场景 2：用户全部记录

```
用户：全部记录

AI：
✅ 已记录所有 4 项：
① → 技能配置
② → 重要决策
③ → 待办/项目
④ → 个人信息

📝 MEMORY.md 已更新
```

### 场景 3：用户跳过

```
用户：都不记录/今天没什么重要的

AI：
好的，已跳过今日摘要。
如有需要，随时说"记住 X"来手动记录。
```

---

## 配置选项

### ~/.openclaw/workspace/summary-config.json

```json
{
  "schedule": "23:00",
  "timezone": "Asia/Shanghai",
  "waitTimeout": "2h",
  "autoCategories": true,
  "detectDuplicates": true,
  "trivialThreshold": "high",
  "maxItems": 20,
  "delivery": "dingtalk"
}
```

---

## 相关技能

- **memory-manager**: 记忆管理
- **todo-manager**: 待办管理

---

**设计原则：** 用户主导，AI 辅助，不错过重要信息
