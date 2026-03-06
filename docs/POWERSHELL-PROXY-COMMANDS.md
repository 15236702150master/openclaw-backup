# PowerShell 正确命令（复制粘贴即可）

## 测试代理访问

```powershell
$env:HTTPS_PROXY="http://127.0.0.1:7897"
python -c "import requests; r=requests.get('https://www.google.com',proxies={'https':'http://127.0.0.1:7897'},timeout=10); print('Success' if r.status_code==200 else 'Failed')"
```

## 分析图片（Gemini API）

```powershell
$env:HTTPS_PROXY="http://127.0.0.1:7897"
$API_KEY="AIzaSyByLm8elNpvR-R16gv-kylBZXopnie25mI"
$IMAGE="/root/.openclaw/media/inbound/f3895224-94e1-437a-a772-08633757de82.png"

python -c "
import base64, requests
with open('$IMAGE', 'rb') as f:
    img = base64.b64encode(f.read()).decode()
r = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$API_KEY', json={'contents': [{'parts': [{'inline_data': {'mime_type': 'image/png', 'data': img}}, {'text': 'Describe this image in Chinese'}]}]}, proxies={'https': 'http://127.0.0.1:7897'})
print(r.json()['candidates'][0]['content']['parts'][0]['text'])
"
```

## 创建 PowerShell 脚本文件

保存为 `C:\test_proxy.ps1`:

```powershell
# 设置代理
$env:HTTPS_PROXY="http://127.0.0.1:7897"

# 测试 Google
Write-Host "测试 Google 访问..." -ForegroundColor Cyan
try {
    $r = Invoke-WebRequest -Uri "https://www.google.com" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 成功！状态码：$($r.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ 失败：$_" -ForegroundColor Red
}

# 测试 Gemini API
Write-Host "`n测试 Gemini API..." -ForegroundColor Cyan
$apiKey = "AIzaSyByLm8elNpvR-R16gv-kylBZXopnie25mI"
$imagePath = "/root/.openclaw/media/inbound/f3895224-94e1-437a-a772-08633757de82.png"

# 读取图片并转换为 base64
$imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
$imageBase64 = [System.Convert]::ToBase64String($imageBytes)

# 构建请求
$body = @{
    contents = @(
        @{
            parts = @(
                @{ inline_data = @{ mime_type = "image/png"; data = $imageBase64 } },
                @{ text = "请用中文详细描述这张图片" }
            )
        }
    )
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$apiKey" -Method Post -Body $body -Headers $headers
    Write-Host "`n✅ Gemini 分析结果:" -ForegroundColor Green
    Write-Host $response.candidates[0].content.parts[0].text
} catch {
    Write-Host "`n❌ 失败：$_" -ForegroundColor Red
}
```

运行：
```powershell
.\test_proxy.ps1
```
