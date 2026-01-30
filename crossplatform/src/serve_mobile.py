#!/usr/bin/env python3
"""
Simple HTTP server for testing the mobile PWA
"""
import http.server
import socketserver
import os
import sys

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), '..', 'mobile'), **kwargs)
    
    def end_headers(self):
        # Add headers for PWA
        self.send_header('Service-Worker-Allowed', '/')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving mobile PWA at http://localhost:{PORT}")
        print("Open this URL in your browser or mobile device")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
