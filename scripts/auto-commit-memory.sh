#!/bin/bash
# 记忆系统自动提交脚本
# 每天 23:30 执行

cd /root/.openclaw/workspace

# 源凭证
source .github-credentials.sh 2>/dev/null

# 添加变更
git add MEMORY.md 2>/dev/null
git add memory/semantic_index.json 2>/dev/null

# 检查是否有变更
if git diff --staged --quiet; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 无变更，跳过提交"
    exit 0
fi

# 提交
git commit -m "自动保存记忆更新 $(date '+%Y-%m-%d %H:%M')"

# 推送到 GitHub（可选）
# git push origin master

echo "$(date '+%Y-%m-%d %H:%M:%S') - ✓ 记忆已提交"
