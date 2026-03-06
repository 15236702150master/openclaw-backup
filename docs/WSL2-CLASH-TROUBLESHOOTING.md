# WSL2 连接 Windows Clash Verge 排查指南

## BOSS 已配置
- ✅ allow-lan: true
- ✅ bind-address: "*"
- ✅ 端口：7897

## 当前问题
WSL2 无法连接到 Windows 的 172.17.48.1:7897

## 排查步骤

### 1. 检查 WSL2 网络模式

在 PowerShell 中运行：
```powershell
# 查看 WSL2 的网络配置
wsl hostname -I

# 应该显示类似：172.17.x.x
```

### 2. 检查 Windows 防火墙

在 PowerShell（管理员）运行：
```powershell
# 查看 7897 端口的防火墙规则
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Clash*" -or $_.DisplayName -like "*7897*"}

# 如果没有规则，添加一个：
New-NetFirewallRule -DisplayName "Clash Verge WSL2" -Direction Inbound -Protocol TCP -LocalPort 7897 -Action Allow
```

### 3. 验证 Clash Verge 监听地址

在 Windows PowerShell 运行：
```powershell
# 查看 7897 端口监听情况
netstat -ano | findstr "7897"

# 应该看到：0.0.0.0:7897 或 *:7897
# 如果是 127.0.0.1:7897，说明还没监听所有接口
```

### 4. 测试连通性

**在 Windows PowerShell 测试**:
```powershell
# 测试本地
Test-NetConnection -ComputerName 127.0.0.1 -Port 7897

# 测试 WSL2 IP（假设 WSL2 IP 是 172.17.x.x）
Test-NetConnection -ComputerName 172.17.48.1 -Port 7897
```

**在 WSL2 测试**:
```bash
# 测试 Windows
ping 172.17.48.1

# 测试端口
timeout 2 bash -c "echo > /dev/tcp/172.17.48.1/7897" && echo "✅ 成功" || echo "❌ 失败"
```

### 5. 检查 WSL2 网络配置

创建 `/etc/wsl.conf`（如果不存在）:
```ini
[network]
generateResolvConf = true
```

然后重启 WSL2：
```powershell
# Windows PowerShell
wsl --shutdown
wsl
```

### 6. 使用 host.docker.internal（Docker Desktop 用户）

如果安装了 Docker Desktop，可以用特殊 DNS：
```bash
export HTTPS_PROXY="http://host.docker.internal:7897"
```

### 7. 获取正确的 Windows IP

在 WSL2 中：
```bash
# 方法 1: 从默认网关
ip route | grep default | awk '{print $3}'

# 方法 2: 从 nameserver
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# 方法 3: 使用 wslview 或 mDNS
host.docker.internal 2>/dev/null || echo "不可用"
```

### 8. 临时解决方案：在 Windows 侧运行

如果 WSL2 网络问题暂时解决不了，可以在 Windows PowerShell 直接运行：

```powershell
$env:HTTPS_PROXY="http://127.0.0.1:7897"
python analyze_with_gemini.py
```

---

## 快速诊断脚本

在 WSL2 创建 `diagnose.sh`:

```bash
#!/bin/bash
echo "=== WSL2 网络诊断 ==="
echo "1. Windows IP: $(ip route | grep default | awk '{print $3}')"
echo "2. DNS: $(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')"
echo "3. WSL2 IP: $(hostname -I | awk '{print $1}')"
echo ""
echo "测试连接 Windows:"
for port in 7890 7897 8080; do
  echo -n "  端口 $port: "
  timeout 1 bash -c "echo > /dev/tcp/172.17.48.1/$port" 2>/dev/null && echo "✅" || echo "❌"
done
echo ""
echo "测试 ping:"
ping -c 1 172.17.48.1 | grep -E "rtt|packets"
```

运行：
```bash
chmod +x diagnose.sh
./diagnose.sh
```

---

## 可能的原因

1. **Windows 防火墙阻止** - 最常见
2. **Clash Verge 没重启** - 配置修改后需要重启
3. **WSL2 网络隔离** - 某些网络设置下 WSL2 和 Windows 隔离
4. **端口不对** - Clash Verge 实际监听的不是 7897

---

**建议 BOSS 先检查 Windows 防火墙和 Clash Verge 是否重启！**
