@echo off
chcp 65001 >nul
echo ========================================
echo   🔐 НАСТРОЙКА ДОСТУПА К GITHUB
echo ========================================
echo.

echo [1/5] Проверка Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен!
    echo    Скачайте: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git установлен
echo.

echo [2/5] Проверка текущих настроек...
echo.
set current_name=
set current_email=
for /f "tokens=*" %%a in ('git config --global user.name 2^>nul') do set current_name=%%a
for /f "tokens=*" %%a in ('git config --global user.email 2^>nul') do set current_email=%%a

if defined current_name (
    echo ✅ Имя пользователя: %current_name%
) else (
    echo ❌ Имя пользователя не настроено
)

if defined current_email (
    echo ✅ Email: %current_email%
) else (
    echo ❌ Email не настроен
)
echo.

echo [3/5] Настройка имени и email...
echo.
if not defined current_name (
    set /p git_name="Введите ваше имя (или Enter для 'maksim4351'): "
    if "%git_name%"=="" set git_name=maksim4351
    git config --global user.name "%git_name%"
    echo ✅ Имя настроено: %git_name%
) else (
    echo ℹ️  Имя уже настроено: %current_name%
)

if not defined current_email (
    set /p git_email="Введите ваш email: "
    if not "%git_email%"=="" (
        git config --global user.email "%git_email%"
        echo ✅ Email настроен: %git_email%
    ) else (
        echo ⚠️  Email не введен, пропускаем...
    )
) else (
    echo ℹ️  Email уже настроен: %current_email%
)
echo.

echo [4/5] Проверка удаленного репозитория...
echo.
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Репозиторий не инициализирован
    echo    Инициализация...
    git init
    git remote add origin https://github.com/maksim4351/api-health-monitor.git
    echo ✅ Репозиторий инициализирован
) else (
    echo ✅ Удаленный репозиторий настроен
    git remote -v
)
echo.

echo [5/5] Инструкции по аутентификации...
echo.
echo ========================================
echo   📋 СЛЕДУЮЩИЕ ШАГИ
echo ========================================
echo.
echo 1. СОЗДАЙТЕ PERSONAL ACCESS TOKEN:
echo    https://github.com/settings/tokens
echo.
echo    • Нажмите "Generate new token" → "Generate new token (classic)"
echo    • Название: api-monitor-access
echo    • Срок: 90 дней (или "No expiration")
echo    • Права: ✅ repo (полный доступ)
echo    • Нажмите "Generate token"
echo    • ⚠️  СКОПИРУЙТЕ ТОКЕН СРАЗУ! (показывается 1 раз)
echo.
echo 2. ПРИ ВЫПОЛНЕНИИ git push:
echo    • Username: ваш логин GitHub (maksim4351)
echo    • Password: вставьте Personal Access Token
echo    (НЕ используйте обычный пароль!)
echo.
echo 3. ИЛИ ИСПОЛЬЗУЙТЕ ВЕБ-ИНТЕРФЕЙС:
echo    https://github.com/maksim4351/api-health-monitor
echo    "Add file" → "Upload files"
echo.
echo ========================================
echo   ✅ НАСТРОЙКА ЗАВЕРШЕНА
echo ========================================
echo.
echo 💡 Подробная инструкция: GITHUB_AUTH_SETUP.md
echo.
pause

