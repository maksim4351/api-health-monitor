@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Открытие HTML отчётов
echo ========================================
echo.

if exist "api_report.html" (
    echo 📊 Открываю отчёт результатов проверки API...
    start "" "api_report.html"
    timeout /t 1 >nul
) else (
    echo ⚠️  api_report.html не найден
    echo    Запустите: generate_html_report.bat
)

if exist "htmlcov\index.html" (
    echo 📈 Открываю отчёт покрытия кода...
    start "" "htmlcov\index.html"
) else (
    echo ⚠️  htmlcov\index.html не найден
    echo    Запустите: run_tests.bat или generate_html_report.bat
)

echo.
echo ✅ Готово!
timeout /t 2 >nul

