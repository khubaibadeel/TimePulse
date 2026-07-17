@echo off
setlocal
cd /d "%~dp0"

echo Preparing TimePulse development environment...
where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.12 and enable "Add Python to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements-dev.txt
if errorlevel 1 goto :error

echo.
echo Setup completed. Run RUN_TIMEPULSE.bat to start the application.
pause
exit /b 0

:error
echo.
echo Setup failed. Review the error shown above.
pause
exit /b 1
