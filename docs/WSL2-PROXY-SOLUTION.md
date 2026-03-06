# WSL2 访问 Windows Clash Verge 代理 - 完整解决方案

## 问题
WSL2 无法直接访问 Windows 的 `127.0.0.1:7897`，因为 WSL2 有独立的网络命名空间。

---

## ✅ 方案 1: 使用 Windows 主机 IP（推荐）⭐

### 步骤 1: 获取 Windows 在 WSL2 中的 IP

在 WSL2 中运行：
```bash
# 方法 1: 从默认网关
ip route | grep default | awk '{print $3}'

# 方法 2: 从 resolv.conf
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# 通常是 172.17.48.1 或 172.2x.x.x
```

### 步骤 2: 配置 Clash Verge 允许局域网

**Clash Verge 配置文件** (`config.yaml`):
```yaml
mixed-port: 7897
allow-lan: true    # ✅ 关键！允许局域网
bind-address: "*"  # ✅ 监听所有接口
```

### 步骤 3: 配置 WSL2 代理

添加到 `~/.bashrc`:
```bash
# WSL2 使用 Windows Clash Verge 代理
WINDOWS_HOST=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
export HTTP_PROXY="http://${WINDOWS_HOST}:7897"
export HTTPS_PROXY="http://${WINDOWS_HOST}:7897"
export http_proxy="http://${WINDOWS_HOST}:7897"
export https_proxy="http://${WINDOWS_HOST}:7897"

# 验证
echo "代理已配置：$HTTPS_PROXY"
```

然后：
```bash
source ~/.bashrc
```

### 步骤 4: 测试

```bash
# 测试端口连通性
timeout 2 bash -c "echo > /dev/tcp/${WINDOWS_HOST}/7897" && echo "✅ 端口开放" || echo "❌ 端口关闭"

# 测试 Google 访问
curl -I --proxy http://${WINDOWS_HOST}:7897 https://www.google.com

# 测试 Gemini API
python3 -c "
import requests
proxies = {'https': 'http://${WINDOWS_HOST}:7897'}
r = requests.get('https://www.google.com', proxies=proxies, timeout=10)
print('✅ 成功!' if r.status_code == 200 else '❌ 失败')
"
```

---

## ✅ 方案 2: 使用 netsh 端口转发（PowerShell 管理员）

### 在 Windows PowerShell（管理员）运行：

```powershell
# 添加端口转发规则
netsh interface portproxy add v4tov4 listenport=7897 listenaddress=0.0.0.0 connectport=7897 connectaddress=127.0.0.1

# 查看规则
netsh interface portproxy show all

# 删除规则（如果需要）
netsh interface portproxy delete v4tov4 listenport=7897 listenaddress=0.0.0.0
```

### 然后在 WSL2 测试：

```bash
export HTTPS_PROXY="http://$(ip route | grep default | awk '{print $3}'):7897"
curl -I --proxy $HTTPS_PROXY https://www.google.com
```

---

## ✅ 方案 3: 使用 hosts.docker.internal（Docker Desktop 用户）

如果安装了 Docker Desktop for Windows：

```bash
# 在 WSL2 的 ~/.bashrc 中添加
export HTTPS_PROXY="http://host.docker.internal:7897"
```

---

## ✅ 方案 4: 修改 WSL2 网络配置（高级）

创建 `/etc/wsl.conf`:
```ini
[network]
generateResolvConf = false
```

然后编辑 `/etc/resolv.conf`:
```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

重启 WSL2：
```powershell
# Windows PowerShell
wsl --shutdown
wsl
```

---

## 🔧 故障排除

### 问题 1: 端口不通

**检查 Clash Verge 配置**:
```yaml
allow-lan: true
bind-address: "*"
```

**检查 Windows 防火墙**:
```powershell
# PowerShell 管理员
New-NetFirewallRule -DisplayName "Clash Verge WSL2" -Direction Inbound -Protocol TCP -LocalPort 7897 -Action Allow
```

### 问题 2: WSL2 IP 变化

WSL2 重启后 IP 可能变化。使用动态获取：
```bash
WINDOWS_HOST=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
```

### 问题 3: DNS 污染

在 WSL2 使用公共 DNS：
```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

---

## 📋 快速配置脚本

在 WSL2 创建 `setup_proxy.sh`:

```bash
#!/bin/bash
echo "🔧 配置 WSL2 代理..."

# 获取 Windows IP
WINDOWS_HOST=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
echo "Windows IP: $WINDOWS_HOST"

# 测试端口
echo -n "测试端口 7897... "
if timeout 2 bash -c "echo > /dev/tcp/$WINDOWS_HOST/7897" 2>/dev/null; then
    echo "✅ 开放"
else
    echo "❌ 关闭 - 请检查 Clash Verge 配置"
    exit 1
fi

# 配置环境变量
cat >> ~/.bashrc << EOF

# WSL2 代理配置 (auto-generated)
WINDOWS_HOST=\"$WINDOWS_HOST\"
export HTTP_PROXY=\"http://\${WINDOWS_HOST}:7897\"
export HTTPS_PROXY=\"http://\${WINDOWS_HOST}:7897\"
export http_proxy=\"http://\${WINDOWS_HOST}:7897\"
export https_proxy=\"http://\${WINDOWS_HOST}:7897\"
EOF

echo "✅ 代理已配置！"
echo "运行 'source ~/.bashrc' 生效"
echo "测试：curl -I --proxy http://$WINDOWS_HOST:7897 https://www.google.com"
```

运行：
```bash
chmod +x setup_proxy.sh
./setup_proxy.sh
source ~/.bashrc
```

---

## 🎯 推荐方案

**最简单**: 方案 1（配置 Clash Verge + WSL2 环境变量）

**最稳定**: 方案 2（netsh 端口转发）

**Docker 用户**: 方案 3（host.docker.internal）

---

**最后更新**: 2026-03-06  
**小宇** 🤖
