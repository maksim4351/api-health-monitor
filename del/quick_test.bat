@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Быстрый тест API Health Monitor
echo ========================================
echo.

:: Проверка Python
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
echo ❌ Python не найден! Попробуйте: python, python3 или py
pause
exit /b 1

:python_ok
:: Установка зависимостей (если нужно)
echo Проверка зависимостей...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt

:: Запуск теста
echo.
echo Запуск проверки API...
echo ----------------------------------------
%PYTHON_CMD% test_run.py

echo.
pause

