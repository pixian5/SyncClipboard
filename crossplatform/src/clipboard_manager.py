"""
Clipboard Manager for SyncClipboard
Handles clipboard operations across different platforms
"""
import sys
import platform
import io
from typing import Optional, Dict, Any
from PIL import Image


class ClipboardManager:
    """Cross-platform clipboard manager"""
    
    def __init__(self):
        """Initialize clipboard manager"""
        self.platform = platform.system()
        self._init_clipboard()
    
    def _init_clipboard(self):
        """Initialize platform-specific clipboard"""
        try:
            import pyperclip
            self.pyperclip = pyperclip
        except ImportError:
            print("Warning: pyperclip not available")
            self.pyperclip = None
        
        # Try to import platform-specific clipboard modules
        if self.platform == "Windows":
            try:
                import win32clipboard
                self.win32clipboard = win32clipboard
            except ImportError:
                self.win32clipboard = None
        elif self.platform == "Darwin":  # macOS
            try:
                from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF
                self.ns_pasteboard = NSPasteboard
                self.ns_png = NSPasteboardTypePNG
                self.ns_tiff = NSPasteboardTypeTIFF
            except ImportError:
                pass
        elif self.platform == "Linux":
            # Linux will use pyperclip with xclip/wl-clipboard
            pass
    
    def get_text(self) -> Optional[str]:
        """Get text from clipboard"""
        try:
            if self.pyperclip:
                return self.pyperclip.paste()
            return None
        except Exception as e:
            print(f"Error getting text from clipboard: {e}")
            return None
    
    def set_text(self, text: str) -> bool:
        """Set text to clipboard"""
        try:
            if self.pyperclip:
                self.pyperclip.copy(text)
                return True
            return False
        except Exception as e:
            print(f"Error setting text to clipboard: {e}")
            return False
    
    def get_image(self) -> Optional[bytes]:
        """Get image from clipboard as PNG bytes"""
        try:
            if self.platform == "Windows" and self.win32clipboard:
                return self._get_image_windows()
            elif self.platform == "Darwin":
                return self._get_image_macos()
            elif self.platform == "Linux":
                return self._get_image_linux()
            return None
        except Exception as e:
            print(f"Error getting image from clipboard: {e}")
            return None
    
    def _get_image_windows(self) -> Optional[bytes]:
        """Get image from Windows clipboard"""
        try:
            import win32clipboard
            from PIL import ImageGrab
            
            img = ImageGrab.grabclipboard()
            if img:
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                return buffer.getvalue()
            return None
        except Exception as e:
            print(f"Error getting Windows clipboard image: {e}")
            return None
    
    def _get_image_macos(self) -> Optional[bytes]:
        """Get image from macOS clipboard"""
        try:
            from AppKit import NSPasteboard
            pb = NSPasteboard.generalPasteboard()
            types = pb.types()
            
            if 'public.png' in types:
                data = pb.dataForType_('public.png')
                return bytes(data)
            elif 'public.tiff' in types:
                data = pb.dataForType_('public.tiff')
                # Convert TIFF to PNG
                img = Image.open(io.BytesIO(bytes(data)))
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                return buffer.getvalue()
            return None
        except Exception as e:
            print(f"Error getting macOS clipboard image: {e}")
            return None
    
    def _get_image_linux(self) -> Optional[bytes]:
        """Get image from Linux clipboard"""
        try:
            import subprocess
            
            # Try xclip first
            try:
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
                    capture_output=True,
                    check=True
                )
                return result.stdout
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            # Try wl-paste for Wayland
            try:
                result = subprocess.run(
                    ['wl-paste', '-t', 'image/png'],
                    capture_output=True,
                    check=True
                )
                return result.stdout
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            return None
        except Exception as e:
            print(f"Error getting Linux clipboard image: {e}")
            return None
    
    def set_image(self, image_data: bytes) -> bool:
        """Set image to clipboard"""
        try:
            if self.platform == "Windows":
                return self._set_image_windows(image_data)
            elif self.platform == "Darwin":
                return self._set_image_macos(image_data)
            elif self.platform == "Linux":
                return self._set_image_linux(image_data)
            return False
        except Exception as e:
            print(f"Error setting image to clipboard: {e}")
            return False
    
    def _set_image_windows(self, image_data: bytes) -> bool:
        """Set image to Windows clipboard"""
        try:
            from PIL import Image
            import win32clipboard
            from io import BytesIO
            
            img = Image.open(BytesIO(image_data))
            
            output = BytesIO()
            img.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]  # Remove BMP header
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            print(f"Error setting Windows clipboard image: {e}")
            return False
    
    def _set_image_macos(self, image_data: bytes) -> bool:
        """Set image to macOS clipboard"""
        try:
            from AppKit import NSPasteboard, NSData
            pb = NSPasteboard.generalPasteboard()
            pb.clearContents()
            data = NSData.dataWithBytes_length_(image_data, len(image_data))
            pb.setData_forType_(data, 'public.png')
            return True
        except Exception as e:
            print(f"Error setting macOS clipboard image: {e}")
            return False
    
    def _set_image_linux(self, image_data: bytes) -> bool:
        """Set image to Linux clipboard"""
        try:
            import subprocess
            
            # Try xclip first
            try:
                proc = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard', '-t', 'image/png'],
                    stdin=subprocess.PIPE
                )
                proc.communicate(image_data)
                return proc.returncode == 0
            except FileNotFoundError:
                pass
            
            # Try wl-copy for Wayland
            try:
                proc = subprocess.Popen(
                    ['wl-copy', '-t', 'image/png'],
                    stdin=subprocess.PIPE
                )
                proc.communicate(image_data)
                return proc.returncode == 0
            except FileNotFoundError:
                pass
            
            return False
        except Exception as e:
            print(f"Error setting Linux clipboard image: {e}")
            return False
    
    def get_clipboard_data(self) -> Dict[str, Any]:
        """Get clipboard data in SyncClipboard format"""
        # Try to get image first
        image_data = self.get_image()
        if image_data:
            return {
                "Type": "Image",
                "Clipboard": "",
                "File": "clipboard.png",
                "ImageData": image_data
            }
        
        # Otherwise get text
        text = self.get_text()
        if text:
            return {
                "Type": "Text",
                "Clipboard": text,
                "File": ""
            }
        
        return {
            "Type": "Text",
            "Clipboard": "",
            "File": ""
        }
    
    def set_clipboard_data(self, data: Dict[str, Any]) -> bool:
        """Set clipboard data from SyncClipboard format"""
        clipboard_type = data.get("Type", "Text")
        
        if clipboard_type == "Text":
            content = data.get("Clipboard", "")
            return self.set_text(content)
        elif clipboard_type == "Image":
            # Image data should be downloaded separately
            return True
        
        return False
