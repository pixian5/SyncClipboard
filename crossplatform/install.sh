#!/bin/bash
# Installation script for SyncClipboard Cross-Platform Edition

set -e

echo "====================================="
echo "SyncClipboard Cross-Platform Installer"
echo "====================================="
echo

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi
echo "✓ Found pip3"

# Install dependencies
echo
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo
echo "====================================="
echo "✓ Installation complete!"
echo "====================================="
echo
echo "Usage:"
echo "  CLI Mode:   python3 src/syncclipboard_cli.py --help"
echo "  GUI Mode:   python3 src/syncclipboard_gui.py"
echo "  Daemon:     python3 src/syncclipboard_cli.py daemon"
echo
echo "Configuration:"
echo "  First run:  python3 src/syncclipboard_cli.py config --server http://your-server:5033 --username user --password pass"
echo
echo "Mobile Web App:"
echo "  Open mobile/index.html in a web browser"
echo "  Or serve via your SyncClipboard server"
echo
