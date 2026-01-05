@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Генерация HTML отчётов
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

:: Установка зависимостей
echo [1/3] Проверка зависимостей...
%PYTHON_CMD% -m pip install --quiet -r requirements.txt

:: Проверка config.yaml
if not exist "config.yaml" (
    echo ❌ Файл config.yaml не найден!
    echo.
    echo Создайте файл config.yaml для проверки API
    pause
    exit /b 1
)

:: Генерация HTML отчёта результатов проверки API
echo [2/3] Генерация HTML отчёта результатов проверки API...
%PYTHON_CMD% -m api_monitor.cli run config.yaml --format html --output api_report.html
if errorlevel 1 (
    echo ⚠️  Ошибка при генерации отчёта (возможно, некоторые API недоступны)
)

:: Генерация HTML отчёта покрытия кода
echo [3/3] Генерация HTML отчёта покрытия кода тестами...
%PYTHON_CMD% -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pytest не установлен, пропускаем отчёт о покрытии
    echo    Установите: %PYTHON_CMD% -m pip install pytest pytest-cov
) else (
    %PYTHON_CMD% -m pytest tests/ --cov=api_monitor --cov-report=html --quiet
    if exist "htmlcov\index.html" (
        echo ✅ Отчёт о покрытии создан: htmlcov\index.html
    )
)

echo.
echo ========================================
echo   HTML отчёты готовы!
echo ========================================
echo.
echo 📊 Отчёты:
if exist "api_report.html" (
    echo    ✅ api_report.html - Отчёт результатов проверки API
)
if exist "htmlcov\index.html" (
    echo    ✅ htmlcov\index.html - Отчёт покрытия кода тестами
)
echo.
echo 💡 Как открыть:
echo    1. Дважды кликните на файл .html
echo    2. Или откройте в браузере: file:///%CD%\api_report.html
echo.
echo    Для покрытия кода: file:///%CD%\htmlcov\index.html
echo.

:: Автоматическое открытие в браузере (опционально)
set /p OPEN="Открыть отчёты в браузере? (y/n): "
if /i "%OPEN%"=="y" (
    if exist "api_report.html" (
        start "" "api_report.html"
    )
    if exist "htmlcov\index.html" (
        timeout /t 1 >nul
        start "" "htmlcov\index.html"
    )
)

pause

