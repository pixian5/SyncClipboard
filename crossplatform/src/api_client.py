"""
API Client for SyncClipboard Server
Handles communication with the SyncClipboard server API
"""
import requests
import base64
import json
from typing import Optional, Dict, Any, Tuple
from requests.auth import HTTPBasicAuth


class SyncClipboardAPI:
    """Client for SyncClipboard server API"""
    
    def __init__(self, server_url: str, username: str, password: str):
        """Initialize API client"""
        self.server_url = server_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        
        # Warn about HTTP vs HTTPS
        if self.server_url.startswith('http://') and not self.server_url.startswith('http://localhost') and not self.server_url.startswith('http://127.0.0.1'):
            import warnings
            warnings.warn(
                "Using HTTP (not HTTPS) for remote server. "
                "Credentials and clipboard data will be transmitted in plaintext. "
                "Consider using HTTPS for security.",
                UserWarning
            )
    
    def get_clipboard(self) -> Optional[Dict[str, Any]]:
        """Get clipboard content from server"""
        try:
            response = self.session.get(
                f"{self.server_url}/SyncClipboard.json",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting clipboard: {e}")
            return None
    
    def put_clipboard(self, clipboard_data: Dict[str, Any]) -> bool:
        """Upload clipboard content to server"""
        try:
            response = self.session.put(
                f"{self.server_url}/SyncClipboard.json",
                json=clipboard_data,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error putting clipboard: {e}")
            return False
    
    def upload_file(self, filename: str, file_data: bytes) -> bool:
        """Upload a file to server"""
        try:
            response = self.session.put(
                f"{self.server_url}/file/{filename}",
                data=file_data,
                timeout=30
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            return False
    
    def download_file(self, filename: str) -> Optional[bytes]:
        """Download a file from server"""
        try:
            response = self.session.get(
                f"{self.server_url}/file/{filename}",
                timeout=30
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return None
    
    def check_file_exists(self, filename: str) -> bool:
        """Check if a file exists on server"""
        try:
            response = self.session.head(
                f"{self.server_url}/file/{filename}",
                timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test connection to server"""
        try:
            response = self.session.get(
                f"{self.server_url}/SyncClipboard.json",
                timeout=5
            )
            if response.status_code == 200:
                return True, "Connection successful"
            elif response.status_code == 401:
                return False, "Authentication failed"
            else:
                return False, f"Server returned status {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed - server unreachable"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Error: {str(e)}"
