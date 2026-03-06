# OpenClaw 技能和插件资源库完整列表

## 📚 官方资源库

### 1. OpenClawDir (主要)
- **网址**: [待确认]
- **规模**: 3425+ 技能，602+ 插件
- **类型**: 官方汇集目录
- **访问方式**: 
  - Web 浏览
  - `npx skills find` 搜索
  - find-skills 技能协助

### 2. ClawHub (官方注册表)
- **网址**: https://clawhub.com
- **规模**: 公共技能注册表
- **类型**: 官方技能发布平台
- **访问方式**:
  ```bash
  # 安装 CLI
  npm i -g clawhub
  
  # 搜索技能
  clawhub search "pdf"
  
  # 安装技能
  clawhub install <skill-slug>
  
  # 更新所有技能
  clawhub update --all
  ```
- **功能**:
  - 技能发布和版本管理
  - 技能搜索和发现
  - 自动更新和同步
  - 社区评价和反馈

### 3. AgentSkills.io (兼容标准)
- **网址**: https://agentskills.io
- **类型**: AgentSkills 兼容标准
- **说明**: OpenClaw 使用 AgentSkills 兼容格式，可以复用该生态的技能

---

## 🔍 第三方资源库

### 4. GitHub Skills
- **网址**: https://github.com/topics/openclaw-skills
- **规模**: 社区贡献
- **类型**: GitHub 主题聚合
- **访问方式**:
  ```bash
  # 直接从 GitHub 安装
  npx skills add https://github.com/owner/repo --skill skill-name
  ```

### 5. Vercel Labs Skills
- **网址**: https://github.com/vercel-labs/skills
- **规模**: 官方示例技能集合
- **类型**: 示例和模板
- **热门技能**:
  - find-skills (技能搜索)
  - 其他 Vercel 官方技能

### 6. ComposioHQ Awesome Skills
- **网址**: https://github.com/ComposioHQ/awesome-claude-skills
- **规模**: 精选技能列表
- **类型**: 社区精选
- **说明**: 虽然主要是 Claude skills，但很多可以适配 OpenClaw

---

## 🔌 插件资源

### 7. NPM Registry
- **网址**: https://www.npmjs.com/search?q=openclaw-plugin
- **规模**: 602+ 官方插件 + 社区插件
- **类型**: NPM 包注册表
- **访问方式**:
  ```bash
  # 安装插件
  openclaw plugins install <plugin-name>
  
  # 示例
  openclaw plugins install @openclaw-china/dingtalk
  openclaw plugins install @openclaw-china/wecom-app
  ```

### 8. OpenClaw Extensions
- **位置**: `~/.openclaw/extensions/`
- **类型**: 本地扩展目录
- **说明**: 已安装插件的本地存储位置

---

## 🎯 使用方式对比

| 资源库 | 搜索 | 安装 | 更新 | 安全性 |
|--------|------|------|------|--------|
| **OpenClawDir** | ✅ Web + CLI | ✅ 一键 | ✅ 自动 | ⭐⭐⭐⭐⭐ 官方 |
| **ClawHub** | ✅ CLI | ✅ 一键 | ✅ 自动 | ⭐⭐⭐⭐⭐ 官方 |
| **GitHub** | ✅ Web | ✅ 手动 | ❌ 手动 | ⭐⭐⭐ 需审查 |
| **NPM** | ✅ Web | ✅ 一键 | ✅ 自动 | ⭐⭐⭐⭐ 审核 |

---

## 📦 安装技能的方法

### 方法 1: 通过 find-skills 技能（推荐）

```
用户：帮我找个能处理 PDF 的技能
AI: [使用 find-skills 搜索 OpenClawDir/ClawHub]
→ 提供多个选项
→ 用户选择后安装
```

### 方法 2: 使用 ClawHub CLI

```bash
# 搜索
clawhub search "pdf editor"

# 安装
clawhub install pdf-pro

# 更新
clawhub update --all
```

### 方法 3: 直接从 GitHub 安装

```bash
# 使用 npx skills
npx skills add https://github.com/owner/repo --skill skill-name

# 使用 auto-install-skill（克隆失败时 fallback）
自动从 raw GitHub URL 抓取文件
```

### 方法 4: 使用 openclaw 命令

```bash
# 安装插件
openclaw plugins install <plugin-name>

# 查看已安装
openclaw plugins list
```

---

## 🔐 安全建议

### 安装前检查清单

1. **来源验证**
   - ✅ 优先选择 OpenClawDir/ClawHub 官方推荐
   - ✅ 查看发布者信誉
   - ⚠️ GitHub 技能需审查源码

2. **代码审查**
   - 阅读 SKILL.md 了解功能
   - 检查脚本文件是否有恶意代码
   - 确认权限要求合理

3. **权限控制**
   - 最小权限原则
   - 敏感操作需用户确认
   - 使用沙箱运行不信任的技能

4. **更新管理**
   - 定期更新技能到最新版本
   - 关注安全公告
   - 删除不再使用的技能

---

## 📊 资源库统计

| 资源库 | 技能数量 | 插件数量 | 总计 | 更新频率 |
|--------|---------|---------|------|---------|
| OpenClawDir | 3425+ | 602+ | 4027+ | 每日 |
| ClawHub | 动态增长 | 包含在内 | - | 实时 |
| GitHub | ~500+ | ~100+ | ~600+ | 社区驱动 |
| NPM | - | 602+ | 602+ | 每日 |

---

## 🎓 学习资源

### 官方文档
- **技能文档**: https://docs.openclaw.ai/tools/skills
- **插件文档**: https://docs.openclaw.ai/tools/plugins
- **ClawHub 文档**: https://docs.openclaw.ai/tools/clawhub
- **完整文档**: https://docs.openclaw.ai

### 社区资源
- **GitHub**: https://github.com/openclaw/openclaw
- **Discord**: https://discord.com/invite/clawd
- **技能模板**: `npx skills init`

---

## 🚀 推荐工作流

### 查找技能
```
1. 使用 find-skills 技能搜索
   ↓
2. AI 协助筛选合适的技能
   ↓
3. 查看技能详情和评价
   ↓
4. 确认后安装
```

### 管理技能
```
1. 定期运行 clawhub update --all
   ↓
2. 审查已安装技能
   ↓
3. 删除不用的技能
   ↓
4. 记录重要技能到 MEMORY.md
```

### 贡献技能
```
1. 使用 npx skills init 创建技能
   ↓
2. 本地测试功能
   ↓
3. 提交到 ClawHub 审核
   ↓
4. 发布到 OpenClawDir
```

---

## 📝 配置示例

### ~/.openclaw/openclaw.json

```json
{
  "skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 250
    },
    "entries": {
      "find-skills": { "enabled": true },
      "auto-install-skill": { "enabled": true },
      "daily-summary-ai": { "enabled": true }
    }
  },
  "plugins": {
    "entries": {
      "dingtalk": { "enabled": true },
      "wecom-app": { "enabled": true }
    }
  }
}
```

---

## 🔮 未来扩展

### 计划中的资源库
- [ ] 技能市场（带付费技能）
- [ ] 企业技能库（私有部署）
- [ ] 技能认证体系
- [ ] 技能排行榜

### 社区贡献
- 提交技能到 ClawHub
- 参与技能审核
- 编写技能教程
- 翻译技能文档

---

**最后更新**: 2026-03-04  
**维护者**: OpenClaw 社区  
**反馈**: https://discord.com/invite/clawd
