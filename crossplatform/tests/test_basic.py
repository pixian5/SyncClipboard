#!/usr/bin/env python3
"""
Simple tests for SyncClipboard cross-platform edition
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_manager import ConfigManager
import tempfile


def test_config_manager():
    """Test configuration manager"""
    print("Testing ConfigManager...")
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = f.name
    
    try:
        # Test initialization
        config = ConfigManager(config_path)
        assert config.get('server_url') == 'http://localhost:5033'
        assert config.get('username') == 'your_username'
        print("✓ Config initialization works")
        
        # Test set
        config.set('server_url', 'http://example.com:5033')
        assert config.get('server_url') == 'http://example.com:5033'
        print("✓ Config set works")
        
        # Test update
        config.update({'username': 'test', 'password': 'test123'})
        assert config.get('username') == 'test'
        assert config.get('password') == 'test123'
        print("✓ Config update works")
        
        # Test save and reload
        config2 = ConfigManager(config_path)
        assert config2.get('server_url') == 'http://example.com:5033'
        assert config2.get('username') == 'test'
        print("✓ Config persistence works")
        
    finally:
        # Cleanup
        if os.path.exists(config_path):
            os.remove(config_path)
    
    print("✓ All ConfigManager tests passed\n")


def test_api_client():
    """Test API client (without actual server)"""
    print("Testing API Client...")
    
    from api_client import SyncClipboardAPI
    
    # Test initialization
    api = SyncClipboardAPI('http://localhost:5033', 'admin', 'password')
    assert api.server_url == 'http://localhost:5033'
    assert api.username == 'admin'
    print("✓ API client initialization works")
    
    print("✓ All API client tests passed\n")


def test_clipboard_manager():
    """Test clipboard manager"""
    print("Testing ClipboardManager...")
    
    from clipboard_manager import ClipboardManager
    
    # Test initialization
    clipboard = ClipboardManager()
    assert clipboard.platform in ['Windows', 'Linux', 'Darwin']
    print(f"✓ Clipboard manager initialized for {clipboard.platform}")
    
    # Test get_clipboard_data format
    data = clipboard.get_clipboard_data()
    assert 'Type' in data
    assert 'Clipboard' in data
    assert 'File' in data
    print("✓ Clipboard data format is correct")
    
    print("✓ All ClipboardManager tests passed\n")


def main():
    """Run all tests"""
    print("=" * 50)
    print("SyncClipboard Cross-Platform Tests")
    print("=" * 50 + "\n")
    
    try:
        test_config_manager()
        test_api_client()
        test_clipboard_manager()
        
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
