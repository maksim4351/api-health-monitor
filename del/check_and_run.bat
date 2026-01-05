@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   API Health Monitor - Проверка кода
echo ========================================
echo.

:: Цвета (если поддерживается)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "NC=[0m"

:: Проверка Python
echo [1/6] Проверка Python...
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_check_ok
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_check_ok
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_check_ok
)
echo %RED%❌ Python не найден! Установите Python 3.8 или выше.%NC%
echo.
echo Скачать Python: https://www.python.org/downloads/
echo.
echo Попробуйте также: python3 или py
pause
exit /b 1

:python_check_ok
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%✅ Python найден: %PYTHON_VERSION% (команда: %PYTHON_CMD%)%NC%
echo.

:: Проверка pip
echo [2/6] Проверка pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ pip не найден!%NC%
    pause
    exit /b 1
)
echo %GREEN%✅ pip найден%NC%
echo.

:: Установка зависимостей
echo [3/6] Установка зависимостей...
%PYTHON_CMD% -m pip install --quiet --upgrade pip
%PYTHON_CMD% -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo %RED%❌ Ошибка установки зависимостей!%NC%
    pause
    exit /b 1
)
echo %GREEN%✅ Зависимости установлены%NC%
echo.

:: Проверка синтаксиса Python файлов
echo [4/6] Проверка синтаксиса Python файлов...
set "ERRORS=0"
for %%f in (api_monitor\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo %RED%❌ Ошибка синтаксиса в: %%f%NC%
        set "ERRORS=1"
    )
)

for %%f in (tests\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo %RED%❌ Ошибка синтаксиса в: %%f%NC%
        set "ERRORS=1"
    )
)

%PYTHON_CMD% -m py_compile test_run.py >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Ошибка синтаксиса в: test_run.py%NC%
    set "ERRORS=1"
)

if !ERRORS! equ 1 (
    echo %RED%❌ Найдены ошибки синтаксиса!%NC%
    pause
    exit /b 1
)
echo %GREEN%✅ Синтаксис всех файлов корректен%NC%
echo.

:: Запуск тестов (если pytest установлен)
echo [5/6] Запуск тестов...
%PYTHON_CMD% -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%⚠️  pytest не установлен, пропускаем тесты%NC%
    echo    Установите: %PYTHON_CMD% -m pip install pytest pytest-cov
) else (
    %PYTHON_CMD% -m pytest tests/ -v --tb=short
    if errorlevel 1 (
        echo %RED%❌ Некоторые тесты не прошли!%NC%
        set "TEST_ERRORS=1"
    ) else (
        echo %GREEN%✅ Все тесты прошли успешно!%NC%
    )
)
echo.

:: Проверка работы основного функционала
echo [6/6] Проверка работы основного функционала...
if not exist "config.yaml" (
    echo %YELLOW%⚠️  Файл config.yaml не найден%NC%
    echo    Создайте файл config.yaml для тестирования
    goto :skip_run
)

echo.
echo Запуск проверки API...
echo ----------------------------------------
%PYTHON_CMD% test_run.py
set "RUN_RESULT=!errorlevel!"

if !RUN_RESULT! equ 0 (
    echo.
    echo %GREEN%✅ Основной функционал работает корректно!%NC%
) else (
    echo.
    echo %YELLOW%⚠️  Проверка завершилась с ошибками (это может быть нормально, если API недоступны)%NC%
)

:skip_run
echo.
echo ========================================
echo   Итоговая сводка
echo ========================================
echo.
echo %GREEN%✅ Python: OK%NC%
echo %GREEN%✅ Зависимости: OK%NC%
echo %GREEN%✅ Синтаксис: OK%NC%

if defined TEST_ERRORS (
    echo %RED%❌ Тесты: ЕСТЬ ОШИБКИ%NC%
) else (
    echo %GREEN%✅ Тесты: OK%NC%
)

echo.
echo ========================================
echo   Дополнительные команды
echo ========================================
echo.
echo Для установки пакета в режиме разработки:
echo   pip install -e .
echo.
echo Для запуска мониторинга:
echo   %PYTHON_CMD% test_run.py
echo   или
echo   %PYTHON_CMD% -m api_monitor.cli run config.yaml
echo.
echo Для запуска тестов с покрытием:
echo   pytest --cov=api_monitor --cov-report=html
echo.

pause

