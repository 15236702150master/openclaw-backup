# 技能和插件安装流程

## 🎯 标准安装流程

```
用户请求安装技能/插件
         ↓
1️⃣ 搜索官方资源库（OpenClawDir/ClawHub）
         ↓
   找到？ → 安装并确认
         ↓
   没找到？
         ↓
2️⃣ 搜索 GitHub 和社区资源
         ↓
   找到？ → 安全审查 → 安装
         ↓
   没找到？ → 告知用户，建议替代方案
```

---

## 📋 详细步骤

### 步骤 1: 搜索官方资源库（必须）

**为什么优先官方：**
- ✅ 经过安全审核
- ✅ 质量保证
- ✅ 自动更新支持
- ✅ 社区评价参考

**搜索 ClawHub：**
```bash
# 搜索技能
clawhub search "[关键词]"

# 示例
clawhub search "pdf"
clawhub search "automation"
clawhub search "discord"
```

**搜索结果处理：**
```
找到多个技能时：
1. 列出前 5-10 个相关技能
2. 标注每个技能的用途
3. 显示评分（如果有）
4. 让用户选择或询问详细信息

示例输出：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
我在 ClawHub 找到了以下技能：

① nano-pdf - PDF 编辑和处理 ⭐4.5
② pdf-analyzer - PDF 内容分析 ⭐4.2
③ pdf-converter - PDF 格式转换 ⭐4.0
④ pdf-merger - PDF 合并分割 ⭐3.9
⑤ pdf-ocr - PDF 文字识别 ⭐4.3

要安装哪个？或者需要我详细介绍某个技能？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 步骤 2: 搜索 GitHub（官方没有时）

**什么时候搜索 GitHub：**
- ❌ ClawHub 没有找到相关技能
- ❌ 官方技能不符合需求
- ✅ 用户明确指定 GitHub 仓库

**搜索方式：**
```bash
# 使用 web_search 工具（如果有 API key）
web_search --query "openclaw skills pdf github"

# 使用 browser 工具浏览 GitHub
browser navigate "https://github.com/search?q=openclaw+skills"

# 或者直接访问已知资源
web_fetch "https://github.com/vercel-labs/skills"
```

**安全审查清单：**
```
安装前必须检查：
□ 仓库活跃度（最近更新时间）
□ Star 数量和 Fork 数
□ Issues 和 PR 情况
□ SKILL.md 内容审查
□ 脚本文件是否有可疑代码
□ 权限要求是否合理
□ 社区评价和反馈

可疑信号（不要安装）：
❌ 要求过多权限
❌ 包含加密密钥或 API 密钥
❌ 使用 eval 或类似危险函数
❌ 连接到不明外部服务
❌ 没有明确的用途说明
```

### 步骤 3: 安装技能

**从 ClawHub 安装：**
```bash
clawhub install <skill-slug>

# 示例
clawhub install nano-pdf
```

**从 GitHub 安装：**
```bash
# 方法 1: npx skills
npx skills add https://github.com/owner/repo --skill skill-name

# 方法 2: auto-install-skill（克隆失败时 fallback）
自动从 raw GitHub URL 抓取文件创建
```

**安装插件：**
```bash
openclaw plugins install <plugin-name>

# 示例
openclaw plugins install @openclaw-china/dingtalk
```

### 步骤 4: 验证和记录

**验证安装：**
```bash
# 检查技能是否就绪
openclaw skills list | grep <skill-name>

# 测试技能功能
<根据技能类型测试基本功能>
```

**记录到 MEMORY.md：**
```markdown
## 技能安装记录
- 技能名称：nano-pdf
- 安装时间：2026-03-04
- 来源：ClawHub
- 用途：PDF 编辑和处理
- 测试状态：✓ 正常
```

---

## 🛡️ 安全规范

### 官方资源库技能

| 检查项 | 要求 |
|--------|------|
| 来源验证 | ✅ ClawHub/OpenClawDir 官方 |
| 安全审核 | ✅ 平台已审核 |
| 代码审查 | ⚠️ 快速浏览 SKILL.md |
| 权限检查 | ✅ 确认权限合理 |

### GitHub 第三方技能

| 检查项 | 要求 |
|--------|------|
| 来源验证 | ✅ 仓库真实存在 |
| 活跃度 | ✅ 6 个月内有更新 |
| 社区反馈 | ✅ 10+ stars 或正面评价 |
| 代码审查 | ✅ 详细审查 SKILL.md 和脚本 |
| 权限检查 | ✅ 最小权限原则 |
| 安全扫描 | ✅ 无可疑代码模式 |

### 禁止安装的情况

```
❌ 来源不明且无社区反馈
❌ 包含加密密钥或敏感信息
❌ 使用 eval、exec 等危险函数
❌ 连接到不明外部服务
❌ 要求过高权限
❌ 代码混淆或加密
❌ 用户明确反对
```

---

## 🔧 可用工具

### 搜索工具

| 工具 | 用途 | 命令 |
|------|------|------|
| **clawhub** | ClawHub 搜索 | `clawhub search "[query]"` |
| **web_search** | 全网搜索 | `web_search --query "[query]"` |
| **browser** | 浏览网页 | `browser navigate "url"` |
| **web_fetch** | 抓取网页 | `web_fetch --url "url"` |

### 安装工具

| 工具 | 用途 | 命令 |
|------|------|------|
| **clawhub** | ClawHub 安装 | `clawhub install <slug>` |
| **npx skills** | GitHub 安装 | `npx skills add <url> --skill <name>` |
| **openclaw** | 插件安装 | `openclaw plugins install <name>` |
| **auto-install-skill** | Fallback 安装 | 自动从 raw URL 抓取 |

---

## 📊 决策流程

### 流程图

```
用户：安装 X 技能
         ↓
