#!/bin/bash
# TuriX-CUA Linux 适配版运行脚本
# 支持动态任务注入、恢复、Skills 系统和规划

set -e

# ---------- 配置 ----------
PROJECT_DIR="/root/.openclaw/workspace/TuriX-CUA"
CONFIG_FILE="$PROJECT_DIR/examples/config.json"
CONDA_PATH="/opt/anaconda3/bin/conda"
ENV_NAME="turix_env"

# Linux 特定 PATH
export PATH="/usr/sbin:/usr/bin:/bin:/sbin:$PATH"
export DISPLAY=:0  # X11 显示

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---------- 帮助信息 ----------
show_help() {
    cat << EOF
用法：run_turix_linux.sh [选项] [任务]

选项:
    -r, --resume ID     恢复指定 agent_id 的任务
    -c, --config FILE   使用自定义配置文件
    -h, --help          显示帮助
    --no-plan           禁用规划（同时禁用 skills）
    --enable-skills     启用 skills（需要 --enable-plan）
    --dry-run           只显示命令不执行

示例:
    ./run_turix_linux.sh "打开 Chrome 访问 github.com"
    ./run_turix_linux.sh --enable-skills --resume my-task "继续任务"
EOF
}

# ---------- 参数解析 ----------
RESUME_ID=""
CUSTOM_CONFIG=""
DRY_RUN=false
USE_PLAN=true
USE_SKILLS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--resume)
            RESUME_ID="$2"
            shift 2
            ;;
        -c|--config)
            CUSTOM_CONFIG="$2"
            shift 2
            ;;
        --no-plan)
            USE_PLAN=false
            USE_SKILLS=false
            shift
            ;;
        --enable-skills)
            USE_SKILLS=true
            USE_PLAN=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            TASK="$*"
            break
            ;;
    esac
done

# ---------- 预检查 ----------
log_info "🔍 TuriX-CUA Linux 预检查..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    log_error "Python3 未安装"
    exit 1
fi

# 检查 pyautogui 依赖
if ! python3 -c "import pyautogui" 2>/dev/null; then
    log_warn "pyautogui 未安装，尝试安装..."
    pip3 install pyautogui pynput
fi

# 检查 xdotool（Linux 窗口管理）
if ! command -v xdotool &> /dev/null; then
    log_warn "xdotool 未安装（可选，用于窗口管理）"
fi

# 检查配置文件
if [[ ! -f "$CONFIG_FILE" ]]; then
    log_error "配置文件不存在：$CONFIG_FILE"
    exit 1
fi

# ---------- 更新配置 ----------
if [[ -n "$TASK" ]]; then
    log_info "📝 更新任务配置..."
    python3 << PYTHON_EOF
import json

config_path = "$CONFIG_FILE"
task_text = '''$TASK'''

with open(config_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['agent']['task'] = task_text.strip()
data['agent']['use_plan'] = $( [[ "$USE_PLAN" == "true" ]] && echo "True" || echo "False" )
data['agent']['use_skills'] = $( [[ "$USE_SKILLS" == "true" ]] && echo "True" || echo "False" )

if [[ -n "$RESUME_ID" ]]; then
    data['agent']['resume'] = True
    data['agent']['agent_id'] = "$RESUME_ID"
else:
    data['agent']['resume'] = False
    data['agent']['agent_id'] = None

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ 配置已更新")
PYTHON_EOF
fi

# ---------- 显示命令 ----------
if [[ "$DRY_RUN" == "true" ]]; then
    log_info "📋 将要执行的命令:"
    echo "cd $PROJECT_DIR && python3 examples/main.py"
    exit 0
fi

# ---------- 运行 TuriX ----------
log_info "🚀 启动 TuriX-CUA Linux..."
log_info "📂 项目目录：$PROJECT_DIR"
log_info "📄 配置文件：$CONFIG_FILE"

if [[ -n "$TASK" ]]; then
    log_info "📝 任务：$TASK"
fi

if [[ -n "$RESUME_ID" ]]; then
    log_info "🔄 恢复任务 ID: $RESUME_ID"
fi

cd "$PROJECT_DIR"

# 检查屏幕截图权限（Linux）
if command -v scrot &> /dev/null; then
    log_info "📸 测试屏幕截图..."
    scrot /tmp/turix_test.png && rm /tmp/turix_test.png && log_info "✅ 截图权限正常"
fi

# 运行主程序
log_info "⏳ 首次运行可能需要 2-5 分钟加载 AI 模型..."
python3 examples/main.py

log_info "✅ TuriX-CUA 执行完成"
