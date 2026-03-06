# OpenClaw 钉钉定时提醒配置指南

## ✅ 已验证的配置方案

使用**隔离会话 + 直达钉钉路由**，完美解决定时提醒问题！

---

## 🚀 快速开始

### 用户在群里@AI 布置任务

```
用户：@AI 明天下午 3 点提醒我开会准备材料
```

### AI 解析并创建定时任务

```bash
openclaw cron add \
  --name "开会提醒 - 吴震宇 -20260305" \
  --at "2026-03-05T15:00:00+08:00" \
  --session isolated \
  --message "⏰ 开会提醒：请准备材料！" \
  --announce \
  --channel dingtalk \
  --delete-after-run
```

### AI 回复用户

```
✅ 已安排明天 15:00 提醒你开会准备材料
任务 ID：开会提醒 - 吴震宇 -20260305
```

---

## 📋 核心配置说明

### 关键参数组合

| 参数 | 值 | 说明 |
|------|-----|------|
| `--session isolated` | 独立会话 | 不依赖群聊上下文 |
| `--announce` | - | 发送消息到指定渠道 |
| `--channel dingtalk` | 钉钉 | 目标渠道 |
| `--at` | ISO 时间或 duration | 精确执行时间 |
| `--delete-after-run` | - | 执行后自动删除 |

### 时间格式

**绝对时间（ISO 8601）：**
```bash
--at "2026-03-05T15:00:00+08:00"  # 明天下午 3 点
--at "2026-03-05T09:00:00+08:00"  # 明天早上 9 点
```

**相对时间（duration）：**
```bash
--at "2m"    # 2 分钟后
--at "30m"   # 30 分钟后
--at "1h"    # 1 小时后
--at "24h"   # 24 小时后
```

---

## 🤖 AI 任务解析逻辑

### 1. 时间解析

```python
def parse_time(time_str):
    """解析时间表达式"""
    # 明天下午 3 点 → 2026-03-05T15:00:00+08:00
    # 1 小时后 → 1h
    # 30 分钟后 → 30m
    pass
```

### 2. 提醒内容提取

```python
def extract_reminder_content(message):
    """提取提醒内容"""
    # "提醒我开会" → "⏰ 开会提醒"
    # "记得带材料" → "📝 请准备材料"
    pass
```

### 3. 任务命名

```python
def generate_task_name(user, content, time):
    """生成唯一任务名"""
    # 吴震宇 + 开会 + 20260305 → "开会提醒 - 吴震宇 -20260305"
    pass
```

---

## 📝 完整示例

### 示例 1: 会议提醒

**用户输入：**
```
@AI 明天上午 9 点提醒我参加项目评审会议
```

**AI 创建的命令：**
```bash
openclaw cron add \
  --name "项目评审会议 - 吴震宇 -20260305" \
  --at "2026-03-05T09:00:00+08:00" \
  --session isolated \
  --message "📅 会议提醒：项目评审会议\n⏰ 时间：上午 9 点" \
  --announce \
  --channel dingtalk \
  --delete-after-run
```

**AI 回复：**
```
✅ 已安排明天 09:00 提醒你参加项目评审会议
```

---

### 示例 2: 健康提醒

**用户输入：**
```
@AI 每 2 小时提醒我喝水
```

**AI 创建的命令：**
```bash
openclaw cron add \
  --name "喝水提醒 - 吴震宇" \
  --every "2h" \
  --session isolated \
  --message "💧 喝水时间到了！起来活动一下～" \
  --announce \
  --channel dingtalk
```

**AI 回复：**
```
✅ 已设置每 2 小时提醒你喝水
第一次提醒将在 2 小时后
```

---

### 示例 3: 待办事项

**用户输入：**
```
@AI 今天下午 5 点提醒我交报告
```

**AI 创建的命令：**
```bash
openclaw cron add \
  --name "交报告 - 吴震宇 -20260304" \
  --at "2026-03-04T17:00:00+08:00" \
  --session isolated \
  --message "✅ 待办提醒：提交报告\n⏰ 截止时间：今天下午 5 点" \
  --announce \
  --channel dingtalk \
  --delete-after-run
```

**AI 回复：**
```
✅ 已安排今天 17:00 提醒你交报告
```

---

## 🔧 管理命令

### 查看任务列表

```bash
openclaw cron list
```

### 查看任务详情

```bash
openclaw cron list --json | jq '.[] | select(.name=="任务名")'
```

### 立即测试任务

```bash
openclaw cron run "任务名" --force
```

### 查看执行历史

```bash
openclaw cron runs "任务名"
```

### 删除任务

```bash
openclaw cron rm "任务名"
```

### 禁用/启用任务

```bash
openclaw cron disable "任务名"
openclaw cron enable "任务名"
```

---

## 📊 任务状态

| 状态 | 说明 |
|------|------|
| `idle` | 等待执行 |
| `running` | 正在执行 |
| `completed` | 执行成功 |
| `failed` | 执行失败 |
| `disabled` | 已禁用 |

---

## ⚠️ 注意事项

### 1. 时区问题

**务必使用 `+08:00` 时区：**
```bash
# ✅ 正确
--at "2026-03-05T15:00:00+08:00"

# ❌ 错误（默认 UTC）
--at "2026-03-05T15:00:00"
```

### 2. 任务命名

**使用唯一名称避免冲突：**
```bash
# ✅ 推荐格式
--name "内容 - 用户 - 日期"

# ❌ 避免重复
--name "提醒"  # 太通用
```

### 3. 一次性 vs 周期性

**一次性任务：**
```bash
--at "2026-03-05T15:00:00+08:00"
--delete-after-run  # 执行后自动删除
```

**周期性任务：**
```bash
--every "2h"  # 每 2 小时
# 不要加 --delete-after-run
```

---

## 🎯 最佳实践

### 1. 消息格式

```
[emoji] 提醒类型：内容
⏰ 时间：具体时间
📝 备注：额外信息（可选）
```

**示例：**
```
📅 会议提醒：项目评审会议
⏰ 时间：上午 9 点
📍 地点：会议室 A
```

### 2. 提前量设置

对于重要事件，设置多个提醒：

```bash
# 提前 1 天
openclaw cron add --at "2026-03-04T09:00:00" ...

# 提前 1 小时
openclaw cron add --at "2026-03-05T08:00:00" ...

# 准时提醒
openclaw cron add --at "2026-03-05T09:00:00" ...
```

### 3. 错误处理

添加 `--best-effort-deliver`：
```bash
openclaw cron add \
  ... \
  --best-effort-deliver \
  ...
```

这样即使消息发送失败，任务也不会报错。

---

## 📈 监控和调试

### 查看任务状态

```bash
openclaw cron status
```

### 查看执行日志

```bash
openclaw logs --follow | grep "cron"
```

### 测试任务

```bash
# 立即执行（不等待时间）
openclaw cron run "任务名" --force

# 查看输出
openclaw cron runs "任务名" --json | tail -20
```

---

## 🔗 相关文档

- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenClaw CLI - Cron](https://docs.openclaw.ai/cli/cron)
- [DingTalk 集成](https://docs.openclaw.ai/channels/dingtalk)

---

**最后更新**: 2026-03-04  
**状态**: ✅ 已验证可用  
**测试任务**: 测试提醒 - 烧热水（2 分钟后执行）
