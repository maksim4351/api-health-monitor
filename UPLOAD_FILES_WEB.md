# 📤 Загрузка файлов через веб-интерфейс GitHub

## ⚠️ Важно

**GitHub веб-интерфейс НЕ поддерживает загрузку папок через drag & drop!**

Нужно загружать файлы по одному, создавая папки через путь в имени файла.

---

## 📋 Пошаговая инструкция

### Для папки `api_monitor/` (9 файлов):

1. Откройте: https://github.com/maksim4351/api-health-monitor
2. Нажмите **"Add file"** → **"Create new file"**
3. В поле **"Name your file..."** введите:
   ```
   api_monitor/__init__.py
   ```
   GitHub автоматически создаст папку `api_monitor/`!
4. Откройте локальный файл `api_monitor/__init__.py` и скопируйте его содержимое
5. Вставьте содержимое в редактор GitHub
6. Прокрутите вниз, введите сообщение коммита:
   ```
   Add api_monitor/__init__.py
   ```
7. Нажмите **"Commit new file"**
8. Повторите для каждого файла:
   - `api_monitor/cache.py`
   - `api_monitor/checker.py`
   - `api_monitor/cli.py`
   - `api_monitor/loader.py`
   - `api_monitor/notifier.py`
   - `api_monitor/reporter.py`
   - `api_monitor/scheduler.py`
   - `api_monitor/web_server.py`

### Для папки `tests/` (7 файлов):

Повторите процесс, используя пути:
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_cache.py`
- `tests/test_checker.py`
- `tests/test_cli.py`
- `tests/test_loader.py`
- `tests/test_notifier.py`
- `tests/test_reporter.py`
- `tests/README.md`

### Для папки `.github/` (8 файлов):

Повторите процесс, используя пути:
- `.github/CODEOWNERS`
- `.github/FUNDING.yml`
- `.github/RELEASE_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/ISSUE_TEMPLATE/question.md`
- `.github/workflows/test.yml`

---

## ⏱️ Время выполнения

- **api_monitor/**: 9 файлов × ~2 минуты = **~18 минут**
- **tests/**: 7 файлов × ~2 минуты = **~14 минут**
- **.github/**: 8 файлов × ~2 минуты = **~16 минут**

**Итого: ~48 минут** для загрузки всех файлов

---

## 💡 Рекомендация

**Это очень долго!** Лучше использовать Git команды (5 минут) или скрипт `ADD_TO_GIT.bat`.

См. `GITHUB_UPLOAD_GUIDE.md` для инструкций по Git.

