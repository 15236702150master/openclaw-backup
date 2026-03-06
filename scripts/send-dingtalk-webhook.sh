#!/bin/bash
# DingTalk 群机器人 Webhook 发送脚本

WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN"

# 发送消息
curl "$WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "'"$1"'"
    }
  }'

echo ""
echo "消息已发送：$1"
