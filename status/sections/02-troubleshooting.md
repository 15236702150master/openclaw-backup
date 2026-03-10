# 故障排查指南

> OpenClaw 常见问题诊断与解决方案

---

## 问题 1: 健康检查脚本日志路径错误

### 症状
- 健康检查显示 [1/10] Gateway: 日志文件不存在

### 原因
- 脚本使用了错误的日志路径 /tmp/openclaw/ 而实际路径是 /tmp/openclaw-0/

### 解决方案
```bash
# 修复日志路径
sed -i "s|/tmp/openclaw/|/tmp/openclaw-0/|g" /root/server-tools/openclaw-healthcheck.sh

# 验证修复
grep "LOG_DIR=" /root/server-tools/openclaw-healthcheck.sh
```

---

## 问题 2: 钉钉连接检查失败

### 症状
- 健康检查显示 [9/10] 钉钉: 连接失败
- 但实际钉钉已连接

### 原因
- 脚本搜索 "socket connected" 但实际日志是 "connected successfully" 或 "CONNECTED"

### 解决方案
```bash
# 修复检查逻辑
sed -i 's/grep -i "socket connected"/grep -iE "connected successfully|CONNECTED"/g' /root/server-tools/openclaw-healthcheck.sh

# 验证修复
bash /root/server-tools/openclaw-healthcheck.sh
```

---

## 问题 3: Web 管理器健康检查返回空输出

### 症状
- Web 管理器点击"健康检查"按钮无输出

### 原因
- health_check() 函数返回 result.stdout，但脚本输出到日志文件

### 解决方案
```bash
# 修改 Web 管理器读取日志文件
# 编辑 /root/server-tools/openclaw-web-manager-final.py
# 修改 health_check() 函数读取 /root/server-tools/healthcheck.log
```

---

## 问题 4: JavaScript 多行字符串错误

### 症状
- Web 管理器页面报错 "Uncaught SyntaxError: Invalid or unexpected token"

### 原因
- Python 三引号字符串保留换行符，破坏 JavaScript 字符串字面量

### 解决方案
```python
# 使用反引号模板字符串
html = f"""
<script>
const message = `这是
多行
字符串`;
</script>
"""
```

---

## 问题 5: OpenClaw 目录权限问题

### 症状
- Gateway 启动失败
- 日志显示 "Failed to load plugin" 或权限错误

### 原因
- /root/.openclaw/ 目录属于 master 用户 (uid=1000)
- Gateway 以 root 用户运行，无法访问

### 解决方案
```bash
# 修改目录所有权为 root
chown -R root:root /root/.openclaw/

# 验证
ls -ld /root/.openclaw/
```

---

## 问题 6: 旧 Gateway 进程占用端口

### 症状
- 新 Gateway 无法启动
- 端口 18789 已被占用

### 原因
- 旧的 master 用户进程仍在运行

### 解决方案
```bash
# 查找占用端口的进程
ss -tlnp | grep 18789

# 杀死旧进程
kill -9 <PID>

# 或杀死所有 openclaw-gateway 进程
pkill -9 -f openclaw-gateway

# 重新启动
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service"
```

---

## 问题 7: 模型配置检查过于严格

### 症状
- 健康检查显示 [7/10] 模型: 配置错误或未使用百炼模型
- 但实际使用的是百炼模型（如 bailian/qwen-max）

### 原因
- 脚本只检查精确名称 "bailian/qwen3.5-plus"

### 解决方案
```bash
# 修改为只检查包含 "bailian"
sed -i 's/grep -i "bailian\/qwen3.5-plus"/grep -i "bailian"/g' /root/server-tools/openclaw-healthcheck.sh

# 验证
bash /root/server-tools/openclaw-healthcheck.sh
```

---

## 问题 8: 钉钉状态检查逻辑错误

### 症状
- 钉钉已连接但检查失败

### 原因
- 搜索模式不匹配实际日志格式

### 解决方案
```bash
# 修改为搜索 CONNECTED 状态
sed -i 's/grep -iE "connected successfully|CONNECTED"/grep -i "CONNECTED"/g' /root/server-tools/openclaw-healthcheck.sh
```

---

## 问题 9: Windows 和 master 用户无法访问文件

### 症状
- Windows 访问 \\\\wsl.localhost\\Ubuntu-24.04\\root\\.openclaw 提示无权限
- master 用户无法读写文件

### 原因
- 目录所有权改为 root:root，权限 700
- 其他用户无法访问

### 解决方案：使用 ACL

#### 方法 1: 一键配置脚本
```bash
# 创建配置脚本
cat > /tmp/setup-acl.sh << 'SCRIPT'
#!/bin/bash
# 安装 ACL 工具
apt-get update > /dev/null 2>&1
apt-get install -y acl > /dev/null 2>&1

# 设置基础权限
chmod 755 /root/.openclaw/
find /root/.openclaw/ -type d -exec chmod 755 {} \\;
find /root/.openclaw/ -type f -exec chmod 644 {} \\;

# 使用 ACL 给 master 用户完整权限
setfacl -R -m u:master:rwx /root/.openclaw/

# 设置默认 ACL（新文件自动继承）
setfacl -R -d -m u:master:rwx /root/.openclaw/

echo "✅ ACL 配置完成"
ls -ld /root/.openclaw/
getfacl /root/.openclaw/ 2>/dev/null | grep -E "user:|group:|other:"
SCRIPT

# 执行脚本
bash /tmp/setup-acl.sh
```

