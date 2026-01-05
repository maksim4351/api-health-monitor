@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo.
echo ========================================
echo   БЫСТРАЯ ПРОВЕРКА КОДА
echo ========================================
echo.

:: 1. Проверка Python
echo [1/4] Проверка Python...
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)
echo ❌ Python не найден!
echo    Попробуйте: python, python3 или py
echo    Убедитесь что Python в PATH
pause
exit /b 1

:python_found
%PYTHON_CMD% --version
echo ✅ Python OK (команда: %PYTHON_CMD%)
echo.

:: 2. Установка зависимостей
echo [2/4] Установка зависимостей...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt
echo ✅ Зависимости установлены
echo.

:: 3. Проверка синтаксиса
echo [3/4] Проверка синтаксиса...
set "SYNTAX_ERRORS=0"

for %%f in (api_monitor\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка в: %%f
        set "SYNTAX_ERRORS=1"
    )
)

for %%f in (tests\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка в: %%f
        set "SYNTAX_ERRORS=1"
    )
)

%PYTHON_CMD% -m py_compile test_run.py >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка в: test_run.py
    set "SYNTAX_ERRORS=1"
)

if !SYNTAX_ERRORS! equ 1 (
    echo.
    echo ❌ Найдены ошибки синтаксиса!
    pause
    exit /b 1
)
echo ✅ Синтаксис OK
echo.

:: 4. Запуск тестов
echo [4/4] Запуск тестов...
%PYTHON_CMD% -m pip install --quiet pytest pytest-cov >nul 2>&1
%PYTHON_CMD% -m pytest tests/ -v --tb=short --cov=api_monitor --cov-report=html --cache-clear
if errorlevel 1 (
    echo ⚠️  Некоторые тесты не прошли
) else (
    echo ✅ Все тесты прошли!
)

echo.
echo ========================================
echo   РЕЗУЛЬТАТЫ
echo ========================================
echo.
if exist "htmlcov\index.html" (
    echo ✅ Отчёт покрытия: htmlcov\index.html
    echo    Откройте в браузере!
) else (
    echo ⚠️  htmlcov\index.html не создан
    echo    Попробуйте: pytest --cov=api_monitor --cov-report=html
)

echo.
if exist "config.yaml" (
    echo ✅ config.yaml найден
    echo    Запустите: %PYTHON_CMD% test_run.py
) else (
    echo ⚠️  config.yaml не найден
)

echo.
pause

