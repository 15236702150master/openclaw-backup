#!/bin/bash
# 测试 DingTalk 定时提醒

echo "=== 测试 DingTalk 定时提醒 ==="
echo ""

# 删除旧任务
openclaw cron rm "测试 DingTalk" 2>/dev/null

# 创建 1 分钟后的任务
echo "创建 1 分钟后的提醒任务..."
openclaw cron add \
  --name "测试 DingTalk" \
  --at "1m" \
  --session isolated \
  --message "💧 测试提醒：这是 DingTalk 定时提醒测试！" \
  --deliver \
  --channel dingtalk \
  --delete-after-run

echo ""
echo "任务已创建，等待 1 分钟..."
echo ""

# 等待 70 秒
sleep 70

# 检查执行历史
echo "检查执行历史..."
openclaw cron runs --id "$(openclaw cron list --json | python3 -c "import sys,json; jobs=json.load(sys.stdin)['jobs']; print(jobs[0]['id']) if jobs else print('none')" 2>/dev/null)" 2>&1 | tail -20

echo ""
echo "=== 测试完成 ==="
