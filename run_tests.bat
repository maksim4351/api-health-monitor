@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Running API Health Monitor Tests
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
echo ❌ Python not found! Try: python, python3 or py
pause
exit /b 1

:python_ok
:: Install test dependencies
echo Installing dependencies...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt

:: Check pytest
%PYTHON_CMD% -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  pytest not installed. Installing...
    %PYTHON_CMD% -m pip install --quiet pytest pytest-cov
)

:: Run tests
echo.
echo Running all tests...
echo ----------------------------------------
%PYTHON_CMD% -m pytest tests/ -v --tb=short --cache-clear

echo.
echo ----------------------------------------
echo Running tests with code coverage...
echo ----------------------------------------
%PYTHON_CMD% -m pytest tests/ --cov=api_monitor --cov-report=term-missing --cov-report=html --cache-clear

echo.
if exist "htmlcov\index.html" (
    echo ✅ Coverage report saved to htmlcov\index.html
    echo    Open in browser: htmlcov\index.html
) else (
    echo ⚠️  htmlcov\index.html not created
    echo    Check that tests ran successfully
)
echo.

pause
