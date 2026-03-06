#!/bin/bash
# memory-summarize.sh - 每周日 02:00 执行记忆提炼任务
# 功能：读取最近 7 天日志，提取重要信息，更新 MEMORY.md，归档旧日志

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
ARCHIVE_DIR="$MEMORY_DIR/archive"
LOG_FILE="$MEMORY_DIR/summarize.log"
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "=== 开始记忆提炼 ==="

# 1. 读取最近 7 天的日志文件
log "读取最近 7 天的日志..."
SEVEN_DAYS_AGO=$(date -d "7 days ago" +%Y-%m-%d)
RECENT_FILES=""

for file in "$MEMORY_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        # 提取日期部分 (YYYY-MM-DD.md)
        file_date="${filename%.md}"
        if [[ "$file_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            if [[ "$file_date" > "$SEVEN_DAYS_AGO" ]] || [[ "$file_date" == "$SEVEN_DAYS_AGO" ]]; then
                RECENT_FILES="$RECENT_FILES $file"
                log "  找到日志：$filename"
            fi
        fi
    fi
done

if [ -z "$RECENT_FILES" ]; then
    log "未发现最近 7 天的日志文件"
    log "=== 记忆提炼完成 (无新内容) ==="
    exit 0
fi

# 2. 提取重要信息
log "提取重要信息..."
TEMP_SUMMARY=$(mktemp)

# 提取关键模式
for file in $RECENT_FILES; do
    filename=$(basename "$file")
    
    # 技能变更
    grep -i "技能\|skill\|安装\|卸载\|配置" "$file" 2>/dev/null | while read -r line; do
        echo "[$filename] $line" >> "$TEMP_SUMMARY"
    done
    
    # 配置修改
    grep -i "配置\|config\|设置\|修改" "$file" 2>/dev/null | while read -r line; do
        echo "[$filename] $line" >> "$TEMP_SUMMARY"
    done
    
    # 重要决定
    grep -i "决定\|决策\|重要\|关键\|note\|decision" "$file" 2>/dev/null | while read -r line; do
        echo "[$filename] $line" >> "$TEMP_SUMMARY"
    done
done

if [ ! -s "$TEMP_SUMMARY" ]; then
    log "未提取到重要信息"
    rm -f "$TEMP_SUMMARY"
    log "=== 记忆提炼完成 (无重要内容) ==="
    exit 0
fi

# 3. 更新 MEMORY.md
log "更新 MEMORY.md..."

# 添加新的记忆条目
{
    echo ""
    echo "## 本周摘要 ($TODAY)"
    echo ""
    cat "$TEMP_SUMMARY"
    echo ""
} >> "$MEMORY_FILE"

rm -f "$TEMP_SUMMARY"
log "MEMORY.md 已更新"

# 4. 归档旧日志
log "归档旧日志..."
mkdir -p "$ARCHIVE_DIR"

for file in $RECENT_FILES; do
    filename=$(basename "$file")
    if [ -f "$file" ]; then
        # 移动到归档目录
        mv "$file" "$ARCHIVE_DIR/${filename%.md}-archived-$TODAY.md"
        log "  已归档：$filename"
    fi
done

log "=== 记忆提炼完成 ==="
log "处理文件数：$(echo $RECENT_FILES | wc -w)"
log "归档目录：$ARCHIVE_DIR"

exit 0
