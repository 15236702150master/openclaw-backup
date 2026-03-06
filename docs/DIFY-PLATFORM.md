# Dify AI 平台

## 📋 平台简介

**Dify** 是一个开源的 AI 应用开发平台，支持创建和管理 AI Agent，并调用 150+ 工具完成复杂任务。

**官方网站：** https://difyai.com  
**GitHub：** https://github.com/langgenius/dify  
**许可证：** Apache 2.0（开源）

---

## 🎯 核心功能

### 1. AI Agent 编排

- **可视化工作流** - 拖拽式 Agent 编排
- **多模型支持** - 支持 GPT、Claude、通义千问等
- **工具调用** - 150+ 预置工具
- **记忆管理** - 长短期记忆支持

### 2. 工具生态

**内置工具（150+）：**
- 🔍 **搜索工具** - Google Search、Bing、Wikipedia
- 📊 **数据分析** - Python 解释器、代码执行
- 📁 **文件处理** - PDF、Word、Excel 解析
- 🌐 **网络工具** - 网页抓取、API 调用
- 📧 **通讯工具** - Email、Slack、Discord
- 📅 **办公工具** - 日历、待办、笔记
- 🎨 **创意工具** - 图像生成、文本创作

**自定义工具：**
- 支持 OpenAPI/Swagger 规范
- 支持 Python/JavaScript 代码工具
- 支持 HTTP 请求工具

### 3. 应用类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **聊天助手** | 对话式 AI | 客服、问答 |
| **Agent** | 自主执行任务 | 自动化、工作流 |
| **工作流** | 可视化编排 | 复杂业务流程 |
| **文本生成** | 结构化输出 | 文章、报告 |

---

## 🔧 技术架构

### 后端
- **语言：** Python
- **框架：** FastAPI
- **数据库：** PostgreSQL
- **缓存：** Redis
- **向量库：** Weaviate/Milvus/Pgvector

### 前端
- **框架：** React + TypeScript
- **UI 库：** Ant Design
- **状态管理：** Redux

### 部署
- **Docker：** 一键部署
- **Kubernetes：** 支持集群部署
- **云服务：** AWS、Azure、阿里云

---

## 🚀 快速开始

### 本地部署

```bash
# 克隆仓库
git clone https://github.com/langgenius/dify.git
cd dify

# 使用 Docker Compose 启动
cd docker
docker compose up -d

# 访问 http://localhost:3000
```

### 云服务

**官方云：** https://cloud.dify.ai  
- 免费额度：每月可用
- 付费计划：按使用量计费

---

## 🔌 与 OpenClaw 集成

### 方案 1: 使用 Dify API

```python
import requests

DYFI_API_KEY = "your-api-key"
DYFI_APP_ID = "your-app-id"

def call_dify_agent(query):
    response = requests.post(
        f"https://api.dify.ai/v1/completion",
        headers={"Authorization": f"Bearer {DYFI_API_KEY}"},
        json={
            "inputs": {"query": query},
            "response_mode": "blocking"
        }
    )
    return response.json()["answer"]
```

### 方案 2: 作为工具调用

```json
{
  "name": "dify-agent",
  "description": "调用 Dify AI Agent 执行复杂任务",
  "endpoint": "https://api.dify.ai/v1/completion",
  "auth": "Bearer ${DIFY_API_KEY}"
}
```

### 方案 3: 工作流集成

```
OpenClaw → Dify API → 150+ 工具 → 返回结果 → OpenClaw
```

---

## 📊 对比 OpenClaw

| 特性 | Dify | OpenClaw |
|------|------|----------|
| **定位** | AI 应用开发平台 | AI 助手编排框架 |
| **工具数量** | 150+ 预置 | 社区技能 + 自定义 |
| **部署方式** | 独立服务 | Node.js 应用 |
| **可视化** | ✅ 工作流编排 | ❌ 代码配置 |
| **开源** | ✅ Apache 2.0 | ✅ MIT |
| **适合场景** | 企业级 AI 应用 | 个人/团队 AI 助手 |

---

## 💡 使用场景

### 1. 客服机器人

```
用户提问 → Dify 理解意图 → 调用知识库 → 生成回答
```

### 2. 数据分析助手

```
上传数据 → Python 解释器分析 → 生成图表 → 输出报告
```

### 3. 自动化工作流

```
触发条件 → 多步骤工具调用 → 结果汇总 → 通知用户
```

### 4. 内容创作

```
主题输入 → 多模型协作 → 内容生成 → 质量检查 → 输出
```

---

## 🔗 相关资源

### 官方资源
- **官网：** https://difyai.com
- **文档：** https://docs.dify.ai
- **GitHub：** https://github.com/langgenius/dify
- **云服务：** https://cloud.dify.ai
- **社区：** https://discord.gg/dify

### 工具市场
- **内置工具：** 150+ 预置工具
- **自定义工具：** 支持 OpenAPI 规范
- **插件系统：** 支持扩展开发

### 学习资源
- **教程：** https://docs.dify.ai/getting-started
- **示例应用：** https://github.com/langgenius/dify-examples
- **API 文档：** https://docs.dify.ai/api

---

## 🎯 集成建议

### 高优先级 ⭐⭐⭐

1. **作为工具调用**
   - 创建 `dify-agent` 技能
   - 通过 API 调用 Dify Agent
   - 利用其 150+ 工具生态

2. **知识库集成**
   - 使用 Dify 的知识库功能
   - 增强 OpenClaw 的记忆检索
   - 语义搜索 + 向量检索

### 中优先级 ⭐⭐

3. **工作流编排**
   - 复杂任务用 Dify 编排
   - OpenClaw 负责任务分发
   - 结果汇总和展示

4. **多模型路由**
   - Dify 支持多模型
   - 根据任务选择模型
   - 优化成本和性能

### 低优先级 ⭐

5. **可视化配置**
   - 使用 Dify 的可视化界面
   - 配置 OpenClaw 技能
   - 降低使用门槛

---

## 📝 配置示例

### 创建 Dify 技能

```markdown
---
name: dify-agent
description: 调用 Dify AI Agent 执行复杂任务，支持 150+ 工具
---

# Dify Agent

通过 Dify API 调用 AI Agent 和工具。

## 配置

```json
{
  "apiKey": "${DIFY_API_KEY}",
  "appId": "${DIFY_APP_ID}",
  "baseUrl": "https://api.dify.ai"
}
```

## 使用

```bash
python3 scripts/call-dify.py "分析这份数据"
```

## 支持的工具

- 搜索：Google、Bing、Wikipedia
- 分析：Python、代码执行
- 文件：PDF、Word、Excel
- 网络：网页抓取、API 调用
- ... 150+ 工具
```
```

---

**最后更新：** 2026-03-05  
**状态：** ✅ 已加入资源库  
**优先级：** 高（建议集成）
