# 快速开始指南 / Quick Start Guide

## 5分钟快速体验 / 5-Minute Quick Experience

### 1. 安装 / Installation

#### Windows
```cmd
cd crossplatform
install.bat
```

#### Linux/macOS
```bash
cd crossplatform
./install.sh
```

### 2. 配置服务器 / Configure Server

```bash
cd crossplatform
python3 src/syncclipboard_cli.py config \
  --server http://your-server:5033 \
  --username admin \
  --password password
```

### 3. 测试连接 / Test Connection

```bash
python3 src/syncclipboard_cli.py status
```

### 4. 开始使用 / Start Using

#### 方式一：CLI 模式 / CLI Mode

```bash
# 上传当前剪贴板
python3 src/syncclipboard_cli.py upload

# 下载剪贴板
python3 src/syncclipboard_cli.py download

# 后台守护进程（自动同步）
python3 src/syncclipboard_cli.py daemon
```

#### 方式二：GUI 模式 / GUI Mode

```bash
python3 src/syncclipboard_gui.py
```

程序会在系统托盘中运行 / Runs in system tray

#### 方式三：移动端 PWA / Mobile PWA

```bash
# 启动 Web 服务器
python3 src/serve_mobile.py
```

然后在手机浏览器中打开 `http://your-computer-ip:8000`

Or open in mobile browser: `http://your-computer-ip:8000`

## 使用场景 / Use Cases

### 场景一：桌面自动同步 / Desktop Auto-Sync
```bash
# 启动守护进程
python3 src/syncclipboard_cli.py daemon
```
保持终端运行，剪贴板将每5秒自动同步

Keep terminal open, clipboard syncs every 5 seconds

### 场景二：手动同步文本 / Manual Text Sync
```bash
# 1. 复制一些文本到剪贴板
# 2. 上传
python3 src/syncclipboard_cli.py upload
# 3. 在另一台设备下载
python3 src/syncclipboard_cli.py download
```

### 场景三：手机快速同步 / Mobile Quick Sync
1. 打开移动端网页
2. 配置服务器信息
3. 点击"下载"按钮获取桌面剪贴板
4. 或点击"上传"发送手机剪贴板到桌面

## 常见问题 / FAQ

### Q: Linux 提示 pyperclip 错误？
A: 安装剪贴板工具：
```bash
sudo apt-get install xclip  # X11
# 或
sudo apt-get install wl-clipboard  # Wayland
```

### Q: 移动端无法访问剪贴板？
A: 需要使用 HTTPS。可以：
1. 使用服务器的 HTTPS 地址
2. 或在本地信任的网络使用 HTTP

### Q: 如何修改同步间隔？
A: 
```bash
python3 src/syncclipboard_cli.py config --interval 10
```

### Q: 如何在后台运行？
A: 
```bash
# Linux/macOS
nohup python3 src/syncclipboard_cli.py daemon &

# Windows - 使用 GUI 模式
python3 src/syncclipboard_gui.py
```

## 性能提示 / Performance Tips

- CLI 模式最轻量，内存占用 < 30MB
- GUI 模式需要 PyQt6，内存占用 ~50MB
- 建议同步间隔 >= 5秒
- 大文件建议先压缩

## 安全建议 / Security Tips

- 使用 HTTPS 连接服务器
- 定期更改密码
- 不要在公共网络同步敏感内容
- 移动端使用时注意浏览器权限

## 下一步 / Next Steps

- 查看完整文档：`docs/IMPLEMENTATION.md`
- 运行测试：`python3 tests/test_basic.py`
- 自定义配置：编辑 `~/.config/SyncClipboard/config.json`
- 构建可执行文件：使用 PyInstaller

## 获取帮助 / Get Help

```bash
# CLI 帮助
python3 src/syncclipboard_cli.py --help
python3 src/syncclipboard_cli.py config --help
```
