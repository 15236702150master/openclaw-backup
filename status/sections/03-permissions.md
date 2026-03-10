# 权限配置说明

> OpenClaw 多用户访问权限配置指南

---

## 权限需求

### 运行要求
- Gateway 必须以 root 用户运行（安全要求）
- master 用户需要读写所有文件
- Windows 需要通过 WSL 访问文件
- master 用户需要无密码 sudo 管理服务

### 目录结构
```
/root/.openclaw/          # 主目录（root 拥有）
├── openclaw.json         # 配置文件
├── workspace/            # 工作区
├── agents/               # Agent 数据
└── status/               # 状态文档
```

---

## 解决方案：ACL + sudo

### 为什么使用 ACL？

传统 Unix 权限只支持：
- 所有者（owner）
- 组（group）
- 其他人（others）

ACL（Access Control Lists）可以：
- 为特定用户设置权限
- 保持 root 所有权
- 不影响其他用户

---

## 配置步骤

### 1. 安装 ACL 工具

```bash
apt-get update
apt-get install -y acl
```

### 2. 设置基础权限

```bash
# 目录权限 755（rwxr-xr-x）
chmod 755 /root/.openclaw/
find /root/.openclaw/ -type d -exec chmod 755 {} \\;

# 文件权限 644（rw-r--r--）
find /root/.openclaw/ -type f -exec chmod 644 {} \\;
```

### 3. 配置 ACL 权限

```bash
# 给 master 用户完整权限（rwx）
setfacl -R -m u:master:rwx /root/.openclaw/

# 设置默认 ACL（新文件自动继承）
setfacl -R -d -m u:master:rwx /root/.openclaw/
```

### 4. 配置 sudo 无密码

```bash
# 创建 sudoers 配置文件
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

# 设置正确权限
chmod 440 /etc/sudoers.d/openclaw-master
```

---

## 一键配置脚本

### ACL 配置脚本

```bash
#!/bin/bash
# 文件: /tmp/setup-acl.sh

echo "🔧 配置 ACL 权限..."

# 安装 ACL 工具
apt-get update > /dev/null 2>&1
apt-get install -y acl > /dev/null 2>&1

# 设置基础权限
chmod 755 /root/.openclaw/
find /root/.openclaw/ -type d -exec chmod 755 {} \\;
find /root/.openclaw/ -type f -exec chmod 644 {} \\;

# 配置 ACL
setfacl -R -m u:master:rwx /root/.openclaw/
setfacl -R -d -m u:master:rwx /root/.openclaw/

echo "✅ ACL 配置完成"
echo ""
echo "📁 目录权限："
ls -ld /root/.openclaw/
echo ""
echo "🔐 ACL 权限："
getfacl /root/.openclaw/ 2>/dev/null | grep -E "user:|group:|other:"
echo ""
echo "📄 配置文件权限："
ls -lh /root/.openclaw/openclaw.json
getfacl /root/.openclaw/openclaw.json 2>/dev/null | grep "user:master"
```

### sudo 配置脚本

```bash
#!/bin/bash
# 文件: /tmp/setup-sudo.sh

echo "🔧 配置 sudo 无密码..."

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
echo ""
echo "📋 配置内容："
cat /etc/sudoers.d/openclaw-master
```

### 执行配置

```bash
# 创建并执行 ACL 配置
bash /tmp/setup-acl.sh

# 创建并执行 sudo 配置
bash /tmp/setup-sudo.sh
```

---

## 验证配置

### 检查 ACL 权限

```bash
# 查看目录 ACL
getfacl /root/.openclaw/

# 查看文件 ACL
getfacl /root/.openclaw/openclaw.json

# 检查 master 用户权限
getfacl /root/.openclaw/ | grep "user:master"
```

### 测试 master 用户访问

```bash
# 切换到 master 用户测试
su - master -c "ls -la /root/.openclaw/"

# 测试读取文件
su - master -c "cat /root/.openclaw/openclaw.json | head -5"

# 测试写入文件
su - master -c "touch /root/.openclaw/test.txt && rm /root/.openclaw/test.txt"
```

### 测试 sudo 无密码

```bash
# 切换到 master 用户测试 sudo
su - master -c "sudo systemctl --user status openclaw-gateway.service"

# 应该不需要输入密码
```

### 测试 Windows 访问

在 Windows 文件管理器中打开：
```
\\wsl.localhost\Ubuntu-24.04\root\.openclaw
```

应该能够：
- 查看所有文件
- 编辑文件
- 创建新文件

---

## 权限说明

### 目录权限（755）

```
rwxr-xr-x
|||||||
||||||└─ 其他用户可执行（进入目录）
|||||└── 其他用户可读（列出文件）
||||└─── 其他用户不可写
|||└──── 组可执行
||└───── 组可读
|└────── 组不可写
└─────── 所有者完整权限
```

### 文件权限（644）

```
rw-r--r--
|||||||||
||||||||└─ 其他用户可读
|||||||└── 其他用户不可写
||||||└─── 其他用户不可执行
|||||└──── 组可读
||||└───── 组不可写
|||└────── 组不可执行
||└─────── 所有者可读
|└──────── 所有者可写
└───────── 所有者不可执行
```

### ACL 权限

```
user:master:rwx
     |      |||
     |      ||└─ 可执行
     |      |└── 可写
     |      └─── 可读
     └────────── 用户名
```

---

## 常见问题

### Q: 为什么不直接改成 777？

A: 777 权限（rwxrwxrwx）会让所有用户都有完整权限，存在安全风险。ACL 可以精确控制特定用户的权限。

### Q: ACL 会影响性能吗？

A: ACL 对性能影响极小，现代文件系统都原生支持。

### Q: 新创建的文件会继承 ACL 吗？

A: 会的，因为我们设置了默认 ACL（-d 参数）。

### Q: 如何删除 ACL？

```bash
# 删除特定用户的 ACL
setfacl -x u:master /root/.openclaw/

# 删除所有 ACL
setfacl -b /root/.openclaw/
```

### Q: 如何查看哪些文件有 ACL？

```bash
# 查找有 ACL 的文件（ls -l 显示 + 号）
ls -la /root/.openclaw/ | grep "+"

# 或使用 getfacl
find /root/.openclaw/ -exec getfacl {} \\; 2>/dev/null | grep "user:master"
```

---

## 维护建议

### 定期检查权限

```bash
# 每周检查一次
getfacl /root/.openclaw/ | grep "user:master"
ls -ld /root/.openclaw/
```

### 新增文件后

新文件会自动继承 ACL，无需手动配置。

### 备份权限配置

```bash
# 备份 ACL
getfacl -R /root/.openclaw/ > /root/openclaw-acl-backup.txt

# 恢复 ACL
setfacl --restore=/root/openclaw-acl-backup.txt
```

---

## 安全注意事项

1. 只给必要的用户添加 ACL 权限
2. 定期审查 sudo 配置
3. 不要给普通用户 root 密码
4. 使用 sudo 日志监控操作
5. 定期更新系统和软件包

---

**提示**: ACL 配置后，Windows 和 master 用户都能正常访问，同时保持 Gateway 以 root 运行的安全性
