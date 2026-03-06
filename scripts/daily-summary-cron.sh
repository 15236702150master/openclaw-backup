#!/bin/bash
# 每日摘要生成脚本
# 每天 23:00 执行

cd /root/.openclaw/workspace

echo "=== 生成每日摘要 ==="
echo "时间：$(date)"
echo ""

# 运行摘要脚本
python3 scripts/daily-summary-ai.py 2>&1

echo ""
echo "=== 摘要生成完成 ==="
