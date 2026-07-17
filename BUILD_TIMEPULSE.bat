@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Development environment not found. Run setup_development.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m PyInstaller --clean TimePulse.spec
if errorlevel 1 (
    echo.
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo Build completed: dist\TimePulse.exe
pause
