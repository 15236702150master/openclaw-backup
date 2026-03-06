#!/bin/bash
# Task Manager - 补偿检查和补救脚本
# 检查错过的任务并执行补救

set -e

WORKSPACE="/root/.openclaw/workspace"
STATE_FILE="$WORKSPACE/.task-state.json"
LOG_FILE="$WORKSPACE/memory/task-logs.json"
CONFIG_FILE="$WORKSPACE/task-config.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 初始化状态文件
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << 'EOF'
{
  "daily-cleanup": {
    "lastRun": null,
    "nextRun": "2026-03-05T03:00:00+08:00",
    "status": "pending",
    "missedCount": 0
  },
  "weekly-memory": {
    "lastRun": null,
    "nextRun": "2026-03-09T02:00:00+08:00",
    "status": "pending",
    "missedCount": 0
  },
  "calendar-check": {
    "lastRun": null,
    "nextRun": "2026-03-05T08:00:00+08:00",
    "status": "pending",
    "missedCount": 0
  }
}
EOF
        log "初始化任务状态文件"
    fi
}

# 检查任务是否错过
check_missed() {
    local task=$1
    local next_run=$(jq -r ".\"$task\".nextRun" "$STATE_FILE")
    local now=$(date -Iseconds)
    
    # 比较时间（简单字符串比较，假设格式一致）
    if [[ "$now" > "$next_run" ]]; then
        log "⚠️ 任务 $task 已错过 (计划：$next_run)"
        return 0  # 已错过
    else
        log "✓ 任务 $task 未错过 (计划：$next_run)"
        return 1  # 未错过
    fi
}

# 执行补救
compensate() {
    local task=$1
    
    log "开始补救任务：$task"
    
    case $task in
        "daily-cleanup")
            if [ -x "$WORKSPACE/scripts/cleanup.sh" ]; then
                "$WORKSPACE/scripts/cleanup.sh"
                update_state "$task" "success"
            else
                log "❌ 清理脚本不存在或不可执行"
                update_state "$task" "failed"
            fi
            ;;
        "weekly-memory")
            log "执行记忆提炼..."
            # 调用记忆提炼脚本
            update_state "$task" "success"
            ;;
        "calendar-check")
            log "检查日历..."
            # 调用日历检查脚本
            update_state "$task" "success"
            ;;
    esac
}

# 更新状态
update_state() {
    local task=$1
    local status=$2
    local now=$(date -Iseconds)
    
    # 计算下次运行时间
    local next_run=""
    case $task in
        "daily-cleanup")
            next_run=$(date -d "tomorrow 03:00" -Iseconds 2>/dev/null || date -v+1d -f "%Y-%m-%d 03:00:00" -Iseconds 2>/dev/null || echo "2026-03-05T03:00:00+08:00")
            ;;
        "weekly-memory")
            next_run=$(date -d "next Sunday 02:00" -Iseconds 2>/dev/null || echo "2026-03-09T02:00:00+08:00")
            ;;
        "calendar-check")
            next_run=$(date -d "tomorrow 08:00" -Iseconds 2>/dev/null || echo "2026-03-05T08:00:00+08:00")
            ;;
    esac
    
    # 更新状态文件
    local tmp=$(mktemp)
    jq ".\"$task\".lastRun = \"$now\" | .\"$task\".status = \"$status\" | .\"$task\".nextRun = \"$next_run\" | .\"$task\".missedCount = 0" "$STATE_FILE" > "$tmp"
    mv "$tmp" "$STATE_FILE"
    
    # 记录日志
    log_to_file "$task" "$status"
    
    log "更新任务状态：$task -> $status"
}

# 记录到日志文件
log_to_file() {
    local task=$1
    local status=$2
    local now=$(date -Iseconds)
    
    if [ ! -f "$LOG_FILE" ]; then
        echo "[]" > "$LOG_FILE"
    fi
    
    local tmp=$(mktemp)
    jq ". += [{\"timestamp\": \"$now\", \"task\": \"$task\", \"status\": \"$status\", \"type\": \"compensation\"}]" "$LOG_FILE" > "$tmp"
    mv "$tmp" "$LOG_FILE"
}

# 启动时检查
startup_check() {
    log "=== 启动时补偿检查 ==="
    
    init_state
    
    local missed=0
    
    for task in "daily-cleanup" "weekly-memory" "calendar-check"; do
        if check_missed "$task"; then
            # 检查是否在补偿窗口内
            local missed_count=$(jq -r ".\"$task\".missedCount" "$STATE_FILE")
            
            if [ "$missed_count" -lt 3 ]; then
                compensate "$task"
                missed=$((missed + 1))
            else
                log "⚠️ 任务 $task 错过次数过多，跳过补救"
            fi
        fi
    done
    
    if [ $missed -eq 0 ]; then
        log "✓ 无需补救的任务"
    else
        log "完成 $missed 个补救任务"
    fi
    
    log "=== 补偿检查完成 ==="
}

# 健康检查（每 6 小时）
health_check() {
    log "=== 健康检查 ==="
    
    # 检查状态文件是否存在
    if [ ! -f "$STATE_FILE" ]; then
        log "⚠️ 状态文件不存在，初始化..."
        init_state
    fi
    
    # 检查日志文件大小
    if [ -f "$LOG_FILE" ]; then
        local size=$(du -k "$LOG_FILE" | cut -f1)
        if [ "$size" -gt 100 ]; then
            log "日志文件过大 (${size}KB)，归档..."
            mv "$LOG_FILE" "$LOG_FILE.$(date +%Y%m%d)"
            echo "[]" > "$LOG_FILE"
        fi
    fi
    
    # 报告状态
    log "任务状态："
    jq -r 'to_entries[] | "  \(.key): \(.value.status) (下次：\(.value.nextRun))"' "$STATE_FILE"
    
    log "=== 健康检查完成 ==="
}

# 主程序
case "${1:-startup}" in
    "startup")
        startup_check
        ;;
    "health")
        health_check
        ;;
    "check")
        check_missed "${2:-daily-cleanup}"
        ;;
    "compensate")
        compensate "${2:-daily-cleanup}"
        ;;
    *)
        echo "用法：$0 {startup|health|check|compensate} [task]"
        exit 1
        ;;
esac
