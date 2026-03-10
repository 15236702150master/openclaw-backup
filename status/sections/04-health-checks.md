# 健康检查说明

> OpenClaw 10 项健康检查详细说明

---

## 健康检查概览

健康检查脚本位于: `/root/server-tools/openclaw-healthcheck.sh`

检查结果保存在: `/root/server-tools/healthcheck.log`

运行命令:
```bash
bash /root/server-tools/openclaw-healthcheck.sh
tail -20 /root/server-tools/healthcheck.log
```

---

## 检查项目详解

### [1/10] Gateway: 进程检查

**检查内容**: Gateway 进程是否正在运行

**检查方法**:
```bash
ps aux | grep openclaw-gateway | grep -v grep
```

**通过条件**: 找到 openclaw-gateway 进程

**失败原因**:
- Gateway 未启动
- 进程崩溃
- 启动失败

**解决方案**:
```bash
# 启动 Gateway
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service"

# 检查启动日志
tail -50 /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log
```

---

### [2/10] Gateway: 端口监听

**检查内容**: Gateway 是否监听 18789 端口

**检查方法**:
```bash
ss -tlnp | grep 18789
```

**通过条件**: 端口 18789 处于 LISTEN 状态

**失败原因**:
- Gateway 未启动
- 端口被其他进程占用
- 启动失败但进程存在

**解决方案**:
```bash
# 检查端口占用
ss -tlnp | grep 18789

# 如果被占用，杀死进程
kill -9 <PID>

# 重新启动
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

---

### [3/10] Gateway: 日志文件

**检查内容**: 今天的日志文件是否存在

**检查方法**:
```bash
test -f /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log
```

**通过条件**: 日志文件存在

**失败原因**:
- Gateway 未启动
- 日志目录权限问题
- 日志路径配置错误

**解决方案**:
```bash
# 检查日志目录
ls -la /tmp/openclaw-0/

# 检查权限
ls -ld /tmp/openclaw-0/

# 如果目录不存在，创建
mkdir -p /tmp/openclaw-0/
chmod 755 /tmp/openclaw-0/
```

---

### [4/10] Gateway: RPC 响应

**检查内容**: Gateway RPC 接口是否响应

**检查方法**:
```bash
/root/.nvm/versions/node/v22.22.0/bin/openclaw gateway probe
```

**通过条件**: 命令返回成功

**失败原因**:
- Gateway 未启动
- RPC 接口异常
- 网络问题

**解决方案**:
```bash
# 检查 Gateway 状态
ps aux | grep openclaw-gateway

# 查看错误日志
tail -50 /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | grep -i error

# 重启 Gateway
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

---

### [5/10] 配置: 文件存在

**检查内容**: 主配置文件是否存在

**检查方法**:
```bash
test -f /root/.openclaw/openclaw.json
```

**通过条件**: 配置文件存在

**失败原因**:
- 配置文件被删除
- 路径错误
- 权限问题

**解决方案**:
```bash
# 检查文件
ls -la /root/.openclaw/openclaw.json

# 如果不存在，从备份恢复
# 或重新初始化 OpenClaw
```

---

### [6/10] 配置: JSON 格式

**检查内容**: 配置文件 JSON 格式是否正确

**检查方法**:
```bash
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null
```

**通过条件**: JSON 解析成功

**失败原因**:
- JSON 语法错误
- 缺少逗号、括号
- 编码问题

**解决方案**:
```bash
# 验证 JSON
python3 -m json.tool /root/.openclaw/openclaw.json

# 查看错误信息
python3 << 'PYEOF'
import json
try:
    with open("/root/.openclaw/openclaw.json", "r") as f:
        json.load(f)
    print("✅ JSON 格式正确")
except Exception as e:
    print(f"❌ JSON 错误: {e}")
PYEOF

# 使用编辑器修复
vim /root/.openclaw/openclaw.json
```

---

### [7/10] 模型: 百炼配置

**检查内容**: 是否配置并使用百炼模型

**检查方法**:
```bash
grep -i "bailian" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log
```

