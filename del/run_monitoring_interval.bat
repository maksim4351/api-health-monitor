@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo.
echo ========================================
echo   Запуск мониторинга с интервалом
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
echo ❌ Python не найден!
pause
exit /b 1

:python_ok
:: Установка зависимостей
%PYTHON_CMD% -m pip install --quiet -r requirements.txt >nul 2>&1

:: Проверка config.yaml
if not exist "config.yaml" (
    echo ❌ Файл config.yaml не найден!
    pause
    exit /b 1
)

:: Запрос интервала
echo Введите интервал проверки в секундах (например: 60 для проверки каждую минуту)
set /p INTERVAL="Интервал (секунды): "

if "%INTERVAL%"=="" (
    echo Используется интервал из config.yaml
    %PYTHON_CMD% -m api_monitor.cli watch config.yaml
) else (
    echo Используется интервал: %INTERVAL% секунд
    %PYTHON_CMD% -m api_monitor.cli watch config.yaml --interval %INTERVAL%
)

pause

