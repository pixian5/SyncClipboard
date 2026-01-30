# SyncClipboard 跨平台实现文档
# Cross-Platform Implementation Documentation

## 概述 / Overview

这是一个使用 Python 实现的 SyncClipboard 跨平台版本，支持 Windows、macOS、Ubuntu、iOS 和 Android。

This is a Python-based cross-platform implementation of SyncClipboard that supports Windows, macOS, Ubuntu, iOS, and Android.

## 技术选型 / Technology Stack

### 后端 / Backend
- **Python 3.8+**: 核心语言 / Core language
- **requests**: HTTP 客户端 / HTTP client
- **pyperclip**: 剪贴板访问 / Clipboard access
- **Pillow**: 图片处理 / Image processing

### 桌面客户端 / Desktop Client
- **PyQt6**: GUI 框架（可选）/ GUI framework (optional)
- 系统托盘支持 / System tray support
- 自动同步 / Auto-sync

### 移动客户端 / Mobile Client
- **Progressive Web App (PWA)**: 网页应用 / Web application
- 可添加到主屏幕 / Add to home screen
- Service Worker 支持离线使用 / Offline support

## 特性 / Features

### 桌面端 Desktop
✅ 文本剪贴板同步 / Text clipboard sync
✅ 图片剪贴板同步 / Image clipboard sync
✅ 文件剪贴板同步 / File clipboard sync
✅ 自动同步守护进程 / Auto-sync daemon
✅ 系统托盘图标 / System tray icon
✅ GUI 配置界面 / GUI settings
✅ CLI 命令行工具 / CLI tool

### 移动端 Mobile
✅ 文本剪贴板同步 / Text clipboard sync
✅ 手动上传/下载 / Manual upload/download
✅ 自动同步选项 / Auto-sync option
✅ PWA 支持离线使用 / PWA offline support
✅ 添加到主屏幕 / Add to home screen

## 安装 / Installation

### Linux/macOS

```bash
cd crossplatform
chmod +x install.sh
./install.sh
```

### Windows

```cmd
cd crossplatform
install.bat
```

### 手动安装 / Manual Installation

```bash
cd crossplatform
pip install -r requirements.txt
```

## 使用方法 / Usage

### 配置 / Configuration

首次使用需要配置服务器信息 / First-time configuration:

```bash
python3 src/syncclipboard_cli.py config \
  --server http://your-server:5033 \
  --username your_username \
  --password your_password \
  --interval 5
```

### CLI 命令 / CLI Commands

```bash
# 上传剪贴板 / Upload clipboard
python3 src/syncclipboard_cli.py upload

# 下载剪贴板 / Download clipboard
python3 src/syncclipboard_cli.py download

# 智能同步 / Smart sync
python3 src/syncclipboard_cli.py sync

# 守护进程模式 / Daemon mode
python3 src/syncclipboard_cli.py daemon

# 查看状态 / Check status
python3 src/syncclipboard_cli.py status
```

### GUI 模式 / GUI Mode

```bash
python3 src/syncclipboard_gui.py
```

启动后会显示在系统托盘中 / Runs in system tray

### 移动端 Mobile

1. 在浏览器中打开 `mobile/index.html` / Open in browser
2. 或通过服务器访问 / Or access via server: `http://your-server:5033/mobile`
3. 配置服务器设置 / Configure server settings
4. 点击"添加到主屏幕" / Tap "Add to Home Screen"
5. 使用上传/下载按钮同步 / Use upload/download buttons

#### iOS
- 在 Safari 中打开 / Open in Safari
- 点击分享按钮 → 添加到主屏幕 / Share → Add to Home Screen
- 在主屏幕打开应用 / Launch from home screen

#### Android
- 在 Chrome 中打开 / Open in Chrome
- 点击菜单 → 添加到主屏幕 / Menu → Add to Home Screen
- 在主屏幕打开应用 / Launch from home screen

## 平台支持 / Platform Support

