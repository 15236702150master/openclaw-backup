# 常用命令参考

> OpenClaw 日常操作命令速查手册

---

## 🚀 服务管理

### 启动服务
```bash
# 启动 Gateway
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service"

# 直接启动（前台）
/root/.nvm/versions/node/v22.22.0/bin/openclaw gateway start
```

### 停止服务
```bash
# 停止 Gateway
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user stop openclaw-gateway.service"

# 强制杀死进程
pkill -9 -f openclaw-gateway
```

### 重启服务
```bash
# 重启 Gateway
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

### 查看状态
```bash
# 服务状态
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user status openclaw-gateway.service"

# 检查进程
ps aux | grep openclaw-gateway | grep -v grep

# 检查端口
ss -tlnp | grep 18789
```

---

## 📝 日志查看

### Gateway 日志
```bash
# 实时查看今天的日志
tail -f /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log

# 查看最近 100 行
tail -100 /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log

# 搜索错误
grep -i "error|failed" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log

# 搜索钉钉日志
grep -i "dingtalk" /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | tail -20
```

### 健康检查日志
```bash
# 查看健康检查结果
tail -50 /root/server-tools/healthcheck.log

# 查看最近一次检查
tail -20 /root/server-tools/healthcheck.log
```

---

## 🔍 状态检查

### 运行健康检查
```bash
# 完整健康检查（10项）
bash /root/server-tools/openclaw-healthcheck.sh

# 查看结果
tail -20 /root/server-tools/healthcheck.log
```

### 端口检查
```bash
# 检查所有端口
ss -tlnp | grep -E "18789|18791|18792"
```

---

## ⚙️ 配置管理

### 查看配置
```bash
# 查看主配置
cat /root/.openclaw/openclaw.json

# 格式化查看
cat /root/.openclaw/openclaw.json | python3 -m json.tool
```

### 编辑配置
```bash
# 编辑配置文件
vim /root/.openclaw/openclaw.json

# 编辑后重启服务
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service"
```

---

## 🔧 进程管理

### 查看进程
```bash
# 查看 Gateway 进程
ps aux | grep openclaw-gateway | grep -v grep

# 查看资源占用
top -p $(pgrep -f openclaw-gateway)
```

---

## 📊 监控命令

### 实时监控
```bash
# 监控日志
tail -f /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log

# 监控进程
watch -n 5 "ps aux | grep openclaw-gateway | grep -v grep"
```

---

## 🔗 快捷别名

添加到 ~/.bashrc:

```bash
alias oc-start="sudo -u master bash -c 'export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service'"
alias oc-stop="sudo -u master bash -c 'export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user stop openclaw-gateway.service'"
alias oc-restart="sudo -u master bash -c 'export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user restart openclaw-gateway.service'"
alias oc-log="tail -f /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log"
alias oc-check="bash /root/server-tools/openclaw-healthcheck.sh && tail -20 /root/server-tools/healthcheck.log"
```

---

## 📞 紧急重启

```bash
# 完全重启流程
pkill -9 -f openclaw-gateway
rm -f /tmp/openclaw-0/*.lock 2>/dev/null
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service"
sleep 5
bash /root/server-tools/openclaw-healthcheck.sh
```

---

## 💡 命令最佳实践

### 进程检测

**推荐方式 - 使用 pgrep**:
```bash
# 检查进程是否运行
pgrep -f "openclaw-gateway" > /dev/null 2>&1 && echo "运行中" || echo "未运行"

# 获取进程 PID
pgrep -f "openclaw-gateway"
```

**为什么不用其他方法**:
- ❌ `systemctl --user is-active`: 依赖环境变量，容易误报
- ❌ `ps aux | grep`: 会匹配到 grep 自身
- ✅ `pgrep`: 直接、可靠、不需要环境变量

### 端口检查

**推荐方式 - 使用 ss**:
```bash
# 检查端口是否监听
ss -tlnp 2>/dev/null | grep -q ":18789" && echo "端口已监听" || echo "端口未监听"

# 查看端口详细信息
ss -tlnp | grep :18789
```

**备选方式 - 使用 netstat**:
```bash
netstat -tlnp 2>/dev/null | grep :18789
```

### 杀掉占用端口的进程

```bash
# 方法 1: 使用 lsof
kill -9 $(lsof -ti:18789)

# 方法 2: 使用 ss 查找 PID
ss -tlnp | grep :18789
# 然后手动 kill -9 <PID>
```

### JSON 文件验证

```bash
# 验证 JSON 格式
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null 2>&1 && echo "✅ 格式正确" || echo "❌ 格式错误"

# 查看格式化的 JSON
python3 -m json.tool /root/.openclaw/openclaw.json
```

### 从日志查找最新匹配项

```bash
# 使用 tac 反向读取（最新的在前）
tac /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | grep "关键字" | head -1

# 查找最新的错误
tac /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | grep -i "error" | head -5
```

### 文件备份

```bash
# 备份配置文件
cp /root/.openclaw/openclaw.json /root/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)

# 验证修改
diff /root/.openclaw/openclaw.json.backup.* /root/.openclaw/openclaw.json
```

---

## 🚫 常见陷阱

### 陷阱 1: systemctl --user 在非交互环境失败

**错误**: "Failed to connect to bus"

**原因**: 缺少 `XDG_RUNTIME_DIR` 环境变量

**解决**: 使用 pgrep 检查进程，或显式设置环境变量

### 陷阱 2: grep 匹配到自身

**问题**: `ps aux | grep xxx` 总是有结果

**原因**: grep 命令本身被匹配

**解决**: 使用 `pgrep` 或 `grep -v grep`

### 陷阱 3: 多个进程导致端口冲突

**问题**: 服务启动失败，端口被占用

**原因**: 旧进程未清理

**解决**: 启动前先 `pkill -9 -f openclaw-gateway`
