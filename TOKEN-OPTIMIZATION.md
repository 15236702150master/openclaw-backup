# Token 节省优化方案

## 📊 问题现状

### 原方案（每 30 分钟心跳）
```
每天检查次数：48 次
每次 token 消耗：~500-1000 tokens
每天总消耗：24k-48k tokens
每月总消耗：720k-1.4M tokens ❌
```

### 问题
- 无操作也消耗 token
- 定时任务故障无补救
- 上下文加载过多

---

## ✅ 优化方案

### 架构对比

| 特性 | 原方案 | 新方案 |
|------|--------|--------|
| 检查频率 | 每 30 分钟 | 事件驱动 + 定时 |
| Token 消耗 | 24k-48k/天 | <2k/天 |
| 故障补救 | ❌ 无 | ✅ 启动时补偿 |
| 上下文加载 | 全部 | 分级加载 |
| 任务隔离 | ❌ 混合 | ✅ 独立 session |

---

## 🧠 Token 节省策略

### 1. 事件驱动记忆记录

**触发条件：**
```
✅ 用户明确说"记住 X" → 立即记录 (~100 tokens)
✅ 技能安装/卸载 → 更新配置 (~200 tokens)
✅ 重要配置变更 → 更新状态 (~150 tokens)
✅ 每天 23:00 可选总结 (~500 tokens)

❌ 日常闲聊 → 不记录
❌ 临时查询 → 不记录
❌ 已存在信息 → 跳过
```

**节省估算：**
```
原方案：心跳检查自动记录 → 48 次/天 × 500 tokens = 24k tokens
新方案：用户触发记录 → 5 次/天 × 200 tokens = 1k tokens
节省：96% ↓
```

### 2. 分级上下文加载

```python
# L1 - 最小上下文（默认）
加载：MEMORY.md
大小：~500 tokens

# L2 - 标准上下文（用户提问时）
加载：MEMORY.md + memory/最近 3 天
大小：~1500 tokens

# L3 - 完整上下文（用户明确要求）
加载：全部文件
大小：~5000+ tokens
```

**节省估算：**
```
原方案：每次加载全部 → 5000 tokens × 48 次 = 240k tokens/天
新方案：默认 L1 + 按需 L2/L3 → 50k tokens/天
节省：79% ↓
```

### 3. 独立 Session 定时任务

```
原方案：主会话执行定时任务
- 加载主会话历史 (~10k tokens)
- 执行任务
- 保留到上下文

新方案：独立 session 执行
- 不加载主会话历史
- 执行任务
- 完成后销毁 session
- 只记录结果到日志
```

**节省估算：**
```
原方案：48 次 × 10k tokens = 480k tokens/天
新方案：独立 session 不消耗主会话 token
节省：100% ↓
```

### 4. 对话历史压缩

```markdown
# 优化前（50 轮对话）
用户：... (50 条消息)
助手：... (50 条回复)
= ~10k tokens

# 优化后
[对话摘要]
讨论了 X、Y、Z 主题
决定：A、B、C
下一步：...
= ~500 tokens (节省 95%)
```

**触发条件：**
- 对话轮次 > 20 → 自动摘要
- 用户说"总结一下" → 立即摘要
- 长对话结束 → 询问"需要总结吗？"

### 5. 日志内容压缩

```markdown
# 优化前
2026-03-04 09:00:00 用户说早上好
2026-03-04 09:05:00 用户询问天气
2026-03-04 09:10:00 用户让我找文件
2026-03-04 09:15:00 找到了 PDF
2026-03-04 09:20:00 提取了内容
= 5 行，~200 tokens

# 优化后
2026-03-04: 早晨问候、天气查询、PDF 文件提取
= 1 行，~40 tokens (节省 80%)
```

### 6. 记忆去重

```python
# 写入前检查
def should_record(new_content):
    if new_content in MEMORY.md:
        return False  # 跳过重复
    if is_trivial(new_content):
        return False  # 跳过琐事
    return True
```

### 7. 懒加载文件

