# Git 推送网络问题解决方案

**问题**: WSL2 推送 GitHub 网络不稳定，经常超时

---

## ✅ 方案 1: 使用 Windows 侧推送（最可靠）⭐

### 原理
Windows 有 Clash Verge 代理，网络稳定。WSL2 文件可通过 WSL 文件系统访问。

### 步骤

**在 Windows PowerShell 运行**:

```powershell
# 1. 访问 WSL2 文件系统
cd \\wsl$\Ubuntu\root\.openclaw\workspace

# 或者映射为网络驱动器
net use X: \\wsl$\Ubuntu\root\.openclaw\workspace

# 2. 设置代理
$env:HTTPS_PROXY="http://127.0.0.1:7897"
$env:HTTP_PROXY="http://127.0.0.1:7897"

# 3. 推送代码
cd X:
git push origin master
```

### 优点
- ✅ 网络稳定（Windows 代理）
- ✅ 不需要额外配置
- ✅ 直接访问 WSL2 文件

---

## ✅ 方案 2: 使用 Git Bundle（断点续传）⭐

### 原理
创建 bundle 文件，通过其他方式上传到 GitHub。

### 步骤

**WSL2 中**:
```bash
# 创建 bundle
cd /root/.openclaw/workspace
git bundle create /tmp/backup.bundle master

# 复制到 Windows 可访问位置
cp /tmp/backup.bundle /mnt/c/Users/admin/Desktop/
```

**Windows 侧**:
```powershell
# 1. 下载 bundle 文件
cd C:\Users\admin\Desktop

# 2. 克隆空仓库
git clone https://github.com/15236702150master/openclaw-backup.git temp-backup
cd temp-backup

# 3. 从 bundle 恢复
git fetch C:\Users\admin\Desktop\backup.bundle master:master
git push origin master
```

### 优点
- ✅ 支持断点续传
- ✅ 文件小（273KB）
- ✅ 可离线操作

---

## ✅ 方案 3: 使用 Gitee 作为中转（国内速度快）

### 原理
先推送到 Gitee（国内），再从 Gitee 同步到 GitHub。

### 步骤

**创建 Gitee 仓库**:
```bash
curl -X POST "https://gitee.com/api/v5/user/repos" \
  -H "Content-Type: application/json" \
  -d '{"access_token":"YOUR_GITEE_TOKEN","name":"openclaw-backup","auto_init":true}'
```

**添加远程仓库**:
```bash
cd /root/.openclaw/workspace
git remote add gitee https://gitee.com/15236702150master/openclaw-backup.git

# 推送到 Gitee（速度快）
git push gitee master

# 从 Gitee 同步到 GitHub（GitHub Actions 自动同步）
```

### 优点
- ✅ 国内推送速度快
- ✅ 可作为备用仓库
- ✅ 支持自动同步

---

## ✅ 方案 4: 使用 Git LFS + 分块推送

### 原理
将大文件用 LFS 管理，分多次推送。

### 步骤

```bash
# 安装 Git LFS
git lfs install

# 跟踪大文件
git lfs track "*.png"
git lfs track "*.pdf"

# 分块推送
git push origin master --dry-run  # 预览
git push origin master --progress 2>&1 | tee push.log
```

### 优点
- ✅ 优化大文件传输
- ✅ 支持断点续传
- ✅ 减少推送时间

---

## ✅ 方案 5: 使用 rsync 同步到 Windows 共享文件夹

### 原理
实时同步到 Windows 文件夹，由 Windows 侧负责推送。

### 步骤

**创建同步脚本** `sync-to-windows.sh`:
```bash
#!/bin/bash
# 同步到 Windows 共享文件夹
rsync -av --delete \
  /root/.openclaw/workspace/ \
  /mnt/c/Users/admin/Desktop/openclaw-backup/ \
  --exclude '.git/' \
  --exclude 'node_modules/' \
  --exclude '*.log'

echo "✅ 同步完成！Windows 侧可推送"
```

**Windows 侧自动推送脚本** `auto-push.ps1`:
```powershell
cd C:\Users\admin\Desktop\openclaw-backup
$env:HTTPS_PROXY="http://127.0.0.1:7897"
git add .
git commit -m "Auto-sync from WSL2"
git push origin master
```

### 优点
- ✅ 实时同步
- ✅ 分离备份和推送
- ✅ 可定时执行

---

## ✅ 方案 6: 使用 GitHub CLI (gh)

### 原理
gh 工具比 git 更稳定，支持重试。

### 步骤

```bash
# 安装 gh
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh -y

# 认证
gh auth login

# 推送
gh repo push origin master
```

### 优点
- ✅ 更好的错误处理
- ✅ 自动重试
- ✅ 官方工具

---

## 🎯 推荐方案组合

### 日常使用（方案 1 + 方案 2）
- **主要**: Windows 侧推送（稳定）
- **备用**: Git Bundle（断网可用）

### 灾难恢复（方案 3）
- **备用仓库**: Gitee
- **自动同步**: GitHub Actions

### 优化传输（方案 4 + 方案 5）
- **大文件**: Git LFS
- **实时同步**: rsync

---

## 📋 快速解决脚本

### WSL2 侧：创建 Bundle
```bash
#!/bin/bash
cd /root/.openclaw/workspace
git bundle create /tmp/backup.bundle master
cp /tmp/backup.bundle /mnt/c/Users/admin/Desktop/
echo "✅ Bundle 已复制到 Windows 桌面"
```

### Windows 侧：推送 Bundle
```powershell
# save as push-bundle.ps1
$bundle = "C:\Users\admin\Desktop\backup.bundle"
$temp = "C:\Users\admin\Desktop\temp-backup"

if (Test-Path $temp) {
    Remove-Item -Recurse -Force $temp
}

git clone https://github.com/15236702150master/openclaw-backup.git $temp
cd $temp
git fetch $bundle master:master
$env:HTTPS_PROXY="http://127.0.0.1:7897"
git push origin master

Write-Host "✅ 推送成功！" -ForegroundColor Green
```

---

## 💡 最佳实践

### 推送前检查
```bash
# 检查网络连接
curl -I https://github.com

# 检查代理
echo $HTTPS_PROXY

# 检查仓库状态
git status
git log --oneline -3
```

### 推送失败处理
1. 检查代理是否工作
2. 尝试使用 bundle
3. 使用 Windows 侧推送
4. 检查 GitHub 状态

### 定期备份
- 每小时：自动本地提交
- 每天：推送到 GitHub
- 每周：创建 bundle 备份

---

**推荐 BOSS 使用方案 1（Windows 侧推送）**，最简单可靠！

---
*创建时间：2026-03-06 21:27*  
*小宇* 🤖
