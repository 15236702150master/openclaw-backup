# 社交媒体备份系统

## 📋 系统说明

自动备份 Twitter/X、微博等社交媒体内容到本地。

---

## 🗂️ 备份目录结构

```
/root/.openclaw/workspace/backups/
├── social-media/          # 社交媒体备份
│   ├── x-twitter/        # Twitter/X
│   ├── weibo/            # 微博
│   └── other/            # 其他平台
├── web-pages/            # 网页备份
└── documents/            # 文档备份
```

---

## 🔧 备份方法

### 方法 1: 直接保存（当前使用）⭐

**适用场景：**
- 用户分享链接
- 创建备份框架
- 手动补充内容

**操作：**
```bash
# 创建备份文件
cat > /root/.openclaw/workspace/backups/social-media/x-xxx.md << 'EOF'
# 备份内容
[用户补充]
EOF
```

### 方法 2: Twitter API（需要配置）⭐⭐⭐

**前提条件：**
- Twitter API v2 密钥
- Bearer Token

**配置：**
```bash
# 添加到环境变量
export TWITTER_BEARER_TOKEN="your-token-here"
```

**脚本：**
```python
#!/usr/bin/env python3
import requests
import json

def backup_tweet(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {
        "expansions": "author_id,attachments.media_keys",
        "tweet.fields": "created_at,public_metrics,context_annotations"
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # 保存到文件
    with open(f"backups/x-{tweet_id}.md", 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data
```

### 方法 3: 浏览器扩展（推荐）⭐⭐

**推荐工具：**
- **SingleFile** - 保存完整网页
- **Save Page WE** - 保存为 HTML
- **Twitter Archive** - 专门备份 Twitter

**使用流程：**
1. 安装浏览器扩展
2. 打开推文链接
3. 点击扩展按钮保存
4. 移动到备份目录

### 方法 4: 第三方服务 ⭐⭐

**在线工具：**
- https://threadreaderapp.com - 保存 Twitter 线程
- https://twishort.com - 推文截图和备份
- https://archive.org/web/ - 网页存档

**使用示例：**
```
原始链接：https://x.com/user/status/123
ThreadReader: https://threadreaderapp.com/thread/123.html
```

---

## 📝 备份模板

### Twitter/X 备份模板

```markdown
# Twitter/X 推文备份

## 原始信息

- **作者**: @username
- **链接**: [原始链接]
- **备份时间**: YYYY-MM-DD HH:mm
- **备份原因**: [说明]

## 推文内容

[复制推文文本]

## 媒体附件

- [ ] 图片 1: [保存路径]
- [ ] 图片 2: [保存路径]
- [ ] 视频：[保存路径]

## 互动数据

- **点赞数**: XXX
- **转发数**: XXX
- **回复数**: XXX
- **浏览数**: XXX（如果有）

## 相关推文（线程）

1. [链接 1]
2. [链接 2]
3. [链接 3]

## 备注

[其他说明]

---

**备份文件位置**: `/root/.openclaw/workspace/backups/social-media/x-xxx.md`
```

---

## 🚀 自动化脚本

### 创建备份脚本

```bash
#!/bin/bash
# backup-social.sh - 社交媒体备份脚本

BACKUP_DIR="/root/.openclaw/workspace/backups/social-media"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建目录
mkdir -p "$BACKUP_DIR"

# 从参数获取链接
URL="$1"

if [ -z "$URL" ]; then
    echo "用法：$0 <社交媒体链接>"
    exit 1
fi

# 提取平台
if [[ "$URL" == *"x.com"* ]] || [[ "$URL" == *"twitter.com"* ]]; then
    PLATFORM="x"
    TWEET_ID=$(echo "$URL" | grep -oP 'status/\K\d+')
    BACKUP_FILE="$BACKUP_DIR/x-${TWEET_ID}-${TIMESTAMP}.md"
elif [[ "$URL" == *"weibo.com"* ]]; then
    PLATFORM="weibo"
    BACKUP_FILE="$BACKUP_DIR/weibo-${TIMESTAMP}.md"
else
    PLATFORM="other"
    BACKUP_FILE="$BACKUP_DIR/other-${TIMESTAMP}.md"
fi

# 创建备份框架
cat > "$BACKUP_FILE" << EOF
# $PLATFORM 备份

## 原始信息
- **链接**: $URL
- **备份时间**: $(date '+%Y-%m-%d %H:%M')

## 内容
[待补充]

---
**备份文件**: $BACKUP_FILE
EOF

echo "✓ 备份框架已创建：$BACKUP_FILE"
echo "⚠️ 请手动补充内容"
```

### 使用示例

```bash
# 备份 Twitter
./backup-social.sh "https://x.com/user/status/123"

# 备份微博
./backup-social.sh "https://weibo.com/123/abc"
```

---

## 📊 备份统计

### 当前备份

| 平台 | 数量 | 最后备份 |
|------|------|----------|
| Twitter/X | 1 | 2026-03-05 10:17 |
| 微信公众号 | 1 | 2026-03-05 10:32 |
| 微博 | 0 | - |
| 其他 | 0 | - |

### 备份位置

```
/root/.openclaw/workspace/backups/social-media/
└── x-billtheinvestor-2026948732424802640.md (916 bytes)
```

---

## ⚠️ 当前限制

### 无法自动抓取的原因

1. **Twitter/X 认证要求**
   - 需要登录才能查看内容
   - web_fetch 无法通过认证

2. **反爬虫机制**
   - JavaScript 渲染
   - 动态加载内容
   - IP 限制

3. **API 限制**
   - 免费 API 有调用限制
   - 需要申请密钥

### 解决方案

| 方案 | 难度 | 成本 | 推荐度 |
|------|------|------|--------|
| 手动复制 | ⭐ | 免费 | ⭐⭐⭐ |
| 浏览器扩展 | ⭐⭐ | 免费 | ⭐⭐⭐ |
| Twitter API | ⭐⭐⭐ | 免费/$$$ | ⭐⭐ |
| 第三方服务 | ⭐ | 免费/$$$ | ⭐⭐ |

---

## 💡 最佳实践

### 推荐流程

```
1. 用户分享链接
   ↓
2. 创建备份框架（自动）
   ↓
3. 手动补充内容（或浏览器扩展）
   ↓
4. 保存到备份目录
   ↓
5. Git 提交备份（可选）
```

### 备份检查清单

- [ ] 保存推文文本
- [ ] 下载图片/视频
- [ ] 记录互动数据
- [ ] 保存相关线程
- [ ] 添加标签/分类
- [ ] Git 提交（可选）

---

## 🔗 相关资源

### 工具推荐

- **SingleFile**: https://github.com/gildas-lormeau/SingleFile
- **ThreadReader**: https://threadreaderapp.com
- **Twitter Archive**: https://github.com/mierak/twitter-archive

### 文档

- Twitter API: https://developer.twitter.com/en/docs
- 备份最佳实践：[待补充]

---

**最后更新**: 2026-03-05  
**状态**: ⚠️ 部分可用（需要手动补充）