| 平台 Platform | 文本 Text | 图片 Image | 文件 Files | GUI | 守护进程 Daemon |
|--------------|-----------|-----------|-----------|-----|----------------|
| Windows      | ✅        | ✅        | ✅        | ✅  | ✅             |
| macOS        | ✅        | ✅        | ✅        | ✅  | ✅             |
| Ubuntu       | ✅        | ✅        | ✅        | ✅  | ✅             |
| iOS          | ✅        | ⚠️        | ❌        | ✅* | ⚠️**          |
| Android      | ✅        | ⚠️        | ❌        | ✅* | ⚠️**          |

* 通过 PWA 网页界面 / Via PWA web interface
** 需要保持浏览器标签打开 / Requires keeping browser tab open

## 架构说明 / Architecture

```
crossplatform/
├── src/
│   ├── config_manager.py       # 配置管理 / Configuration
│   ├── api_client.py           # API 客户端 / API client
│   ├── clipboard_manager.py    # 剪贴板管理 / Clipboard manager
│   ├── syncclipboard_cli.py    # CLI 工具 / CLI tool
│   └── syncclipboard_gui.py    # GUI 应用 / GUI app
├── mobile/
│   ├── index.html              # PWA 主页 / PWA main page
│   ├── app.js                  # PWA 逻辑 / PWA logic
│   ├── manifest.json           # PWA 清单 / PWA manifest
│   └── service-worker.js       # Service Worker
├── tests/
│   └── test_basic.py           # 基本测试 / Basic tests
├── requirements.txt            # Python 依赖 / Dependencies
├── config.json                 # 配置文件 / Config file
└── README.md                   # 说明文档 / Documentation
```

## API 兼容性 / API Compatibility

本实现完全兼容原 SyncClipboard 服务器 API:

This implementation is fully compatible with the original SyncClipboard server API:

- `GET/PUT /SyncClipboard.json` - 剪贴板元数据 / Clipboard metadata
- `GET/PUT /file/{filename}` - 文件上传下载 / File upload/download
- HTTP Basic Authentication - 身份认证 / Authentication

## 依赖说明 / Dependencies

### 必需 Required
- Python 3.8+
- requests (HTTP 客户端 / HTTP client)
- pyperclip (剪贴板访问 / Clipboard access)
- Pillow (图片处理 / Image processing)

### 可选 Optional
- PyQt6 (GUI 界面，仅桌面端 / GUI, desktop only)
- xclip 或 wl-clipboard (Linux 剪贴板支持 / Linux clipboard)

## 限制和注意事项 / Limitations

### Linux
- 需要安装 `xclip` (X11) 或 `wl-clipboard` (Wayland)
- Needs `xclip` (X11) or `wl-clipboard` (Wayland)

### Mobile PWA
- 需要 HTTPS 才能访问剪贴板 API / Requires HTTPS for Clipboard API
- 图片同步功能受限 / Limited image sync support
- 后台同步需要保持标签打开 / Background sync requires tab open

### 安全 Security
- 建议使用 HTTPS 连接服务器 / Use HTTPS for server connection
- 密码存储在本地配置文件 / Passwords stored in local config

## 性能 / Performance

- 轻量级，内存占用 < 50MB / Lightweight, < 50MB RAM
- 快速启动 < 1秒 / Fast startup < 1s
- 网络流量最小化 / Minimal network traffic

## 故障排除 / Troubleshooting

### Linux 剪贴板不工作
```bash
# 安装 xclip (X11)
sudo apt-get install xclip

# 或安装 wl-clipboard (Wayland)
sudo apt-get install wl-clipboard
```

### 移动端无法访问剪贴板
- 确保使用 HTTPS / Ensure HTTPS is used
- 检查浏览器权限 / Check browser permissions

### 连接失败
- 检查服务器 URL 是否正确 / Check server URL
- 验证用户名密码 / Verify credentials
- 确认服务器可访问 / Confirm server is accessible

## 开发 / Development

### 运行测试 Run Tests
```bash
python3 tests/test_basic.py
```

### 调试 Debugging
```bash
# CLI with verbose output
python3 src/syncclipboard_cli.py status
```

## 贡献 / Contributing

欢迎提交问题和改进建议！
Issues and improvements are welcome!

## 许可 / License

与主项目相同 / Same as parent project
