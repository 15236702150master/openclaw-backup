#!/bin/bash
# Memory Manager - Quick Cleanup Script
# 清理临时文件、缓存、旧日志

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
LOG_FILE="$WORKSPACE/memory/cleanup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== 开始清理 ==="

# 1. 清理 /tmp 中的 OpenClaw 临时文件（>24 小时）
log "清理临时文件..."
TMP_COUNT=0
TMP_SIZE=0

for dir in /tmp/openclaw-* /tmp/jiti /tmp/node-compile-cache; do
    if [ -d "$dir" ]; then
        COUNT=$(find "$dir" -type f -mmin +1440 2>/dev/null | wc -l)
        SIZE=$(du -sb "$dir" 2>/dev/null | cut -f1)
        find "$dir" -type f -mmin +1440 -delete 2>/dev/null
        TMP_COUNT=$((TMP_COUNT + COUNT))
        TMP_SIZE=$((TMP_SIZE + SIZE))
    fi
done

log "删除临时文件：$TMP_COUNT 个 (~$((TMP_SIZE / 1024)) KB)"

# 2. 清理工作区临时文件
log "清理工作区临时文件..."
find "$WORKSPACE" -name "*.tmp" -mtime +1 -delete 2>/dev/null
find "$WORKSPACE" -name "*.cache" -mtime +7 -delete 2>/dev/null
find "$WORKSPACE" -name "*.log" -mtime +7 -delete 2>/dev/null

# 3. 归档旧日志（>30 天）
log "归档旧日志..."
mkdir -p "$ARCHIVE_DIR"
OLD_LOGS=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime +30 2>/dev/null | wc -l)

if [ "$OLD_LOGS" -gt 0 ]; then
    find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime +30 -exec mv {} "$ARCHIVE_DIR/" \;
    log "归档日志：$OLD_LOGS 个"
else
    log "无需归档的日志"
fi

# 4. 删除超期归档（>90 天）
log "清理超期归档..."
ARCHIVE_DEL=$(find "$ARCHIVE_DIR" -name "*.md" -mtime +90 2>/dev/null | wc -l)
find "$ARCHIVE_DIR" -name "*.md" -mtime +90 -delete 2>/dev/null
log "删除归档：$ARCHIVE_DEL 个"

# 5. 删除空文件
log "删除空文件..."
EMPTY_FILES=$(find "$WORKSPACE" -name "*.md" -empty 2>/dev/null | wc -l)
find "$WORKSPACE" -name "*.md" -empty -delete 2>/dev/null
log "删除空文件：$EMPTY_FILES 个"

# 6. 计算工作区大小
WORKSPACE_SIZE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)
log "工作区当前大小：$WORKSPACE_SIZE"

# 7. 生成报告
cat >> "$LOG_FILE" << EOF

=== 清理完成 ===
时间：$(date '+%Y-%m-%d %H:%M:%S')
临时文件：删除 $TMP_COUNT 个
归档日志：$OLD_LOGS 个
删除归档：$ARCHIVE_DEL 个
空文件：$EMPTY_FILES 个
工作区大小：$WORKSPACE_SIZE

EOF

log "=== 清理完成 ==="

# 输出摘要
echo ""
echo "🧹 清理完成摘要"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "临时文件：删除 $TMP_COUNT 个"
echo "归档日志：$OLD_LOGS 个"
echo "工作区大小：$WORKSPACE_SIZE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