**通过条件**: 日志中包含 "bailian"

**失败原因**:
- 未配置百炼模型
- 使用其他模型
- 模型配置错误

**解决方案**:
```bash
# 检查配置
grep -A 5 "model" /root/.openclaw/openclaw.json

# 查看当前使用的模型
grep "agent model" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | tail -1

# 修改配置使用百炼模型
vim /root/.openclaw/openclaw.json
# 设置: "model": "bailian/qwen3.5-plus"

# 重启服务
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

---

### [8/10] 插件: 加载状态

**检查内容**: 插件是否成功加载

**检查方法**:
```bash
grep -i "plugin.*loaded\|plugin.*enabled" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log
```

**通过条件**: 日志中有插件加载成功的记录

**失败原因**:
- 插件目录权限问题
- 插件配置错误
- 插件文件损坏

**解决方案**:
```bash
# 检查插件目录权限
ls -la /root/.openclaw/plugins/

# 查看插件加载日志
grep -i "plugin" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | tail -20

# 修复权限
chown -R root:root /root/.openclaw/
setfacl -R -m u:master:rwx /root/.openclaw/
```

---

### [9/10] 钉钉: 连接状态

**检查内容**: 钉钉是否成功连接

**检查方法**:
```bash
grep -i "CONNECTED" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log
```

**通过条件**: 日志中有 "CONNECTED" 状态

**失败原因**:
- 钉钉配置错误
- 网络连接问题
- 认证失败

**解决方案**:
```bash
# 检查钉钉配置
grep -A 20 "dingtalk" /root/.openclaw/openclaw.json

# 查看钉钉连接日志
grep -i "dingtalk" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | tail -20

# 测试网络连接
ping -c 3 oapi.dingtalk.com

# 重启服务
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

---

### [10/10] 会话: 数据目录

**检查内容**: 会话数据目录是否存在

**检查方法**:
```bash
test -d /root/.openclaw/agents/*/sessions/
```

**通过条件**: 会话目录存在

**失败原因**:
- 目录被删除
- 权限问题
- 初始化未完成

**解决方案**:
```bash
# 检查目录
ls -la /root/.openclaw/agents/

# 如果不存在，创建
mkdir -p /root/.openclaw/agents/default/sessions/

# 修复权限
chown -R root:root /root/.openclaw/
chmod -R 755 /root/.openclaw/
```

---

## 健康检查结果解读

### 全部通过（10/10）
```
✅ [1/10] Gateway: 进程运行正常
✅ [2/10] Gateway: 端口监听正常
✅ [3/10] Gateway: 日志文件存在
✅ [4/10] Gateway: RPC 响应正常
✅ [5/10] 配置: 文件存在
✅ [6/10] 配置: JSON 格式正确
✅ [7/10] 模型: 使用百炼模型
✅ [8/10] 插件: 加载成功
✅ [9/10] 钉钉: 连接成功
✅ [10/10] 会话: 数据目录存在

健康检查: 10/10 通过 ✅
```

**状态**: 系统运行正常，无需操作

---

### 部分失败（例如 8/10）
```
✅ [1/10] Gateway: 进程运行正常
✅ [2/10] Gateway: 端口监听正常
❌ [3/10] Gateway: 日志文件不存在
✅ [4/10] Gateway: RPC 响应正常
✅ [5/10] 配置: 文件存在
✅ [6/10] 配置: JSON 格式正确
❌ [7/10] 模型: 配置错误或未使用百炼模型
✅ [8/10] 插件: 加载成功
✅ [9/10] 钉钉: 连接成功
✅ [10/10] 会话: 数据目录存在

健康检查: 8/10 通过 ⚠️
```

**状态**: 系统部分功能异常，需要修复

**处理**: 根据失败项目的解决方案逐一修复

---

