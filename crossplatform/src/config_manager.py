"""
Configuration Manager for SyncClipboard
Handles loading and saving configuration settings
"""
import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "server_url": "http://localhost:5033",
        "username": "admin",
        "password": "password",
        "auto_sync": True,
        "sync_interval": 5,
        "sync_text": True,
        "sync_images": True,
        "sync_files": True,
        "last_sync": None,
        "clipboard_history_size": 100
    }
    
    def __init__(self, config_path: str = None):
        """Initialize config manager"""
        if config_path is None:
            # Default config location
            if os.name == 'nt':  # Windows
                config_dir = os.path.join(os.environ['APPDATA'], 'SyncClipboard')
            elif os.name == 'posix':
                if 'darwin' in os.sys.platform:  # macOS
                    config_dir = os.path.expanduser('~/Library/Application Support/SyncClipboard')
                else:  # Linux
                    config_dir = os.path.expanduser('~/.config/SyncClipboard')
            else:
                config_dir = os.path.expanduser('~/.syncclipboard')
            
            os.makedirs(config_dir, exist_ok=True)
            self.config_path = os.path.join(config_dir, 'config.json')
        else:
            self.config_path = config_path
        
        self.config = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**self.DEFAULT_CONFIG, **config}
            else:
                # Create default config
                self.save(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save(self, config: Dict[str, Any] = None) -> bool:
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        self.config.update(updates)
        self.save()
