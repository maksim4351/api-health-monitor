<<<<<<< HEAD
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo.
echo ========================================
echo   Starting Continuous API Monitoring
echo ========================================
echo.

:: Python check
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_ok
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_ok
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_ok
)
echo ❌ Python not found!
pause
exit /b 1

:python_ok
:: Install dependencies
echo Installing dependencies...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt >nul 2>&1

:: Check config.yaml
if not exist "config.yaml" (
    echo ❌ config.yaml file not found!
    pause
    exit /b 1
)

echo.
echo 💡 Monitoring will run continuously
echo    Press Ctrl+C to stop
echo.
echo ========================================
echo.

:: Start monitoring
%PYTHON_CMD% -m api_monitor.cli watch config.yaml

pause
=======
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo.
echo ========================================
echo   Starting Continuous API Monitoring
echo ========================================
echo.

:: Python check
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_ok
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_ok
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_ok
)
echo ❌ Python not found!
pause
exit /b 1

:python_ok
:: Install dependencies
echo Installing dependencies...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt >nul 2>&1

:: Check config.yaml
if not exist "config.yaml" (
    echo ❌ config.yaml file not found!
    pause
    exit /b 1
)

echo.
echo 💡 Monitoring will run continuously
echo    Press Ctrl+C to stop
echo.
echo ========================================
echo.

:: Start monitoring
%PYTHON_CMD% -m api_monitor.cli watch config.yaml

pause
>>>>>>> master
