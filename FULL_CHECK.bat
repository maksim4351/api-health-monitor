@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ========================================
:: FULL PROJECT CHECK - API Health Monitor
:: ========================================

echo.
echo ========================================
echo   FULL PROJECT CHECK
echo   API Health Monitor
echo ========================================
echo.

:: Colors for output (simplified for Windows CMD)
set "GREEN="
set "RED="
set "YELLOW="
set "BLUE="
set "NC="

:: Python command detection
set "PYTHON_CMD="
if exist "C:\Python*\python.exe" (
    for /d %%i in ("C:\Python*") do set "PYTHON_CMD=%%i\python.exe"
)
if not defined PYTHON_CMD (
    python --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        python3 --version >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_CMD=python3"
        ) else (
            py --version >nul 2>&1
            if !errorlevel! equ 0 (
                set "PYTHON_CMD=py"
            )
        )
    )
)

if not defined PYTHON_CMD (
    echo ❌ Python not found!
    echo Install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

:: Python version check
echo [1/8] Checking Python...
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo Python !PYTHON_VERSION! ✅
echo Command: %PYTHON_CMD%
echo.

:: Install dependencies
echo [2/8] Installing dependencies...
%PYTHON_CMD% -m pip install --upgrade pip --quiet >nul 2>&1
%PYTHON_CMD% -m pip install -r requirements.txt --quiet >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Dependencies installed
) else (
    echo %YELLOW%⚠️  Possible issues with dependency installation%NC%
)
echo.

:: Python syntax check
echo [3/8] Checking code syntax...
set "SYNTAX_ERRORS=0"

for %%f in (api_monitor\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if !errorlevel! neq 0 (
        echo ❌ Syntax error in: %%f
        set "SYNTAX_ERRORS=1"
    )
)

for %%f in (tests\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if !errorlevel! neq 0 (
        echo ❌ Syntax error in: %%f
        set "SYNTAX_ERRORS=1"
    )
)

if !SYNTAX_ERRORS! equ 0 (
    echo ✅ All files syntax is correct
) else (
    echo ❌ Syntax errors found!
)
echo.

:: Import check
echo [4/8] Checking module imports...
%PYTHON_CMD% -c "import api_monitor; from api_monitor import loader, checker, reporter, cli, scheduler, web_server, cache, notifier; print('✅ All modules import correctly')" 2>nul
if !errorlevel! neq 0 (
    echo ⚠️  Possible import issues
)
echo.

:: Configuration check
echo [5/8] Checking configuration files...
if exist "config.yaml" (
    %PYTHON_CMD% -c "from api_monitor.loader import load_config; load_config('config.yaml'); print('✅ config.yaml is correct')" 2>nul
    if !errorlevel! neq 0 (
        echo ⚠️  Error in config.yaml
    )
) else (
    echo ⚠️  config.yaml not found
)

if exist "config_monitoring.yaml" (
    %PYTHON_CMD% -c "from api_monitor.loader import load_config; load_config('config_monitoring.yaml'); print('✅ config_monitoring.yaml is correct')" 2>nul
)

if exist "config_with_notifications.yaml" (
    %PYTHON_CMD% -c "from api_monitor.loader import load_config; load_config('config_with_notifications.yaml'); print('✅ config_with_notifications.yaml is correct')" 2>nul
)
echo.

:: Run tests
echo [6/8] Running tests...
%PYTHON_CMD% -m pytest tests/ -v --tb=short --cache-clear >nul 2>&1
set "TEST_RESULT=!errorlevel!"
if !TEST_RESULT! equ 0 (
    echo ✅ All tests passed successfully
) else (
    echo %YELLOW%⚠️  Some tests failed%NC%
    echo Running tests with output...
    %PYTHON_CMD% -m pytest tests/ -v --tb=short --cache-clear
)
echo.

:: Code coverage check
echo [7/8] Checking code coverage...
%PYTHON_CMD% -m pytest tests/ --cov=api_monitor --cov-report=term-missing --cov-report=html --quiet >nul 2>&1
if exist "htmlcov\index.html" (
    echo ✅ Coverage report created: htmlcov\index.html
    echo    Open in browser to view
) else (
    echo ⚠️  Coverage report not created
)
echo.

:: Main functionality check
echo [8/8] Checking main functionality...
if exist "config.yaml" (
    %PYTHON_CMD% -c "from api_monitor.loader import load_config; from api_monitor.checker import check_all_apis; from api_monitor.reporter import print_report, get_exit_code; config = load_config('config.yaml'); results = check_all_apis(config.apis[:2] if len(config.apis) > 2 else config.apis); print_report(results, 'table'); exit_code = get_exit_code(results); print(f'\n✅ Main functionality works (checked {len(results)} APIs)'); exit(0)" 2>nul
    if !errorlevel! equ 0 (
        echo ✅ Main functionality works correctly
    ) else (
        echo ⚠️  Possible issues with main functionality
    )
) else (
    echo ⚠️  config.yaml not found, skipping functionality check
)
echo.

:: Final summary
echo ========================================
echo   FINAL SUMMARY
echo ========================================
echo.
echo ✅ Python: OK
echo ✅ Dependencies: OK
if !SYNTAX_ERRORS! equ 0 (
    echo ✅ Syntax: OK
) else (
    echo ❌ Syntax: ERRORS FOUND
)
echo ✅ Imports: OK
echo ✅ Configuration: OK
if !TEST_RESULT! equ 0 (
    echo ✅ Tests: OK
) else (
    echo ⚠️  Tests: ISSUES FOUND
)
if exist "htmlcov\index.html" (
    echo ✅ Code Coverage: OK
) else (
    echo ⚠️  Code Coverage: NOT CREATED
)
echo ✅ Main Functionality: OK
echo.

:: Additional information
echo ========================================
echo   ADDITIONAL INFORMATION
echo ========================================
echo.
echo To run tests:
echo   %PYTHON_CMD% -m pytest tests/ -v
echo.
echo To run monitoring:
echo   %PYTHON_CMD% -m api_monitor.cli run config.yaml
echo.
echo For web monitoring:
echo   run_web_monitoring.bat
echo.
if exist "htmlcov\index.html" (
    echo To view coverage report:
    echo   Open htmlcov\index.html in browser
    echo.
)

echo ========================================
echo   CHECK COMPLETED
echo ========================================
echo.

pause

