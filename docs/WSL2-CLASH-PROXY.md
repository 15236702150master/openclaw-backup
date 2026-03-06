# WSL2 使用 Windows Clash Verge 代理配置指南

## 问题
WSL2 无法直接访问 Windows 的 clash verge 代理端口（7890），因为：
1. clash verge 默认只监听 `127.0.0.1`（localhost）
2. WSL2 通过虚拟网卡连接，IP 是 `172.17.48.1`（从 WSL2 看 Windows）
3. Windows 防火墙可能阻止入站连接

## 解决方案

### 方案 1: 修改 Clash Verge 配置（推荐）⭐

**步骤**:
1. 打开 Clash Verge 设置
2. 找到 **监听地址** 或 **Bind Address**
3. 从 `127.0.0.1` 改为 `0.0.0.0`（允许所有接口）
4. 保存并重启 Clash Verge

**Clash 配置文件** (`config.yaml`):
```yaml
mixed-port: 7890
allow-lan: true  # 关键！允许局域网连接
bind-address: "*"  # 监听所有接口
```

**验证**:
在 WSL2 中测试：
```bash
timeout 2 bash -c "echo > /dev/tcp/172.17.48.1/7890" && echo "✅ 端口开放" || echo "❌ 端口关闭"
```

**使用代理**:
```bash
export HTTP_PROXY="http://172.17.48.1:7890"
export HTTPS_PROXY="http://172.17.48.1:7890"
```

---

### 方案 2: Windows 防火墙规则

如果已经设置 `allow-lan: true` 但还是连不上，需要添加防火墙规则：

**PowerShell（管理员）**:
```powershell
New-NetFirewallRule -DisplayName "Clash Verge WSL2" -Direction Inbound -Protocol TCP -LocalPort 7890 -Action Allow
```

---

### 方案 3: 使用 Windows 的 IP 地址

WSL2 中获取 Windows 主机 IP：
```bash
# 方法 1: 从 resolv.conf
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# 方法 2: 从路由
ip route | grep default | awk '{print $3}'

# 方法 3: 使用 wslview
hostname -I | awk '{print $1}'
```

通常是 `172.17.48.1` 或 `172.2x.x.x`

---

### 方案 4: 在 Windows 侧运行命令

如果 WSL2 网络配置复杂，可以直接在 Windows PowerShell 运行：

```powershell
# 设置代理
$env:HTTPS_PROXY="http://127.0.0.1:7890"

# 运行 Python 脚本
python analyze_image.py
```

---

## 快速测试脚本

在 WSL2 中创建测试脚本 `test_proxy.py`:

```python
import requests

proxies = {
    'http': 'http://172.17.48.1:7890',
    'https': 'http://172.17.48.1:7890'
}

try:
    response = requests.get('https://www.google.com', proxies=proxies, timeout=10)
    print(f"✅ 代理成功！状态码：{response.status_code}")
except Exception as e:
    print(f"❌ 失败：{e}")
```

运行：
```bash
python3 test_proxy.py
```

---

## 永久配置（WSL2）

添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
# WSL2 使用 Windows Clash Verge 代理
WINDOWS_HOST=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
export HTTP_PROXY="http://${WINDOWS_HOST}:7890"
export HTTPS_PROXY="http://${WINDOWS_HOST}:7890"
export http_proxy="http://${WINDOWS_HOST}:7890"
export https_proxy="http://${WINDOWS_HOST}:7890"
```

然后：
```bash
source ~/.bashrc
```

---

## 检查清单

- [ ] Clash Verge 设置 `allow-lan: true`
- [ ] Clash Verge 设置 `bind-address: "*"`
- [ ] Windows 防火墙允许 7890 端口
- [ ] WSL2 能 ping 通 Windows（172.17.48.1）
- [ ] 端口测试通过（`echo > /dev/tcp/172.17.48.1/7890`）
- [ ] 环境变量已设置

---

## 常见问题

### Q: 为什么 WSL2 不能直接访问 Windows 的 localhost？
A: WSL2 运行在轻量级虚拟机中，有独立的网络命名空间。WSL2 的 localhost 和 Windows 的 localhost 是隔离的。

### Q: 每次重启 WSL2 后 IP 会变吗？
A: 可能会变。建议使用动态获取 Windows IP 的方法（从 resolv.conf）。

### Q: Clash Verge 重启后需要重新配置吗？
A: 不需要，`allow-lan: true` 会保存在配置文件中。

---

**最后更新**: 2026-03-06  
**小宇** 🤖