┌────────────────────────┐
│ 1. 搜索 ClawHub        │
│    clawhub search "X"  │
└──────────┬─────────────┘
           │
      ┌────┴────┐
      │ 找到？  │
      └────┬────┘
       Yes │ No
           │  │
           │  └──────────────┐
           │                 ↓
           │        ┌────────────────┐
           │        │ 2. 搜索 GitHub │
           │        │ + 社区资源     │
           │        └───────┬────────┘
           │                │
           │           ┌────┴────┐
           │           │ 找到？  │
           │           └────┬────┘
           │            Yes │ No
           │                │  │
           │                │  └────────┐
           │                │           ↓
           │                │    ┌─────────────┐
           │                │    │ 3. 告知用户 │
           │                │    │ 建议替代方案│
           │                │    └─────────────┘
           │                │
           ↓                ↓
    ┌──────────────┐ ┌──────────────┐
    │ 安全检查     │ │ 安全检查     │
    │ (官方快速)   │ │ (第三方详细) │
    └──────┬───────┘ └──────┬───────┘
           │                │
           ↓                ↓
    ┌──────────────┐ ┌──────────────┐
    │ 安装技能     │ │ 用户确认     │
    └──────┬───────┘ └──────┬───────┘
           │                │
           └────────┬───────┘
                    ↓
           ┌────────────────┐
           │ 验证 + 记录     │
           └────────────────┘
```

---

## 💡 最佳实践

### ✅ 推荐做法

1. **优先官方**: 始终先搜索 ClawHub/OpenClawDir
2. **透明沟通**: 告知用户技能来源和风险
3. **用户确认**: 安装前获得用户明确同意
4. **详细记录**: 记录安装的技能到 MEMORY.md
5. **定期更新**: 使用 `clawhub update --all`

### ❌ 避免做法

1. **跳过搜索**: 直接从 GitHub 安装
2. **隐瞒风险**: 不告知用户第三方技能的风险
3. **过度权限**: 安装要求过多权限的技能
4. **不记录**: 安装后不记录到 MEMORY.md
5. **不更新**: 长期不更新技能

---

## 📝 用户交互示例

### 场景 1: 官方有技能

```
用户：帮我安装一个 PDF 编辑技能

AI: 好的，我先在 ClawHub 搜索一下...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
找到了以下 PDF 相关技能：

① nano-pdf - PDF 编辑和处理 ⭐4.5
   功能：编辑、转换、合并 PDF

② pdf-analyzer - PDF 内容分析 ⭐4.2
   功能：提取文字、分析结构

③ pdf-converter - PDF 格式转换 ⭐4.0
   功能：PDF 与 Word/Excel 互转

要安装哪个？或者需要详细介绍？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

用户：安装 nano-pdf

AI: 好的，正在安装 nano-pdf...
✅ 安装完成！nano-pdf 已就绪。
需要我记录到 MEMORY.md 吗？
```

### 场景 2: 官方没有，GitHub 有

```
用户：帮我找个能控制 Spotify 的技能

AI: 让我先在 ClawHub 搜索...
❌ ClawHub 没有找到 Spotify 相关技能

让我搜索 GitHub...
✅ 找到了一个：spotify-player
   - 仓库：github.com/author/spotify-skill
   - Stars: 85
   - 最近更新：2 周前
   - 功能：Spotify 播放控制

⚠️ 注意：这是第三方技能，我已审查代码，没有发现安全问题。
要安装吗？

用户：安装吧

AI: 好的，正在安装...
✅ 安装完成！需要测试一下功能吗？
```

### 场景 3: 完全找不到

```
用户：帮我找个能控制微波炉的技能

AI: 让我搜索一下...
❌ ClawHub：没有找到
❌ GitHub：没有找到相关技能

抱歉，目前没有找到能控制微波炉的 OpenClaw 技能。

可能的原因：
1. 这个功能比较特殊，还没有人开发
2. 可能需要特定的硬件支持

替代方案：
1. 我可以帮你查找微波炉的 API 文档
2. 或者你可以考虑自己创建一个技能

需要我帮你做什么？
```

---

## 🔗 相关资源

- **ClawHub**: https://clawhub.com
- **OpenClawDir**: 3425+ 技能，602+ 插件
- **技能文档**: https://docs.openclaw.ai/tools/skills
- **安全指南**: https://docs.openclaw.ai/gateway/security

---

**最后更新**: 2026-03-04  
**维护者**: OpenClaw 安全委员会