### 严重失败（例如 3/10）
```
❌ [1/10] Gateway: 进程未运行
❌ [2/10] Gateway: 端口未监听
❌ [3/10] Gateway: 日志文件不存在
❌ [4/10] Gateway: RPC 无响应
✅ [5/10] 配置: 文件存在
✅ [6/10] 配置: JSON 格式正确
❌ [7/10] 模型: 配置错误或未使用百炼模型
❌ [8/10] 插件: 加载失败
❌ [9/10] 钉钉: 连接失败
✅ [10/10] 会话: 数据目录存在

健康检查: 3/10 通过 ❌
```

**状态**: 系统严重异常，需要完整修复

**处理**: 运行完整修复脚本
```bash
bash /root/server-tools/fix-openclaw-complete.sh
```

---

## 自动化健康检查

### 定时任务（Cron）

```bash
# 编辑 crontab
crontab -e

# 每 5 分钟运行一次健康检查
*/5 * * * * /bin/bash /root/server-tools/openclaw-healthcheck.sh

# 每小时发送结果到日志
0 * * * * /bin/bash /root/server-tools/openclaw-healthcheck.sh && tail -20 /root/server-tools/healthcheck.log >> /root/server-tools/health-history.log
```

### 监控脚本

```bash
#!/bin/bash
# 文件: /root/server-tools/health-monitor.sh

while true; do
    bash /root/server-tools/openclaw-healthcheck.sh
    RESULT=$(tail -1 /root/server-tools/healthcheck.log | grep -o "[0-9]*/10" | cut -d/ -f1)
    
    if [ "$RESULT" -lt 8 ]; then
        echo "⚠️ 健康检查失败: $RESULT/10"
        # 发送告警（可选）
        # 自动修复（可选）
    fi
    
    sleep 300  # 5 分钟检查一次
done
```

---

## Web 管理器集成

Web 管理器地址: https://uolyss7sgi.fy.takin.cc/

功能:
- 一键健康检查
- 查看检查结果
- 重启 Gateway
- 运行状态检查（30秒活动监控）

---

**提示**: 定期运行健康检查，及时发现和解决问题

---

## 任务状态检测

### 检测方法

判断 OpenClaw 是否正在处理任务，有以下三种方法（按准确性排序）：

#### 方法 1: 检查 Session Lock 文件（最准确）

```bash
# 检查是否存在 .lock 文件
ls /root/.openclaw/agents/main/sessions/*.lock 2>/dev/null

# 如果有输出 = 正在处理任务
# 如果无输出 = 空闲状态
```

**原理**: OpenClaw 在处理任务时会创建 `.lock` 文件，任务完成后自动删除。

#### 方法 2: 检查日志中的 totalActive 值

```bash
# 查看最新的活跃任务数
tail -100 /root/.openclaw/agents/main/logs/openclaw.log | grep "totalActive"

# totalActive=1 = 正在处理任务
# totalActive=0 = 空闲状态
```

**示例输出**:
```
[2024-01-15 10:30:45] INFO: Session stats: totalActive=1, totalCompleted=5
[2024-01-15 10:35:20] INFO: Session stats: totalActive=0, totalCompleted=6
```

#### 方法 3: 检查 Session 文件修改时间

```bash
# 查看最近修改的 session 文件
find /root/.openclaw/agents/main/sessions -name "*.json" -mmin -1

# 如果有文件在 1 分钟内被修改 = 可能正在处理任务
# 如果没有 = 可能空闲
```

**注意**: 此方法不够准确，建议配合方法 1 或 2 使用。

---

### 状态指标对照表

| 指标 | 处理中 | 空闲 |
|------|--------|------|
| `.lock` 文件 | 存在 | 不存在 |
| `totalActive` | = 1 | = 0 |
| Session 修改时间 | < 60秒 | > 60秒 |
| Gateway 进程 | 运行中 | 运行中 |

---

### 任务生命周期日志

完整的任务处理过程会产生以下日志：

```
# 1. 任务开始
[INFO] Session started: session_id=xxx

# 2. 任务处理中
[INFO] Session stats: totalActive=1, totalCompleted=N

# 3. 任务完成
[INFO] Session completed: session_id=xxx
[INFO] Session stats: totalActive=0, totalCompleted=N+1
```

