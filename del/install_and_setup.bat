@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Установка API Health Monitor
echo ========================================
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Установите Python 3.8 или выше с https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python: %PYTHON_VERSION%
echo.

:: Обновление pip
echo [1/4] Обновление pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip обновлён
echo.

:: Установка зависимостей
echo [2/4] Установка зависимостей...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей!
    pause
    exit /b 1
)
echo ✅ Зависимости установлены
echo.

:: Установка пакета в режиме разработки
echo [3/4] Установка пакета в режиме разработки...
python -m pip install -e .
if errorlevel 1 (
    echo ❌ Ошибка установки пакета!
    pause
    exit /b 1
)
echo ✅ Пакет установлен
echo.

:: Проверка установки
echo [4/4] Проверка установки...
python -c "import api_monitor; print('✅ Модуль api_monitor импортирован успешно')" 2>nul
if errorlevel 1 (
    echo ⚠️  Модуль не может быть импортирован
)

python -m api_monitor.cli --help >nul 2>&1
if errorlevel 1 (
    echo ⚠️  CLI команда не работает
) else (
    echo ✅ CLI команда работает
)

echo.
echo ========================================
echo   Установка завершена!
echo ========================================
echo.
echo Теперь вы можете использовать:
echo   api-monitor run config.yaml
echo.
echo Или запустить тесты:
echo   run_tests.bat
echo.
pause

