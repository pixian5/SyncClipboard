#!/usr/bin/env python3
"""
SyncClipboard GUI - Graphical User Interface
Cross-platform clipboard synchronization with system tray
"""
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, 
                                  QMenu, QDialog, QVBoxLayout, QHBoxLayout,
                                  QLabel, QLineEdit, QPushButton, QCheckBox,
                                  QSpinBox, QTextEdit, QMessageBox)
    from PyQt6.QtCore import QTimer, Qt
    from PyQt6.QtGui import QIcon, QAction
    HAS_QT = True
except ImportError:
    HAS_QT = False
    print("PyQt6 not available. Install with: pip install PyQt6")

from config_manager import ConfigManager
from api_client import SyncClipboardAPI
from clipboard_manager import ClipboardManager


class SettingsDialog(QDialog):
    """Settings dialog"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("SyncClipboard Settings")
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Server URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Server URL:"))
        self.url_input = QLineEdit()
        self.url_input.setText(self.config_manager.get('server_url'))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Username
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit()
        self.user_input.setText(self.config_manager.get('username'))
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)
        
        # Password
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("Password:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setText(self.config_manager.get('password'))
        pass_layout.addWidget(self.pass_input)
        layout.addLayout(pass_layout)
        
        # Auto sync
        self.auto_sync_check = QCheckBox("Enable auto-sync")
        self.auto_sync_check.setChecked(self.config_manager.get('auto_sync'))
        layout.addWidget(self.auto_sync_check)
        
        # Sync interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Sync interval (seconds):"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(3600)
        self.interval_spin.setValue(self.config_manager.get('sync_interval'))
        interval_layout.addWidget(self.interval_spin)
        layout.addLayout(interval_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(test_button)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def test_connection(self):
        """Test connection to server"""
        api = SyncClipboardAPI(
            self.url_input.text(),
            self.user_input.text(),
            self.pass_input.text()
        )
        success, message = api.test_connection()
        
        if success:
            QMessageBox.information(self, "Connection Test", f"✓ {message}")
        else:
            QMessageBox.warning(self, "Connection Test", f"✗ {message}")
    
    def save_settings(self):
        """Save settings"""
        self.config_manager.update({
            'server_url': self.url_input.text(),
            'username': self.user_input.text(),
            'password': self.pass_input.text(),
            'auto_sync': self.auto_sync_check.isChecked(),
            'sync_interval': self.interval_spin.value()
        })
        self.accept()


class SyncClipboardGUI(QMainWindow):
    """Main GUI window"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.clipboard_manager = ClipboardManager()
        self.api_client = self._create_api_client()
        
        self.setWindowTitle("SyncClipboard")
        self.setMinimumSize(600, 400)
        
        # System tray
        self.tray_icon = None
        self.init_tray()
        
        # Timer for auto-sync
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.auto_sync)
        
        self.init_ui()
        self.update_sync_timer()
        
        # Hide main window, show tray only
        self.hide()
    
    def _create_api_client(self):
        """Create API client from config"""
        return SyncClipboardAPI(
            self.config_manager.get('server_url'),
            self.config_manager.get('username'),
            self.config_manager.get('password')
        )
    
    def init_ui(self):
        """Initialize main window UI"""
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.setCentralWidget(self.status_text)
        
        self.log("SyncClipboard started")
    
    def init_tray(self):
        """Initialize system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create icon (using text as placeholder)
        # In production, use actual icon file
        from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 120, 215))
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 32, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "SC")
        painter.end()
        
        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        
        # Create menu
        tray_menu = QMenu()
        
        upload_action = QAction("Upload Clipboard", self)
        upload_action.triggered.connect(self.upload_clipboard)
        tray_menu.addAction(upload_action)
        
        download_action = QAction("Download Clipboard", self)
        download_action.triggered.connect(self.download_clipboard)
        tray_menu.addAction(download_action)
        
        sync_action = QAction("Sync Now", self)
        sync_action.triggered.connect(self.sync_now)
        tray_menu.addAction(sync_action)
        
        tray_menu.addSeparator()
        
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()
    
    def tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
    
    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.append(f"[{timestamp}] {message}")
    
    def upload_clipboard(self):
        """Upload clipboard to server"""
        try:
            self.log("Uploading clipboard...")
            clipboard_data = self.clipboard_manager.get_clipboard_data()
            
            clipboard_type = clipboard_data.get("Type", "Text")
            
            if clipboard_type == "Image":
                image_data = clipboard_data.pop("ImageData", None)
                if image_data:
                    filename = clipboard_data.get("File", "clipboard.png")
                    if not self.api_client.upload_file(filename, image_data):
                        self.log("✗ Failed to upload image")
                        self.tray_icon.showMessage("SyncClipboard", "Failed to upload image", 
                                                   QSystemTrayIcon.MessageIcon.Warning)
                        return
            
            if self.api_client.put_clipboard(clipboard_data):
                self.log("✓ Clipboard uploaded successfully")
                self.tray_icon.showMessage("SyncClipboard", "Clipboard uploaded", 
                                          QSystemTrayIcon.MessageIcon.Information)
            else:
                self.log("✗ Failed to upload clipboard")
                self.tray_icon.showMessage("SyncClipboard", "Upload failed", 
                                          QSystemTrayIcon.MessageIcon.Warning)
        except Exception as e:
            self.log(f"✗ Error: {e}")
    
    def download_clipboard(self):
        """Download clipboard from server"""
        try:
            self.log("Downloading clipboard...")
            clipboard_data = self.api_client.get_clipboard()
            
            if not clipboard_data:
                self.log("✗ Failed to download clipboard")
                return
            
            clipboard_type = clipboard_data.get("Type", "Text")
            
            if clipboard_type == "Image":
                filename = clipboard_data.get("File", "")
                if filename:
                    image_data = self.api_client.download_file(filename)
                    if image_data:
                        if self.clipboard_manager.set_image(image_data):
                            self.log("✓ Image clipboard downloaded")
                            self.tray_icon.showMessage("SyncClipboard", "Image downloaded", 
                                                      QSystemTrayIcon.MessageIcon.Information)
                        else:
                            self.log("✗ Failed to set image")
            else:
                if self.clipboard_manager.set_clipboard_data(clipboard_data):
                    content = clipboard_data.get("Clipboard", "")
                    preview = content[:30] + "..." if len(content) > 30 else content
                    self.log(f"✓ Downloaded: {preview}")
                    self.tray_icon.showMessage("SyncClipboard", "Text downloaded", 
                                              QSystemTrayIcon.MessageIcon.Information)
        except Exception as e:
            self.log(f"✗ Error: {e}")
    
    def sync_now(self):
        """Manual sync"""
        self.log("Syncing...")
        self.download_clipboard()
    
    def auto_sync(self):
        """Auto sync timer callback"""
        if self.config_manager.get('auto_sync'):
            self.download_clipboard()
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec():
            self.log("Settings saved")
            # Close old API client session
            if hasattr(self.api_client, 'session'):
                self.api_client.session.close()
            # Recreate API client with new settings
            self.api_client = self._create_api_client()
            # Update timer
            self.update_sync_timer()
    
    def update_sync_timer(self):
        """Update sync timer based on settings"""
        if self.config_manager.get('auto_sync'):
            interval = self.config_manager.get('sync_interval', 5) * 1000
            self.sync_timer.start(interval)
            self.log(f"Auto-sync enabled ({self.config_manager.get('sync_interval')}s)")
        else:
            self.sync_timer.stop()
            self.log("Auto-sync disabled")
    
    def quit_app(self):
        """Quit application"""
        self.log("Quitting...")
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle close event - minimize to tray instead"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "SyncClipboard",
            "Application minimized to system tray",
            QSystemTrayIcon.MessageIcon.Information
        )


def main():
    """Main entry point"""
    if not HAS_QT:
        print("PyQt6 is required for GUI mode")
        print("Install with: pip install PyQt6")
        print("Or use CLI mode: python syncclipboard_cli.py")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    
    window = SyncClipboardGUI()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
