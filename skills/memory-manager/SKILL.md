---
name: memory-manager
description: Automatic memory management and cleanup system. Handles memory updates, log rotation, temp file cleanup, and token optimization. Runs on heartbeat to keep workspace clean and efficient.
---

# Memory Manager

自动记忆管理和清理系统，确保工作区保持整洁、高效，避免 token 浪费。

## 核心功能

### 1. 记忆更新策略

#### 自动触发时机

| 触发条件 | 频率 | 操作 |
|----------|------|------|
| 心跳检查 | 每 30 分钟 | 检查待办、更新状态 |
| 会话结束 | 用户 2 小时无响应 | 摘要对话到 memory/日志 |
| 重大变更 | 实时 | 技能安装/卸载、配置修改 |
| 明确指令 | 用户说"记住 X" | 立即写入 MEMORY.md |

#### 记忆提炼规则

```
memory/YYYY-MM-DD.md (原始日志)
         ↓ 每 7 天审查
    提炼重要内容
         ↓
MEMORY.md (长期记忆)
         ↓ 每 30 天审查
    删除过时信息
         ↓
更新 MEMORY.md
```

### 2. 文件清理策略

#### 临时文件清理

**目标目录：**
- `/tmp/openclaw-*`
- `/tmp/jiti/`
- `/tmp/node-compile-cache/`
- `~/.openclaw/workspace/.tmp/`
- `~/.openclaw/workspace/tmp/`
- `~/.openclaw/cache/`

**清理规则：**

| 文件类型 | 保留时间 | 操作 |
|----------|----------|------|
| `*.log` | 7 天 | 删除 |
| `*.tmp` | 1 天 | 删除 |
| `*.cache` | 7 天 | 删除 |
| `*.snapshot` | 3 天 | 删除 |
| 空目录 | 立即 | 删除 |
| 重复文件 | 立即 | 删除旧版本 |

#### 日志文件轮转

```
memory/2026-03-01.md  →  30 天后 →  压缩 → memory/archive/2026-03.zip
memory/2026-03-02.md  →  30 天后 →  压缩 → memory/archive/2026-03.zip
```

**规则：**
- 每日日志保留 30 天
- 超过 30 天 → 压缩归档
- 超过 90 天 → 删除归档

#### Markdown 文件管理

**检查项：**
1. 空的 `.md` 文件 → 删除
2. 只有标题无内容 → 标记审查
3. 重复内容 → 合并或删除
4. 过时的技能文档 → 归档

### 3. Token 优化

#### 上下文加载优化

**加载优先级：**
```
1. MEMORY.md (必须加载)
2. memory/最近 3 天 (相关时加载)
3. 其他文件 (按需加载)
```

**避免加载：**
- 超过 30 天的日志（除非明确提及）
- 临时文件
- 缓存文件
- 重复备份文件

#### 文件内容压缩

```markdown
# 优化前（浪费 token）
2026-03-01 09:00 用户说早上好
2026-03-01 09:05 用户问了天气
2026-03-01 09:10 用户让我找文件

# 优化后（节省 70% token）
2026-03-01: 早晨对话、天气查询、文件查找
```

## 自动化脚本

### 心跳检查脚本

```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/memory-cleanup.sh

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
TMP_DIRS=("/tmp/openclaw-*" "/tmp/jiti" "/tmp/node-compile-cache")

# 1. 清理临时文件（>24 小时）
for dir in "${TMP_DIRS[@]}"; do
    find $dir -type f -mtime +1 -delete 2>/dev/null
done

# 2. 日志轮转（>30 天）
find $MEMORY_DIR -name "*.md" -mtime +30 -exec mv {} $ARCHIVE_DIR/ \;

# 3. 压缩归档（>90 天）
find $ARCHIVE_DIR -name "*.md" -mtime +90 -delete

# 4. 删除空文件
find $WORKSPACE -name "*.md" -empty -delete

# 5. 生成报告
echo "Cleanup completed at $(date)"
echo "Temp files removed: $(find /tmp -name 'openclaw*' -mmin +1440 | wc -l)"
echo "Old logs archived: $(find $MEMORY_DIR -mtime +30 | wc -l)"
```

### 记忆提炼脚本

