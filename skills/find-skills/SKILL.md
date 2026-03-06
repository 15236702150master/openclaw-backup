---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## OpenClawDir - Official Directory

**OpenClawDir** is the official directory for OpenClaw skills and plugins:

- **3425+ Skills** - Community-contributed skills for various tasks
- **602+ Plugins** - Extensions that enhance OpenClaw capabilities
- **Search & Discover** - Find skills by category, popularity, or keywords
- **One-Click Install** - Install skills directly from the directory

**Access Methods:**
1. Web: Browse OpenClawDir website
2. CLI: `npx skills find [query]`
3. AI: Ask the assistant to find skills using find-skills skill

## How to Help Users Find Skills

### Installation Workflow (优化流程)

```
User requests skill/plugin installation
         ↓
Step 1: Search official repositories (OpenClawDir/ClawHub)
         ↓
   Found? → Install and confirm
         ↓
   Not found?
         ↓
Step 2: Search web (GitHub, community sources)
         ↓
   Found? → Verify safety → Install
         ↓
   Not found? → Inform user, suggest alternatives
```

### Step 1: Search Official Repositories (优先官方)

**Search ClawHub:**
```bash
clawhub search "[query]"
```

**Examples:**
- "pdf editor" → Search PDF-related skills
- "automation" → Search automation skills
- "discord" → Search Discord plugins

**Present results:**
```
我在 ClawHub 找到了以下技能：

1. nano-pdf - PDF 编辑和处理
2. pdf-analyzer - PDF 内容分析
3. pdf-converter - PDF 格式转换

要安装哪个？或者需要我详细介绍某个技能？
```

### Step 2: Search Web (官方没有再上网找)

**If not found in official repos:**

1. **Search GitHub:**
```bash
# Use web search or browser
https://github.com/search?q=openclaw+skills+pdf
```

2. **Verify Safety:**
- Check repository stars and activity
- Read SKILL.md carefully
- Look for suspicious code patterns
- Check community feedback

3. **Install from GitHub:**
```bash
npx skills add https://github.com/owner/repo --skill skill-name
```

### Step 3: Present and Install

**Example response:**
```
✅ 官方资源库没有找到合适的技能

我从 GitHub 找到了一个备选：
- Skill: pdf-tools
- Repository: github.com/author/pdf-tools
- Description: PDF 处理工具集
- Stars: 150+

⚠️ 注意：这是第三方技能，需要审查代码

要安装吗？或者我帮你找其他替代方案？
```

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
