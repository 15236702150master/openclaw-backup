#!/bin/bash
# 安装完成检查脚本

echo "🔍 检查安装进度..."
echo ""

# 检查核心包
echo "核心包状态:"
pip3 list 2>&1 | grep -iE "(sentence|transformers|torch|scikit)" | while read line; do
    echo "  ✓ $line"
done

echo ""
echo "测试语义搜索..."

# 快速测试
python3 -c "
from sentence_transformers import SentenceTransformer
print('加载模型...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('✓ 模型加载成功')

# 简单测试
embedding = model.encode('测试')
print(f'✓ 嵌入生成成功 (维度：{len(embedding)})')
" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有依赖安装完成！"
    echo ""
    echo "现在可以使用:"
    echo "  python3 /root/.openclaw/workspace/scripts/semantic-search.py search <查询>"
    echo "  python3 /root/.openclaw/workspace/scripts/semantic-search.py add <文本>"
    echo "  python3 /root/.openclaw/workspace/scripts/semantic-search.py stats"
else
    echo ""
    echo "⚠️ 测试失败，请检查安装"
fi
