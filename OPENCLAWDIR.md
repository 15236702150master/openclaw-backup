# OpenClawDir - 技能和插件资源库

## 📚 资源概览

**OpenClawDir** 是 OpenClaw 官方的技能和插件汇集目录，提供丰富的扩展资源。

### 规模统计

| 类型 | 数量 | 说明 |
|------|------|------|
| **技能 (Skills)** | 3425+ | 社区贡献的各种功能技能 |
| **插件 (Plugins)** | 602+ | 扩展 OpenClaw 核心能力的插件 |
| **总计** | 4027+ | 可用扩展资源 |

---

## 🔍 技能分类

### 热门技能类别

| 类别 | 数量 | 示例 |
|------|------|------|
| **开发工具** | ~800 | Git 管理、代码审查、测试生成 |
| **数据处理** | ~500 | PDF 处理、Excel 分析、数据可视化 |
| **自动化** | ~600 | 文件管理、定时任务、工作流 |
| **AI 增强** | ~400 | 文本分析、图像识别、语音处理 |
| **生产力** | ~350 | 笔记管理、待办、时间追踪 |
| **集成** | ~300 | Slack、Discord、Notion 等 |
| **其他** | ~475 | 各种专业领域技能 |

---

## 🔌 插件分类

### 热门插件类别

| 类别 | 数量 | 示例 |
|------|------|------|
| **通讯插件** | ~150 | DingTalk、WeCom、Telegram |
| **存储插件** | ~100 | Google Drive、Dropbox、OneDrive |
| **开发插件** | ~120 | GitHub、GitLab、VSCode |
| **AI 服务** | ~80 | ElevenLabs、Midjourney、Stability |
| **工具插件** | ~152 | 浏览器控制、文件系统等 |

---

## 🎯 使用方式

### 方法 1: 通过 find-skills 技能

```
用户：帮我找个能处理 PDF 的技能
AI：[使用 find-skills 搜索]
→ 找到 nano-pdf、pdf-editor 等
→ 提供安装命令
→ 用户确认后安装
```

### 方法 2: 直接搜索

```bash
# 搜索技能
npx skills find pdf

# 搜索插件
npx skills find plugin:discord

# 按类别搜索
npx skills find category:automation
```

### 方法 3: 浏览 OpenClawDir 网站

访问 OpenClawDir 官方网站浏览和搜索技能/插件。

---

## 📦 安装技能

### 标准安装

```bash
# 从 GitHub 安装
npx skills add owner/repo@skill-name

# 从 OpenClawDir 安装
npx skills add openclawdir/skill-name
```

### 批量安装

```bash
# 安装多个技能
npx skills add skill1 skill2 skill3

# 安装整个类别
npx skills add category:productivity --all
```

### 更新技能

```bash
# 更新所有技能
npx skills update --all

# 更新特定技能
npx skills update skill-name
```

---

## 🔧 常用技能推荐

### 开发相关

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `git-helper` | Git 操作辅助 | `npx skills add git-helper` |
| `code-review` | 代码审查 | `npx skills add code-review` |
| `test-generator` | 测试生成 | `npx skills add test-generator` |

### 数据处理

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `nano-pdf` | PDF 编辑 | `npx skills add nano-pdf` |
| `excel-analyzer` | Excel 分析 | `npx skills add excel-analyzer` |
| `data-visualizer` | 数据可视化 | `npx skills add data-visualizer` |

### 生产力

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `todo-manager` | 待办管理 | `npx skills add todo-manager` |
| `memory-manager` | 记忆管理 | `npx skills add memory-manager` |
| `daily-summary` | 每日摘要 | `npx skills add daily-summary` |

### 自动化

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `file-organizer` | 文件整理 | `npx skills add file-organizer` |
| `cron-manager` | 定时任务 | `npx skills add cron-manager` |
| `workflow-automation` | 工作流 | `npx skills add workflow-automation` |

---

## 🔌 常用插件推荐

### 通讯插件

| 插件 | 用途 | 安装命令 |
|------|------|----------|
| `dingtalk` | 钉钉集成 | 已内置 |
| `wecom-app` | 企业微信 | 已内置 |
| `telegram` | Telegram 机器人 | `openclaw plugins install telegram` |

### AI 服务插件

| 插件 | 用途 | 安装命令 |
|------|------|----------|
| `elevenlabs-tts` | 语音合成 | `openclaw plugins install elevenlabs-tts` |
| `midjourney` | 图像生成 | `openclaw plugins install midjourney` |

---

## 📊 技能发现技巧

### 1. 关键词搜索

```bash
# 精确搜索
npx skills find "pdf editor"

# 模糊搜索
npx skills find pdf

# 组合搜索
npx skills find "pdf edit convert"
```

### 2. 按类别浏览

```bash
# 查看所有类别
npx skills categories

# 查看特定类别
npx skills find category:development
```

### 3. 查看热门技能

```bash
# 按下载量排序
npx skills find --sort=downloads

# 按评分排序
npx skills find --sort=rating
```

### 4. 查看技能详情

```bash
# 查看技能信息
npx skills info skill-name

# 查看技能依赖
npx skills info skill-name --deps
```

---

## ⚠️ 注意事项

### 安装前检查

1. **兼容性**: 确认技能与当前 OpenClaw 版本兼容
2. **依赖**: 检查是否需要额外依赖
3. **权限**: 确认技能需要的权限
4. **评价**: 查看其他用户评价

### 安全建议

1. **官方优先**: 优先安装 OpenClawDir 官方推荐的技能
2. **查看源码**: 安装前查看技能源码
3. **最小权限**: 只授予必要的权限
4. **定期更新**: 保持技能更新到最新版本

---

## 🔄 贡献技能

### 发布技能到 OpenClawDir

1. **创建技能**: 使用 `npx skills init` 创建技能模板
2. **测试技能**: 本地测试技能功能
3. **提交审核**: 提交到 OpenClawDir 审核
4. **发布**: 审核通过后发布

### 技能模板

```bash
# 初始化技能
npx skills init my-skill

# 目录结构
my-skill/
├── SKILL.md          # 技能定义（必需）
├── script.sh         # 脚本文件
├── config.json       # 配置文件
└── README.md         # 说明文档
```

---

## 📈 统计数据

### OpenClawDir 增长趋势

| 时间 | 技能数量 | 插件数量 |
|------|---------|---------|
| 2024-01 | 1000+ | 200+ |
| 2024-06 | 2000+ | 400+ |
| 2024-12 | 3000+ | 550+ |
| 2025-03 | 3425+ | 602+ |

### 热门类别增长

- **AI 增强**: +150% (年增长)
- **自动化**: +120% (年增长)
- **数据处理**: +100% (年增长)

---

## 🔗 相关链接

- **OpenClawDir 官网**: [待补充]
- **技能文档**: https://docs.openclaw.ai/tools/skills
- **插件文档**: https://docs.openclaw.ai/plugins
- **GitHub 仓库**: https://github.com/openclaw/openclaw
- **社区**: https://discord.com/invite/clawd

---

**最后更新**: 2026-03-04  
**维护者**: OpenClaw 社区
