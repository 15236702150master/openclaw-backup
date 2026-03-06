#!/bin/bash
# 检查语义搜索依赖是否安装完成
# 用法：./check-semantic-search.sh [--notify]

NOTIFY=false
if [ "$1" == "--notify" ]; then
    NOTIFY=true
fi

echo "🔍 检查语义搜索依赖..."

# 检查 Python 依赖
python3 -c "
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    print('✅ 所有依赖已安装')
    exit(0)
except ImportError as e:
    print(f'⏳ 依赖未完全安装：{e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 语义搜索依赖安装完成！"
    
    if [ "$NOTIFY" = true ]; then
        echo ""
        echo "📤 发送通知..."
        cd ~/.openclaw/workspace
        
        # 尝试使用 OpenClaw 消息系统发送提醒
        # 注意：需要正确的 target 格式，由主代理处理
        echo "请主代理发送消息：✅ 语义搜索已安装完成！现在可以使用语义搜索功能了"
    fi
    
    exit 0
else
    echo ""
    echo "⏳ 语义搜索依赖仍在安装中..."
    exit 1
fi