---

### 完整检测脚本

```bash
#!/bin/bash

# OpenClaw 任务状态检测脚本

echo "=== OpenClaw 任务状态检测 ==="
echo ""

# 1. 检查 Lock 文件
echo "1. Lock 文件检测:"
LOCK_FILES=$(ls /root/.openclaw/agents/main/sessions/*.lock 2>/dev/null | wc -l)
if [ "$LOCK_FILES" -gt 0 ]; then
    echo "   ✅ 发现 $LOCK_FILES 个 lock 文件 → 正在处理任务"
    ls -lh /root/.openclaw/agents/main/sessions/*.lock
    TASK_STATUS="处理中"
else
    echo "   ⭕ 无 lock 文件 → 空闲状态"
    TASK_STATUS="空闲"
fi
echo ""

# 2. 检查 totalActive
echo "2. 日志 totalActive 检测:"
TOTAL_ACTIVE=$(tail -100 /root/.openclaw/agents/main/logs/openclaw.log 2>/dev/null | grep "totalActive" | tail -1 | grep -oP 'totalActive=\K\d+')
if [ -n "$TOTAL_ACTIVE" ]; then
    if [ "$TOTAL_ACTIVE" -gt 0 ]; then
        echo "   ✅ totalActive=$TOTAL_ACTIVE → 正在处理任务"
    else
        echo "   ⭕ totalActive=$TOTAL_ACTIVE → 空闲状态"
    fi
else
    echo "   ⚠️  无法从日志获取 totalActive 值"
fi
echo ""

# 3. 检查 Session 文件修改时间
echo "3. Session 文件活动检测:"
RECENT_SESSIONS=$(find /root/.openclaw/agents/main/sessions -name "*.json" -mmin -1 2>/dev/null | wc -l)
if [ "$RECENT_SESSIONS" -gt 0 ]; then
    echo "   ✅ 发现 $RECENT_SESSIONS 个最近修改的 session → 可能正在处理"
else
    echo "   ⭕ 无最近修改的 session → 可能空闲"
fi
echo ""

# 4. 综合判断
echo "=== 综合判断 ==="
echo "任务状态: $TASK_STATUS"
echo ""

# 5. Gateway 状态（额外信息）
echo "=== Gateway 状态 ==="
if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    echo "✅ Gateway 进程: 运行中"
    systemctl --user status openclaw-gateway.service 2>/dev/null | grep -E "(Active|Main PID|Memory|CPU)" || echo "   (无法获取详细状态)"
else
    echo "❌ Gateway 进程: 未运行"
fi
```

**使用方法**:
```bash
# 保存为脚本
cat > /root/check-openclaw-task.sh << 'EOF'
# ... 上面的脚本内容 ...
EOF

# 添加执行权限
chmod +x /root/check-openclaw-task.sh

# 运行检测
/root/check-openclaw-task.sh
```

---

### 集成到 Web 管理器

Web 管理器文件: `/root/server-tools/openclaw-web-manager-final.py`

已集成任务状态检测功能，在"运行状态"按钮中会显示：
- Gateway 运行状态
- 任务处理状态（正在处理/空闲）
- 检测详情（lock 文件或日志信息）

**更新方法**（如需重新集成）:

```bash
python3 << 'EOF'
import os

with open('/root/server-tools/openclaw-web-manager-final.py', 'r') as f:
    content = f.read()

# 添加检测函数和集成代码
# ... (完整代码见对话记录)

with open('/root/server-tools/openclaw-web-manager-final.py', 'w') as f:
    f.write(content)

print('更新完成')
EOF

# 重启 Web 管理器
pkill -f "openclaw-web-manager-final.py"
nohup python3 /root/server-tools/openclaw-web-manager-final.py > /root/web-manager.log 2>&1 &
```

---

**提示**: 
- 优先使用 `.lock` 文件检测，最准确
- `totalActive` 值可作为辅助验证
- Session 文件修改时间仅供参考
- 建议每 30-60 秒轮询一次状态
