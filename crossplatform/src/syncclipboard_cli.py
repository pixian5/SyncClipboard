#!/usr/bin/env python3
"""
SyncClipboard CLI - Command Line Interface
Cross-platform clipboard synchronization tool
"""
import sys
import os
import argparse
import time
import hashlib
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from api_client import SyncClipboardAPI
from clipboard_manager import ClipboardManager


class SyncClipboardCLI:
    """CLI interface for SyncClipboard"""
    
    def __init__(self, config_path=None):
        """Initialize CLI"""
        self.config_manager = ConfigManager(config_path)
        self.clipboard_manager = ClipboardManager()
        
        # Initialize API client
        self.api_client = SyncClipboardAPI(
            self.config_manager.get('server_url'),
            self.config_manager.get('username'),
            self.config_manager.get('password')
        )
        
        self.last_clipboard_hash = None
    
    def upload_clipboard(self) -> bool:
        """Upload current clipboard to server"""
        try:
            print("Getting clipboard content...")
            clipboard_data = self.clipboard_manager.get_clipboard_data()
            
            clipboard_type = clipboard_data.get("Type", "Text")
            
            if clipboard_type == "Image":
                # Upload image file first
                image_data = clipboard_data.pop("ImageData", None)
                if image_data:
                    filename = clipboard_data.get("File", "clipboard.png")
                    print(f"Uploading image: {filename}")
                    if not self.api_client.upload_file(filename, image_data):
                        print("Failed to upload image")
                        return False
            
            # Upload clipboard metadata
            print("Uploading clipboard metadata...")
            if self.api_client.put_clipboard(clipboard_data):
                print("✓ Clipboard uploaded successfully")
                self.config_manager.set('last_sync', datetime.now().isoformat())
                return True
            else:
                print("✗ Failed to upload clipboard")
                return False
        except Exception as e:
            print(f"✗ Error uploading clipboard: {e}")
            return False
    
    def download_clipboard(self) -> bool:
        """Download clipboard from server"""
        try:
            print("Downloading clipboard...")
            clipboard_data = self.api_client.get_clipboard()
            
            if not clipboard_data:
                print("✗ Failed to download clipboard")
                return False
            
            clipboard_type = clipboard_data.get("Type", "Text")
            
            if clipboard_type == "Image":
                # Download image file
                filename = clipboard_data.get("File", "")
                if filename:
                    print(f"Downloading image: {filename}")
                    image_data = self.api_client.download_file(filename)
                    if image_data:
                        if self.clipboard_manager.set_image(image_data):
                            print("✓ Image clipboard downloaded successfully")
                            self.config_manager.set('last_sync', datetime.now().isoformat())
                            return True
                        else:
                            print("✗ Failed to set image to clipboard")
                            return False
                    else:
                        print("✗ Failed to download image file")
                        return False
            else:
                # Set text clipboard
                if self.clipboard_manager.set_clipboard_data(clipboard_data):
                    content = clipboard_data.get("Clipboard", "")
                    preview = content[:50] + "..." if len(content) > 50 else content
                    print(f"✓ Text clipboard downloaded: {preview}")
                    self.config_manager.set('last_sync', datetime.now().isoformat())
                    return True
                else:
                    print("✗ Failed to set clipboard")
                    return False
        except Exception as e:
            print(f"✗ Error downloading clipboard: {e}")
            return False
    
    def sync_clipboard(self) -> bool:
        """Smart sync - upload if clipboard changed, otherwise download"""
        try:
            # Get current clipboard
            clipboard_data = self.clipboard_manager.get_clipboard_data()
            clipboard_str = str(clipboard_data)
            current_hash = hashlib.md5(clipboard_str.encode()).hexdigest()
            
            # Check if clipboard changed
            if self.last_clipboard_hash and current_hash != self.last_clipboard_hash:
                print("Clipboard changed, uploading...")
                result = self.upload_clipboard()
                self.last_clipboard_hash = current_hash
                return result
            else:
                print("Checking for updates...")
                result = self.download_clipboard()
                # Update hash after download
                clipboard_data = self.clipboard_manager.get_clipboard_data()
                clipboard_str = str(clipboard_data)
                self.last_clipboard_hash = hashlib.md5(clipboard_str.encode()).hexdigest()
                return result
        except Exception as e:
            print(f"✗ Error syncing clipboard: {e}")
            return False
    
    def daemon_mode(self):
        """Run in daemon mode with auto-sync"""
        print("Starting SyncClipboard daemon...")
        print(f"Server: {self.config_manager.get('server_url')}")
        print(f"Sync interval: {self.config_manager.get('sync_interval')} seconds")
        print("Press Ctrl+C to stop\n")
        
        # Test connection
        success, message = self.api_client.test_connection()
        if not success:
            print(f"✗ Connection test failed: {message}")
            print("Please check your configuration and server status")
            return
        
        print(f"✓ Connection test successful\n")
        
        # Initialize clipboard hash
        clipboard_data = self.clipboard_manager.get_clipboard_data()
        clipboard_str = str(clipboard_data)
        self.last_clipboard_hash = hashlib.md5(clipboard_str.encode()).hexdigest()
        
        try:
            while True:
                self.sync_clipboard()
                time.sleep(self.config_manager.get('sync_interval', 5))
        except KeyboardInterrupt:
            print("\n\nStopping daemon...")
            print("Goodbye!")
    
    def show_status(self):
        """Show current status"""
        print("=== SyncClipboard Status ===")
        print(f"Server URL: {self.config_manager.get('server_url')}")
        print(f"Username: {self.config_manager.get('username')}")
        print(f"Auto-sync: {self.config_manager.get('auto_sync')}")
        print(f"Sync interval: {self.config_manager.get('sync_interval')} seconds")
        
        last_sync = self.config_manager.get('last_sync')
        if last_sync:
            print(f"Last sync: {last_sync}")
        else:
            print("Last sync: Never")
        
        print("\nTesting connection...")
        success, message = self.api_client.test_connection()
        print(f"Connection: {message}")
    
    def configure(self, args):
        """Configure settings"""
        if args.server:
            self.config_manager.set('server_url', args.server)
            print(f"Server URL set to: {args.server}")
        
        if args.username:
            self.config_manager.set('username', args.username)
            print(f"Username set to: {args.username}")
        
        if args.password:
            self.config_manager.set('password', args.password)
            print("Password updated")
        
        if args.interval:
            self.config_manager.set('sync_interval', args.interval)
            print(f"Sync interval set to: {args.interval} seconds")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='SyncClipboard - Cross-platform clipboard synchronization'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Upload command
    subparsers.add_parser('upload', help='Upload clipboard to server')
    
    # Download command
    subparsers.add_parser('download', help='Download clipboard from server')
    
    # Sync command
    subparsers.add_parser('sync', help='Smart sync clipboard')
    
    # Daemon command
    subparsers.add_parser('daemon', help='Run in daemon mode with auto-sync')
    
    # Status command
    subparsers.add_parser('status', help='Show current status')
    
    # Configure command
    config_parser = subparsers.add_parser('config', help='Configure settings')
    config_parser.add_argument('--server', help='Server URL')
    config_parser.add_argument('--username', help='Username')
    config_parser.add_argument('--password', help='Password')
    config_parser.add_argument('--interval', type=int, help='Sync interval in seconds')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create CLI instance
    cli = SyncClipboardCLI()
    
    # Execute command
    if args.command == 'upload':
        cli.upload_clipboard()
    elif args.command == 'download':
        cli.download_clipboard()
    elif args.command == 'sync':
        cli.sync_clipboard()
    elif args.command == 'daemon':
        cli.daemon_mode()
    elif args.command == 'status':
        cli.show_status()
    elif args.command == 'config':
        cli.configure(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
