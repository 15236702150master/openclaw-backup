#!/bin/bash
# 微信公众号文章备份工具
# 使用 wechat.imagenie.us 服务读取并保存文章

BACKUP_DIR="/root/.openclaw/workspace/backups/wechat"
mkdir -p "$BACKUP_DIR"

if [ -z "$1" ]; then
    echo "用法：$0 <微信公众号文章链接>"
    echo ""
    echo "示例:"
    echo "  $0 https://mp.weixin.qq.com/s/xxxxx"
    exit 1
fi

URL="$1"
ARTICLE_ID=$(echo "$URL" | grep -oP 's/\K[a-zA-Z0-9_-]+')
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$BACKUP_DIR/wechat-${ARTICLE_ID}.md"

echo "📖 正在读取文章..."
echo "链接：$URL"
echo ""

# 调用 API 获取文章
curl -s -X POST "https://wechat.imagenie.us/extract" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$URL\"}" \
  -o "$OUTPUT_FILE"

if [ $? -eq 0 ] && [ -s "$OUTPUT_FILE" ]; then
    echo "✅ 备份成功！"
    echo ""
    echo "文件位置：$OUTPUT_FILE"
    echo "文件大小：$(wc -c < "$OUTPUT_FILE") bytes"
    echo "行数：$(wc -l < "$OUTPUT_FILE") 行"
    echo ""
    echo "=== 文章标题 ==="
    head -1 "$OUTPUT_FILE"
else
    echo "❌ 备份失败"
    echo "请检查链接是否正确，或稍后重试"
    rm -f "$OUTPUT_FILE"
    exit 1
fi
