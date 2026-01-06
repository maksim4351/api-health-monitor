@echo off
chcp 65001 >nul
echo ========================================
echo   🖥️  ОТКРЫТИЕ ТЕРМИНАЛА В ПАПКЕ ПРОЕКТА
echo ========================================
echo.
echo 📍 Текущая папка: %CD%
echo.
echo Выберите терминал:
echo.
echo [1] PowerShell (рекомендуется)
echo [2] Command Prompt (CMD)
echo [3] Открыть папку в Проводнике
echo [4] Отмена
echo.
set /p choice="Ваш выбор (1-4): "

if "%choice%"=="1" (
    echo.
    echo ✅ Открываю PowerShell...
    start powershell -NoExit -Command "cd '%CD%'; Write-Host '========================================' -ForegroundColor Cyan; Write-Host '  ✅ ТЕРМИНАЛ ОТКРЫТ В ПАПКЕ ПРОЕКТА' -ForegroundColor Green; Write-Host '========================================' -ForegroundColor Cyan; Write-Host ''; Write-Host '📁 Папка: %CD%' -ForegroundColor Yellow; Write-Host ''; Write-Host '💡 Теперь можете выполнить Git команды:' -ForegroundColor Cyan; Write-Host '   git add .' -ForegroundColor Gray; Write-Host '   git commit -m \"Add project structure\"' -ForegroundColor Gray; Write-Host '   git push origin main' -ForegroundColor Gray; Write-Host ''"
    exit /b 0
)

if "%choice%"=="2" (
    echo.
    echo ✅ Открываю Command Prompt...
    start cmd /k "cd /d %CD% && echo ======================================== && echo   ✅ ТЕРМИНАЛ ОТКРЫТ В ПАПКЕ ПРОЕКТА && echo ======================================== && echo. && echo 📁 Папка: %CD% && echo. && echo 💡 Теперь можете выполнить Git команды: && echo    git add . && echo    git commit -m \"Add project structure\" && echo    git push origin main && echo."
    exit /b 0
)

if "%choice%"=="3" (
    echo.
    echo ✅ Открываю папку в Проводнике...
    explorer .
    exit /b 0
)

if "%choice%"=="4" (
    echo.
    echo ❌ Отменено
    exit /b 0
)

echo.
echo ❌ Неверный выбор!
pause
exit /b 1

