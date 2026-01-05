@echo off
chcp 65001 >nul
echo ========================================
echo   📦 ДОБАВЛЕНИЕ ВСЕХ ФАЙЛОВ В GIT
echo ========================================
echo.

echo [1/5] Проверка git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен!
    echo    Установите Git: https://git-scm.com/
    pause
    exit /b 1
)
echo ✅ Git найден
echo.

echo [2/5] Проверка статуса репозитория...
if not exist .git (
    echo ⚠️  Репозиторий не инициализирован
    echo    Инициализация...
    git init
    git remote add origin https://github.com/maksim4351/api-health-monitor.git 2>nul
    echo ✅ Репозиторий инициализирован
) else (
    echo ✅ Репозиторий найден
)
echo.

echo [3/5] Добавление всех файлов...
git add api_monitor/
git add tests/
git add .github/
git add *.md
git add *.yaml
git add *.bat
git add *.py
git add *.txt
git add *.ini
git add LICENSE
git add setup.py
git add requirements.txt
git add pytest.ini
git add .gitignore
git add .gitattributes
git add .codespellrc
git add .cursorrules
echo ✅ Файлы добавлены
echo.

echo [4/5] Проверка статуса...
git status --short
echo.

echo [5/5] Создание коммита...
set /p commit_msg="Введите сообщение коммита (или Enter для 'Add all project files'): "
if "%commit_msg%"=="" set commit_msg=Add all project files
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo ⚠️  Нет изменений для коммита или ошибка
) else (
    echo ✅ Коммит создан
)
echo.

echo ========================================
echo   ✅ ГОТОВО К ОТПРАВКЕ
echo ========================================
echo.
echo 📋 Следующие шаги:
echo    1. git push -u origin main
echo    2. Или: git push -u origin master
echo.
echo 💡 Если ветка называется по-другому:
echo    git branch --show-current
echo    git push -u origin <имя_ветки>
echo.
pause

