@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Starting API Web Monitoring
echo ========================================
echo.

set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto python_ok
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto python_ok
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto python_ok
)
echo Python not found!
echo Install Python 3.8+ from https://www.python.org/
pause
exit /b 1

:python_ok
echo Installing dependencies...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt >nul 2>&1

if not exist "config.yaml" (
    echo config.yaml file not found!
    pause
    exit /b 1
)

echo.
echo Enter check interval in seconds (e.g., 60 for checking every minute)
echo Or press Enter to use interval from config.yaml
set /p INTERVAL="Interval (seconds): "

echo.
echo Web interface will open automatically in browser
echo    Initial address: http://localhost:8080
echo    (If port is busy, a free port will be automatically selected)
echo.
echo    Press Ctrl+C to stop
echo.
echo ========================================
echo.

if "%INTERVAL%"=="" (
    %PYTHON_CMD% -m api_monitor.cli watch config.yaml --web
) else (
    %PYTHON_CMD% -m api_monitor.cli watch config.yaml --web --interval %INTERVAL%
)

pause