```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/memory-summarize.sh

MEMORY_FILE="/root/.openclaw/workspace/MEMORY.md"
LOG_DIR="/root/.openclaw/workspace/memory"

# 读取最近 7 天的日志
WEEK_LOGS=$(find $LOG_DIR -name "*.md" -mtime -7 -exec cat {} \;)

# 提取关键信息（技能变更、配置修改、重要决定）
IMPORTANT=$(echo "$WEEK_LOGS" | grep -E "(安装 | 卸载 | 配置 | 决定|重要)")

# 更新 MEMORY.md
if [ ! -z "$IMPORTANT" ]; then
    echo "## $(date +%Y-%m-%d) 更新" >> $MEMORY_FILE
    echo "$IMPORTANT" >> $MEMORY_FILE
fi
```

## 执行计划

### 每次心跳检查时

```
1. 检查 /tmp 目录大小
   ├─ 如果 >500MB → 清理旧文件
   └─ 报告清理结果

2. 检查 memory/ 目录
   ├─ 归档>30 天的日志
   ├─ 删除>90 天的归档
   └─ 提炼重要内容到 MEMORY.md

3. 检查工作区文件
   ├─ 删除空的 .md 文件
   ├─ 标记重复文件
   └─ 报告空间使用

4. 更新记忆状态
   ├─ 记录本次清理结果
   └─ 更新最后清理时间
```

### 每周日执行深度清理

```
1. 扫描整个工作区
2. 识别大文件（>10MB）
3. 识别重复文件
4. 生成清理建议
5. 用户确认后执行
```

## 监控指标

### 健康检查清单

| 指标 | 健康值 | 警告值 | 危险值 |
|------|--------|--------|--------|
| 工作区总大小 | <100MB | <500MB | >500MB |
| 临时文件大小 | <50MB | <200MB | >200MB |
| memory/文件数 | <50 | <200 | >200 |
| MEMORY.md 大小 | <50KB | <200KB | >200KB |
| 日志文件平均大小 | <10KB | <50KB | >50KB |

### 自动报告

每次心跳检查后报告：

```
🧹 记忆系统健康检查

工作区：45.2 MB (健康 ✓)
临时文件：12.3 MB (健康 ✓)
日志文件：23 个 (健康 ✓)
MEMORY.md: 8.5 KB (健康 ✓)

本次清理：
- 删除临时文件：15 个 (3.2 MB)
- 归档日志：2 个
- 节省 token 估算：~2000

下次深度清理：周日 02:00
```

## 用户命令

### 手动触发清理

```bash
# 快速清理（临时文件）
openclaw memory cleanup --quick

# 完整清理（包括日志轮转）
openclaw memory cleanup --full

# 查看状态
openclaw memory status

# 预览将删除的文件
openclaw memory cleanup --dry-run
```

### 手动更新记忆

```bash
# 记录重要信息
openclaw memory add "用户偏好：使用 VSCode 编辑代码"

# 删除过时信息
openclaw memory remove "旧项目名称"

# 查看记忆
openclaw memory list
```

## 配置文件

### ~/.openclaw/memory-config.json

```json
{
  "cleanup": {
    "tempFileMaxAge": "1d",
    "logFileMaxAge": "30d",
    "archiveMaxAge": "90d",
    "maxWorkspaceSize": "500MB",
    "maxTempSize": "200MB"
  },
  "memory": {
    "summarizeInterval": "7d",
    "maxMemorySize": "200KB",
    "autoSummarize": true
  },
  "token": {
    "maxContextFiles": 10,
    "excludePatterns": ["*.tmp", "*.cache", "*.log"],
    "priorityFiles": ["MEMORY.md", "SOUL.md", "USER.md"]
  },
  "schedule": {
    "quickCleanup": "daily 03:00",
    "deepCleanup": "weekly Sunday 02:00",
    "healthCheck": "every 30m"
  }
}
```

## 错误处理

### 清理失败

```
如果清理脚本失败：
1. 记录错误到 memory/cleanup-errors.log
2. 通知用户清理失败
3. 建议手动执行
4. 下次心跳重试
```

### 文件占用

```
如果文件被占用无法删除：
1. 跳过该文件
2. 记录到待清理列表
3. 下次重启后重试
```

## 相关技能

- **heartbeat-manager**: 管理心跳检查计划
- **workspace-optimizer**: 工作区空间优化
- **token-saver**: Token 使用优化

---

**激活方式**: 添加到 HEARTBEAT.md 自动执行，或手动运行 `openclaw memory cleanup`
