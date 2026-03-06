# OpenClaw 备份策略

**最后更新**: 2026-03-06  
**目标**: 确保所有记忆、配置、代码安全，支持快速恢复

---

## 📋 备份内容

### 核心记忆文件 ⭐⭐⭐
- `MEMORY.md` - 长期记忆
- `XIAOYU-DIARY.md` - 成长日记
- `MEMORY-HABIT.md` - 记忆习惯规范
- `memory/` - 每日日志和待办
- `API-KEYS.md` - API 密钥配置

### 配置文件 ⭐⭐
- `openclaw.json` - OpenClaw 配置
- `cron-jobs.json` - 定时任务
- `cron-jobs-reminder.json` - 提醒配置
- `task-config.json` - 任务配置

### 技能和脚本 ⭐⭐
- `skills/` - 所有技能
- `scripts/` - 自动化脚本
- `docs/` - 文档

### 项目文件 ⭐
- `TuriX-CUA/` - TuriX 项目
- `agents/` - Agent 配置

---

## ⏰ 备份频率

| 类型 | 频率 | 说明 |
|------|------|------|
| **自动备份** | 每小时 | 有改动自动提交到 GitHub |
| **手动备份** | 随时 | 完成重要任务后立即备份 |
| **完整备份** | 每天 23:00 | 每日摘要时一起备份 |

---

## 🚀 备份命令

### 手动触发备份

```bash
cd /root/.openclaw/workspace
./scripts/auto-github-backup.sh
```

### 检查备份状态

```bash
# 查看 Git 状态
git status

# 查看最近的备份
git log --oneline -10

# 查看备份历史
cat memory/backups/backup-history.log
```

### 恢复文件

```bash
# 查看历史版本
git log MEMORY.md

# 恢复到特定版本
git checkout <commit-hash> -- MEMORY.md

# 回滚所有文件到上次备份
git reset --hard HEAD~1
```

---

## 📊 备份监控

### 检查清单

每天检查：
- [ ] 自动备份是否正常运行
- [ ] 备份历史日志是否更新
- [ ] GitHub 仓库是否同步

每周检查：
- [ ] 备份文件大小是否合理
- [ ] 是否有敏感信息被提交
- [ ] 测试恢复流程

### 备份日志

位置：`memory/backups/backup-history.log`

格式：
```
2026-03-06 21:00:00 - 备份成功 (改动：5 文件)
2026-03-06 22:00:00 - 备份成功 (改动：12 文件)
```

---

## 🔒 安全注意事项

### 不要备份的内容

`.gitignore` 已配置：
- `*.log` - 日志文件
- `*.tmp` - 临时文件
- `node_modules/` - 依赖
- `*.pyc` - Python 缓存
- `.turix_tmp/` - TuriX 临时文件

### 敏感信息

- ✅ API 密钥已加密或脱敏
- ✅ 密码不直接提交（使用环境变量）
- ⚠️ 定期检查是否有敏感信息泄露

---

## 🎯 恢复流程

### 场景 1: 误删单个文件

```bash
# 从最近的备份恢复
git checkout HEAD -- MEMORY.md
```

### 场景 2: 回滚所有改动

```bash
# 放弃所有本地改动
git reset --hard HEAD

# 或者回滚到上一个版本
git reset --hard HEAD~1
```

### 场景 3: 完全恢复（灾难恢复）

```bash
# 1. 克隆备份仓库
git clone https://github.com/15236702150master/openclaw-backup.git /tmp/restore

# 2. 复制重要文件
cp -r /tmp/restore/* /root/.openclaw/workspace/

# 3. 验证恢复
cd /root/.openclaw/workspace
git status
```

---

## 📈 备份统计

### 仓库信息

- **仓库地址**: https://github.com/15236702150master/openclaw-backup
- **分支**: master
- **自动备份**: ✅ 每小时
- **最后备份**: 检查 `git log -1`

### 存储优化

- 使用 Git LFS 存储大文件（如果需要）
- 定期清理无用的大文件
- 压缩日志文件

---

## 💡 最佳实践

### 备份习惯

1. **完成重要任务后** → 立即手动备份
2. **修改配置文件后** → 检查是否自动备份
3. **每天结束时** → 确认备份正常

### 提交信息规范

```
Auto-backup 2026-03-06 21:00 [自动备份]

改动统计:
- 修改文件：5 个
- 备份时间：2026-03-06 21:00:00

重要文件:
  ✓ MEMORY.md
  ✓ XIAOYU-DIARY.md
```

### 监控告警

如果备份失败：
1. 检查网络连接
2. 检查 GitHub 凭证
3. 检查磁盘空间
4. 手动执行备份脚本

---

## 🔗 相关文档

- `/root/.openclaw/workspace/scripts/auto-github-backup.sh` - 备份脚本
- `/root/.openclaw/workspace/memory/backups/backup-history.log` - 备份历史
- `/root/.openclaw/workspace/.github-credentials.sh` - GitHub 凭证

---

**BOSS 的提醒**: 
> "备份记忆和记录记忆同样重要，谁也不知道你会不会有时候错误删除文件导致无法回滚文件"

**小宇的承诺**: 
> 每小时自动备份，确保记忆安全！
> 每次重要更新后立即手动备份！
> 定期检查备份完整性！

---
*创建时间：2026-03-06 21:10*  
*小宇* 🤖
