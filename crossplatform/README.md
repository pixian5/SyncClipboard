# SyncClipboard Cross-Platform Edition

A truly cross-platform clipboard synchronization solution supporting Windows, macOS, Ubuntu, iOS, and Android.

## Technology Stack

- **Backend**: Python 3.8+ (cross-platform CLI and daemon)
- **Desktop UI**: PyQt6 (Windows, macOS, Ubuntu)
- **Mobile**: Web-based PWA (Progressive Web App) for iOS and Android
- **API Client**: Python requests library

## Features

- ✅ Text clipboard synchronization across all platforms
- ✅ Image clipboard synchronization
- ✅ File clipboard synchronization
- ✅ Clipboard history
- ✅ Auto-sync daemon mode
- ✅ Manual sync mode
- ✅ Web UI for mobile devices

## Installation

### Desktop (Windows, macOS, Ubuntu)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/syncclipboard_gui.py

# Or run as CLI/daemon
python src/syncclipboard_cli.py
```

### Mobile (iOS, Android)

1. Open your browser
2. Navigate to `http://your-server:5033/mobile`
3. Add to home screen for PWA experience
4. Configure server settings
5. Enable automatic sync

## Configuration

Edit `config.json`:

```json
{
  "server_url": "http://your-server:5033",
  "username": "your_username",
  "password": "your_password",
  "auto_sync": true,
  "sync_interval": 5,
  "sync_text": true,
  "sync_images": true,
  "sync_files": true
}
```

## Usage

### Desktop GUI

- System tray icon for easy access
- Auto-sync in background
- Clipboard history viewer
- Quick settings

### Desktop CLI

```bash
# Start daemon
python src/syncclipboard_cli.py --daemon

# Upload current clipboard
python src/syncclipboard_cli.py --upload

# Download to clipboard
python src/syncclipboard_cli.py --download

# Show status
python src/syncclipboard_cli.py --status
```

### Mobile Web App

- Open in browser or add to home screen
- Tap "Upload" to send current clipboard to server
- Tap "Download" to get clipboard from server
- Enable "Auto Sync" for background synchronization

## Platform-Specific Notes

### Windows
- Requires Python 3.8+
- PyQt6 for GUI
- Works with Windows 10+

### macOS
- Requires Python 3.8+
- PyQt6 for GUI
- Works with macOS 10.14+

### Ubuntu (Linux)
- Requires Python 3.8+
- PyQt6 for GUI
- May need `xclip` (X11) or `wl-clipboard` (Wayland)

### iOS
- Use Safari or any browser
- "Add to Home Screen" for app-like experience
- Background sync available in Safari with PWA

### Android
- Use Chrome or any browser
- "Add to Home Screen" for app-like experience
- Background sync with service workers

## Building

### Desktop Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build for current platform
pyinstaller --onefile --windowed src/syncclipboard_gui.py
```

### Mobile PWA

The PWA is served automatically by the SyncClipboard server at `/mobile` endpoint.

## Architecture

```
crossplatform/
├── src/
│   ├── syncclipboard_cli.py      # CLI and daemon
│   ├── syncclipboard_gui.py      # Desktop GUI (PyQt6)
│   ├── api_client.py              # API communication
│   ├── clipboard_manager.py       # Clipboard operations
│   └── config_manager.py          # Configuration handling
├── mobile/
│   ├── index.html                 # PWA main page
│   ├── manifest.json              # PWA manifest
│   ├── service-worker.js          # PWA service worker
│   └── app.js                     # PWA logic
├── tests/
│   └── test_*.py                  # Unit tests
├── requirements.txt               # Python dependencies
├── config.json                    # Configuration file
└── README.md                      # This file
```

## License

Same as the parent SyncClipboard project.
