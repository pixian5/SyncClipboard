@echo off
REM Installation script for SyncClipboard Cross-Platform Edition (Windows)

echo =====================================
echo SyncClipboard Cross-Platform Installer
echo =====================================
echo.

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is required but not installed.
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

echo + Found Python
python --version

REM Check pip
where pip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: pip is required but not installed.
    pause
    exit /b 1
)

echo + Found pip

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo =====================================
echo + Installation complete!
echo =====================================
echo.
echo Usage:
echo   CLI Mode:   python src\syncclipboard_cli.py --help
echo   GUI Mode:   python src\syncclipboard_gui.py
echo   Daemon:     python src\syncclipboard_cli.py daemon
echo.
echo Configuration:
echo   First run:  python src\syncclipboard_cli.py config --server http://your-server:5033 --username user --password pass
echo.
echo Mobile Web App:
echo   Open mobile\index.html in a web browser
echo   Or serve via your SyncClipboard server
echo.
pause
