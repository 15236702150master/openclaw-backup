# 默认文件操作规则

## /root 目录文件编辑规则

对于 `/root/.openclaw/` 目录下的所有文件操作，默认使用以下方法：

### 读取文件

使用 grepSearch 工具读取文件内容：
```
grepSearch 工具
- explanation: 读取文件内容
- includePattern: **/root/.openclaw/路径/文件名
- query: .*
```

或使用命令行：
```bash
cat /root/.openclaw/路径/文件名
grep -E .* /root/.openclaw/路径/文件名
```

### 创建文件
```bash
sudo touch /root/.openclaw/路径/文件名
```

### 赋予读写权限
```bash
sudo chmod 666 /root/.openclaw/路径/文件名
```

### 写入内容
```bash
sudo bash -c "cat > /root/.openclaw/路径/文件名 << 'EOL'
文件内容
EOL"
```

### 组合操作（创建并赋权）
```bash
sudo touch /root/.openclaw/路径/文件名 && sudo chmod 666 /root/.openclaw/路径/文件名
```

## 说明

- 读取文件：优先使用 grepSearch 工具，无需命令行
- 写入文件：使用 sudo bash -c 配合 cat 和 heredoc
- 所有 `/root` 目录下的文件操作都需要 root 权限
- 使用 chmod 666 确保文件可被普通用户读写
- 系统已配置 sudo 免密码执行
