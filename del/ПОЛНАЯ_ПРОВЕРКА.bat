@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo.
echo ========================================
echo   ПОЛНАЯ ПРОВЕРКА ПРОЕКТА
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
echo [1/8] Проверка Python...
%PYTHON_CMD% --version
echo ✅ Python OK
echo.

:: Установка зависимостей
echo [2/8] Установка зависимостей...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)
echo ✅ Зависимости установлены
echo.

:: Проверка синтаксиса
echo [3/8] Проверка синтаксиса Python...
set SYNTAX_ERROR=0
for %%f in (api_monitor\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка синтаксиса в %%f
        set SYNTAX_ERROR=1
    )
)
for %%f in (tests\*.py) do (
    %PYTHON_CMD% -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка синтаксиса в %%f
        set SYNTAX_ERROR=1
    )
)
if %SYNTAX_ERROR%==1 (
    echo ❌ Обнаружены ошибки синтаксиса
    pause
    exit /b 1
)
echo ✅ Синтаксис OK
echo.

:: Проверка импортов
echo [4/8] Проверка импортов модулей...
%PYTHON_CMD% -c "from api_monitor import checker, cli, loader, reporter, scheduler, web_server; print('✅ Все модули импортируются')" 2>nul
if errorlevel 1 (
    echo ❌ Ошибка импорта модулей
    pause
    exit /b 1
)
echo ✅ Импорты OK
echo.

:: Запуск тестов
echo [5/8] Запуск тестов...
%PYTHON_CMD% -m pytest --cache-clear --cov=api_monitor --cov-report=html --cov-report=term -v
if errorlevel 1 (
    echo ⚠️ Некоторые тесты не прошли
    set TEST_FAILED=1
) else (
    echo ✅ Все тесты прошли
    set TEST_FAILED=0
)
echo.

:: Проверка конфигурации
echo [6/8] Проверка конфигурации...
if not exist "config.yaml" (
    echo ❌ Файл config.yaml не найден
    set CONFIG_OK=0
) else (
    %PYTHON_CMD% -c "from api_monitor.loader import load_config; load_config('config.yaml'); print('✅ config.yaml валиден')" 2>nul
    if errorlevel 1 (
        echo ❌ Ошибка в config.yaml
        set CONFIG_OK=0
    ) else (
        echo ✅ config.yaml OK
        set CONFIG_OK=1
    )
)
echo.

:: Проверка CLI
echo [7/8] Проверка CLI команд...
%PYTHON_CMD% -m api_monitor.cli --help >nul 2>&1
if errorlevel 1 (
    echo ❌ CLI не работает
    set CLI_OK=0
) else (
    echo ✅ CLI работает
    set CLI_OK=1
)
echo.

:: Проверка веб-сервера
echo [8/8] Проверка веб-сервера...
%PYTHON_CMD% -c "from api_monitor.web_server import WebMonitoringServer, MonitoringHandler; print('✅ Веб-сервер импортируется')" 2>nul
if errorlevel 1 (
    echo ❌ Веб-сервер не импортируется
    set WEB_OK=0
) else (
    echo ✅ Веб-сервер OK
    set WEB_OK=1
)
echo.

:: Итоговый отчет
echo ========================================
echo   ИТОГОВЫЙ ОТЧЕТ
echo ========================================
echo.

if %TEST_FAILED%==1 (
    echo ⚠️ Тесты: НЕКОТОРЫЕ НЕ ПРОШЛИ
) else (
    echo ✅ Тесты: ВСЕ ПРОШЛИ
)

if %CONFIG_OK%==1 (
    echo ✅ Конфигурация: OK
) else (
    echo ❌ Конфигурация: ОШИБКА
)

if %CLI_OK%==1 (
    echo ✅ CLI: РАБОТАЕТ
) else (
    echo ❌ CLI: НЕ РАБОТАЕТ
)

if %WEB_OK%==1 (
    echo ✅ Веб-сервер: OK
) else (
    echo ❌ Веб-сервер: ОШИБКА
)

echo.
echo 📊 Отчет покрытия: htmlcov\index.html
echo.

if %TEST_FAILED%==0 if %CONFIG_OK%==1 if %CLI_OK%==1 if %WEB_OK%==1 (
    echo ========================================
    echo   ✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!
    echo ========================================
    echo.
    echo Проект готов к использованию!
) else (
    echo ========================================
    echo   ⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ
    echo ========================================
    echo.
    echo Проверьте ошибки выше и исправьте их.
)

echo.
pause

