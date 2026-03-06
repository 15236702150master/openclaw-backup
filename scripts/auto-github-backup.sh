#!/bin/bash
# OpenClaw 记忆和重要文件自动备份
# 每小时执行，有改动才推送

set -e

BACKUP_TIME=$(date '+%Y-%m-%d %H:%M:%S')
SHORT_TIME=$(date '+%Y-%m-%d %H:%M')

cd /root/.openclaw/workspace

# 加载凭证
if [ -f .github-credentials.sh ]; then
    source .github-credentials.sh
fi

echo "=========================================="
echo "🔄 OpenClaw 自动备份 - $BACKUP_TIME"
echo "=========================================="

# 1. 备份重要文件清单
echo "📋 备份重要文件..."
IMPORTANT_FILES=(
    "MEMORY.md"
    "XIAOYU-DIARY.md"
    "MEMORY-HABIT.md"
    "API-KEYS.md"
    "SCREENSHOT-CAPABILITIES.md"
    "memory/"
    "docs/"
    "scripts/"
    "skills/"
    "TuriX-CUA/"
)

# 2. 检查 Git 状态
git add -A
CHANGED=$(git diff --staged --name-only | wc -l)

if [ $CHANGED -eq 0 ]; then
    echo "✅ 无改动，跳过提交"
    echo "=========================================="
    exit 0
fi

echo "📝 检测到 $CHANGED 个文件改动:"
git diff --staged --name-only | head -20
[ $CHANGED -gt 20 ] && echo "... 等 $((CHANGED-20)) 个文件"

# 3. 创建提交
COMMIT_MSG="Auto-backup $SHORT_TIME [自动备份]

改动统计:
- 修改文件：$CHANGED 个
- 备份时间：$BACKUP_TIME

重要文件:
$(for f in "${IMPORTANT_FILES[@]}"; do git diff --staged --name-only | grep -q "^$f" && echo "  ✓ $f"; done)"

git commit -m "$COMMIT_MSG"

# 4. 推送到 GitHub
echo "🚀 推送到 GitHub..."
if git push origin master 2>&1 | tail -10; then
    echo "=========================================="
    echo "✅ 备份成功！$BACKUP_TIME"
    echo "=========================================="
else
    echo "=========================================="
    echo "⚠️  推送失败，下次重试"
    echo "=========================================="
    # 保留本地提交，不退出错误
fi

# 5. 创建备份日志
mkdir -p memory/backups
echo "$BACKUP_TIME - 备份成功 (改动：$CHANGED 文件)" >> memory/backups/backup-history.log
