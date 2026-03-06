# 微信公众号文章读取工具调研

## ✅ 已找到解决方案！

**服务：** https://wechat.imagenie.us

**使用方法：**
```bash
curl -X POST "https://wechat.imagenie.us/extract" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/xxxxx"}'
```

**状态：** ✅ 已验证可用（2026-03-05）

---

## 📋 调研结果

### 已发现的微信相关技能

| 技能名称 | 用途 | 安装量 | 相关性 |
|----------|------|--------|--------|
| `wechat-article-writer` | 写微信公众号文章 | 560 | ⭐⭐ 写文章 |
| `baoyu-post-to-wechat` | 发布内容到微信 | 5.9K | ⭐⭐ 发布 |
| `auth-wechat-miniprogram` | 微信小程序认证 | 417 | ⭐ 小程序 |
| `notion-to-weixin` | Notion 转微信格式 | 18 | ⭐ 格式转换 |
| `auto-weixin-video` | 微信视频号自动化 | 8 | ⭐ 视频号 |

**结论：** ⚠️ **技能库中没有，但发现了第三方服务**

---

## 🔍 为什么无法自动读取

### 技术限制

1. **登录认证**
   - 微信公众号文章需要微信登录
   - 部分文章仅粉丝可见
   - 有访问频率限制

2. **反爬机制**
   - JavaScript 动态渲染
   - 内容分块加载
   - IP 访问限制
   - User-Agent 检测

3. **内容加密**
   - 部分链接有时效性
   - 需要微信客户端
   - 有防盗链机制

---

## 💡 可行方案对比

### 方案 1: 微信官方 API ⭐⭐⭐

**前提：** 需要公众号管理员权限

```python
# 微信公众号 API
# https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html

# 获取文章列表
access_token = get_access_token(appid, secret)
articles = get_article_list(access_token)
```

**优点：**
- ✅ 官方支持
- ✅ 稳定可靠
- ✅ 完整内容

**缺点：**
- ❌ 需要公众号管理员权限
- ❌ 只能获取自己公众号的文章
- ❌ 需要申请开发者资质

---

### 方案 2: 浏览器自动化 ⭐⭐

**工具：** Puppeteer / Playwright

```python
from playwright.sync_api import sync_playwright

def fetch_wechat_article(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 需要微信扫码登录
        page.goto(url)
        page.wait_for_load_state()
        
        content = page.content()
        return content
```

**优点：**
- ✅ 可以访问任意公众号
- ✅ 获取完整内容

**缺点：**
- ❌ 需要微信扫码登录
- ❌ 每次登录有冷却时间
- ❌ 可能被检测为爬虫

---

### 方案 3: 第三方 API 服务 ⭐⭐

**服务示例：**
- https://www.tophub.today (已失效)
- https://wechat.js.org (社区项目)
- 各种付费 API

**优点：**
- ✅ 无需自己维护
- ✅ 简单易用

**缺点：**
- ❌ 稳定性差
- ❌ 可能收费
- ❌ 有隐私风险

---

### 方案 4: RSS 订阅 ⭐⭐⭐

**工具：**
- 微信读书 RSS
- 公众号 RSS 生成器

**示例：**
```
https://rsshub.app/wechat/mp/...
```

**优点：**
- ✅ 标准化协议
- ✅ 易于集成

**缺点：**
- ❌ 很多公众号不支持
- ❌ 内容可能不完整
- ❌ RSSHub 可能不稳定

---

### 方案 5: 手动保存 ⭐⭐⭐⭐⭐

**方法：**
1. 微信中打开文章
2. 复制全文
3. 粘贴到本地文件
4. 或使用"收藏"功能

**优点：**
- ✅ 100% 可靠
- ✅ 无技术门槛
- ✅ 最完整

**缺点：**
- ❌ 需要手动操作
- ❌ 不适合批量

---

## 🎯 推荐方案

### 最佳实践：**手动 + 自动化结合**

```
1. 用户分享链接 → OpenClaw 接收
   ↓
2. 创建备份框架（自动）
   ↓
3. 用户在微信中打开 → 复制内容
   ↓
4. 粘贴到备份文件（或告诉我，我帮你记录）
   ↓
5. Git 提交备份（可选）
```

### 工作流程

**对于重要文章：**
```
1. 微信收藏（最可靠）
2. 截图关键内容
3. 告诉我核心观点，我帮你记录到 MEMORY.md
```

**对于一般文章：**
```
1. 保存链接到待读列表
2. 有时间再阅读
3. 需要时再备份
```

---

## 📝 替代方案：使用 OpenClaw 记忆

**与其备份全文，不如：**

```
1. 阅读文章
2. 告诉我核心观点
3. 我记录到 MEMORY.md
4. 随时可以检索
```

**示例：**
```
你：这篇文章讲了 OpenClaw 稳定性的两个方法
我：好的，已记录到 MEMORY.md

## 学习笔记：OpenClaw 稳定性
- 方法 1: [内容]
- 方法 2: [内容]
- 来源：老里的 AI 实验室
- 日期：2026-03-05
```

**优点：**
- ✅ 节省空间
- ✅ 易于检索
- ✅ 内化为知识
- ✅ 不需要完整备份

---

## 🔧 技术实现建议

### 如果一定要自动读取

**最佳方案：浏览器扩展 + API**

```javascript
// 浏览器扩展代码
// 在微信中运行时自动保存

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "saveArticle") {
        const content = document.querySelector('.rich_media_content');
        const title = document.querySelector('.rich_media_title');
        
        fetch('http://localhost:18789/api/save', {
            method: 'POST',
            body: JSON.stringify({ title, content })
        });
    }
});
```

**复杂度：** ⭐⭐⭐⭐⭐
**稳定性：** ⭐⭐⭐
**推荐度：** ⭐⭐

---

## 📊 方案对比总结

| 方案 | 难度 | 成本 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|
| 微信官方 API | ⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 浏览器自动化 | ⭐⭐⭐⭐ | 免费 | ⭐⭐ | ⭐⭐ |
| 第三方 API | ⭐ | 付费 | ⭐⭐ | ⭐⭐ |
| RSS 订阅 | ⭐⭐ | 免费 | ⭐⭐⭐ | ⭐⭐⭐ |
| **手动保存** | ⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **记忆记录** | ⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 💡 我的建议

**对于微信公众号文章：**

1. **不要尝试自动抓取** - 技术限制太多，不稳定
2. **使用微信收藏** - 最可靠，随时可查看
3. **记录核心观点** - 告诉我，我帮你记录到记忆
4. **需要时再查找** - 微信搜索很方便

**对于重要内容：**
```
阅读 → 理解 → 记录要点 → 内化知识
```

**比完整备份更有价值！**

---

**结论：** ❌ **目前没有可靠的技能或工具能自动读取微信公众号全文**

**最佳方案：** ✅ **手动阅读 + 记录要点到 OpenClaw 记忆**

---

**最后更新**: 2026-03-05  
**状态**: ❌ 无自动读取方案  
**推荐**: 手动阅读 + 记忆记录