#### 方法 2: 配置 sudo 无密码
```bash
# 创建 sudo 配置
cat > /tmp/setup-sudo.sh << 'SCRIPT'
#!/bin/bash
cat > /etc/sudoers.d/openclaw-master << 'SUDOERS'
# OpenClaw master 用户权限配置
master ALL=(ALL) NOPASSWD: /bin/systemctl --user start openclaw-gateway.service
master ALL=(ALL) NOPASSWD: /bin/systemctl --user stop openclaw-gateway.service
master ALL=(ALL) NOPASSWD: /bin/systemctl --user restart openclaw-gateway.service
master ALL=(ALL) NOPASSWD: /bin/systemctl --user status openclaw-gateway.service
master ALL=(ALL) NOPASSWD: /bin/kill
master ALL=(ALL) NOPASSWD: /usr/bin/pkill
master ALL=(ALL) NOPASSWD: /bin/journalctl
master ALL=(ALL) NOPASSWD: /bin/chmod
master ALL=(ALL) NOPASSWD: /bin/chown
SUDOERS

chmod 440 /etc/sudoers.d/openclaw-master
echo "✅ sudo 配置完成"
SCRIPT

# 执行脚本
bash /tmp/setup-sudo.sh
```

#### 验证配置
```bash
# 检查 ACL 权限
getfacl /root/.openclaw/

# 测试 master 用户访问
su - master -c "ls -la /root/.openclaw/"

# 测试 Windows 访问
# 在 Windows 文件管理器打开: \\\\wsl.localhost\\Ubuntu-24.04\\root\\.openclaw
```

---

## 完整修复脚本

```bash
#!/bin/bash
# OpenClaw 完整修复脚本

echo "🔧 开始修复 OpenClaw..."

# 1. 停止所有进程
echo "1️⃣ 停止旧进程..."
pkill -9 -f openclaw-gateway

# 2. 修复目录权限
echo "2️⃣ 修复目录权限..."
chown -R root:root /root/.openclaw/
chmod 755 /root/.openclaw/
find /root/.openclaw/ -type d -exec chmod 755 {} \\;
find /root/.openclaw/ -type f -exec chmod 644 {} \\;

# 3. 配置 ACL
echo "3️⃣ 配置 ACL 权限..."
apt-get install -y acl > /dev/null 2>&1
setfacl -R -m u:master:rwx /root/.openclaw/
setfacl -R -d -m u:master:rwx /root/.openclaw/

# 4. 修复健康检查脚本
echo "4️⃣ 修复健康检查脚本..."
sed -i "s|/tmp/openclaw/|/tmp/openclaw-0/|g" /root/server-tools/openclaw-healthcheck.sh
sed -i 's/grep -i "bailian\\/qwen3.5-plus"/grep -i "bailian"/g' /root/server-tools/openclaw-healthcheck.sh
sed -i 's/grep -iE "connected successfully|CONNECTED"/grep -i "CONNECTED"/g' /root/server-tools/openclaw-healthcheck.sh

# 5. 重启服务
echo "5️⃣ 重启 Gateway..."
sudo -u master bash -c "export XDG_RUNTIME_DIR=/run/user/1000 && systemctl --user start openclaw-gateway.service"

# 6. 等待启动
echo "6️⃣ 等待服务启动..."
sleep 5

# 7. 运行健康检查
echo "7️⃣ 运行健康检查..."
bash /root/server-tools/openclaw-healthcheck.sh

# 8. 显示结果
echo ""
echo "✅ 修复完成！健康检查结果："
tail -20 /root/server-tools/healthcheck.log
```

---

## 快速诊断命令

```bash
# 检查 Gateway 是否运行
ps aux | grep openclaw-gateway | grep -v grep

# 检查端口是否监听
ss -tlnp | grep 18789

# 查看最新错误
tail -50 /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | grep -i error

# 检查目录权限
ls -ld /root/.openclaw/
getfacl /root/.openclaw/

# 运行健康检查
bash /root/server-tools/openclaw-healthcheck.sh && tail -20 /root/server-tools/healthcheck.log
```

---

## 常见错误日志

### 插件加载失败
```
Failed to load plugin: EACCES: permission denied
```
**解决**: 检查目录权限，确保 Gateway 运行用户有访问权限

### 端口已占用
```
Error: listen EADDRINUSE: address already in use :::18789
```
**解决**: 杀死占用端口的进程，重新启动

### 配置文件错误
```
SyntaxError: Unexpected token in JSON
```
**解决**: 验证 JSON 格式，修复语法错误

### 钉钉连接失败
```
DingTalk connection failed: timeout
```
**解决**: 检查网络连接，验证钉钉配置

---

**提示**: 遇到问题先运行健康检查，根据失败项目定位问题
