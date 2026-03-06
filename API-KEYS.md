# API Keys 配置

## Google Gemini API
**用途**: 多模态图片分析、视觉理解  
**Key**: `AIzaSyByLm8elNpvR-R16gv-kylBZXopnie25mI`  
**状态**: ⚠️ 中国大陆访问受限，需要代理

**设置方式**:
```bash
export GEMINI_API_KEY="AIzaSyByLm8elNpvR-R16gv-kylBZXopnie25mI"
export HTTPS_PROXY="http://your-proxy:port"  # 如果有代理
```

**使用示例**:
```bash
# 分析图片（需要代理）
summarize /tmp/screenshot.png --model google/gemini-2.0-flash

# 或者使用 Python
python3 analyze_with_gemini.py /tmp/screenshot.png
```

**免费额度**: $5 或 60 次/分钟  
**文档**: https://ai.google.dev/gemini-api/docs

**替代方案**:
- 使用阿里云 Qwen-VL（需要单独开通多模态权限）
- 使用本地 VLM（LLaVA、InternVL）
- 在有代理的服务器上运行

---

## 阿里云 Qwen API
**用途**: 文本 LLM、对话、规划  
**Key**: `sk-sp-fb44441446d9445799ce6370cd17de36`  
**Base URL**: `https://coding.dashscope.aliyuncs.com/v1`

---

**配置文件位置**: `/root/.openclaw/workspace/API-KEYS.md`  
**最后更新**: 2026-03-06 02:10
