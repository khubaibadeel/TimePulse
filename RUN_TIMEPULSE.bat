@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" TimePulse.py
) else (
    python TimePulse.py
)

if errorlevel 1 (
    echo.
    echo TimePulse stopped with an error.
    pause
)