```python
# 优化前
files = list_all_files()  # 加载所有
for f in files:
    process(f)

# 优化后
def find_file(query):
    # 先问清楚再查找
    location = ask_user("在哪里找？")
    file_type = ask_user("什么类型？")
    # 只加载相关目录
    return search(location, file_type)
```

---

## 🛡️ 容错机制

### 故障场景和补救

| 故障类型 | 检测方式 | 补救措施 |
|----------|----------|----------|
| Gateway 崩溃 | 启动时检查 | 立即执行错过的任务 |
| 定时任务失败 | 状态追踪 | 重试 3 次，间隔 30 分钟 |
| 网络中断 | 超时检测 | 恢复后补偿执行 |
| 磁盘满 | 空间检查 | 紧急清理 + 通知用户 |
| 脚本错误 | 返回码检查 | 记录错误 + 下次重试 |

### 启动时补偿检查

```
每次 Gateway 启动/会话恢复
       ↓
读取 .task-state.json
       ↓
检查每个任务的 nextRun
   ├─ 已错过且在 24h 内 → 立即补救
   ├─ 已错过超过 24h → 跳过，等下次
   └─ 未错过 → 正常等待
```

### 任务状态追踪

```json
{
  "daily-cleanup": {
    "lastRun": "2026-03-04T03:00:00+08:00",
    "nextRun": "2026-03-05T03:00:00+08:00",
    "status": "success",
    "missedCount": 0
  }
}
```

### 健康检查（低频）

```
频率：每 6 小时（而非 30 分钟）
检查项：
- 任务状态是否正常
- 日志文件是否过大
- 工作区空间是否充足
Token 消耗：~100 tokens/次
每天总消耗：400 tokens（vs 原方案 24k-48k）
```

---

## 📈 效果对比

### Token 消耗

| 项目 | 原方案/天 | 新方案/天 | 节省 |
|------|-----------|-----------|------|
| 心跳检查 | 24k-48k | 0 | 100% |
| 记忆记录 | 5k | 1k | 80% |
| 上下文加载 | 50k | 10k | 80% |
| 定时任务 | 10k | 0 | 100% |
| 健康检查 | 2k | 0.4k | 80% |
| **总计** | **91k-115k** | **~11.4k** | **87-90%** |

### 每月节省

```
原方案：2.7M - 3.4M tokens/月
新方案：~340k tokens/月
每月节省：~3M tokens (约 90%)
```

---

## 🔧 实施清单

### 已完成
- [x] 创建 memory-manager 技能
- [x] 创建清理脚本 cleanup.sh
- [x] 创建任务管理器 task-manager.py
- [x] 配置文件 task-config.json
- [x] 状态追踪 .task-state.json
- [x] 禁用心跳检查（HEARTBEAT.md）

### 待完成
- [ ] 配置系统 cron 任务
- [ ] 实现记忆提炼脚本
- [ ] 实现日历检查集成
- [ ] 添加用户通知机制
- [ ] 监控和报告仪表板

---

## 📋 手动命令

```bash
# 查看任务状态
python3 /root/.openclaw/workspace/scripts/task-manager.py status

# 手动执行启动检查
python3 /root/.openclaw/workspace/scripts/task-manager.py startup

# 手动执行健康检查
python3 /root/.openclaw/workspace/scripts/task-manager.py health

# 手动清理
/root/.openclaw/workspace/scripts/cleanup.sh

# 查看清理日志
cat /root/.openclaw/workspace/memory/cleanup.log

# 查看任务日志
cat /root/.openclaw/workspace/memory/task-logs.json
```

---

## 🎯 最佳实践

### 用户侧
1. 重要信息明确说"记住 X"
2. 定期查看 MEMORY.md 确认记录
3. 每周审查任务日志

### 系统侧
1. 启动时自动补偿检查
2. 任务失败自动重试（最多 3 次）
3. 日志文件自动轮转
4. 工作区大小监控

---

**最后更新：** 2026-03-04  
**维护者：** memory-manager 技能
