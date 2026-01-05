# Руководство по мониторингу API

## 📋 Режимы работы

### 1. Разовая проверка (по умолчанию)

**Идея:** Запустить проверку один раз и завершить работу.

**Использование:**
```bash
api-monitor run config.yaml
```

**Когда использовать:**
- ✅ Быстрая проверка API
- ✅ Интеграция в CI/CD
- ✅ Ручная проверка перед деплоем
- ✅ Тестирование конфигурации

---

### 2. Периодический мониторинг (постоянная работа)

**Идея:** Постоянно проверять API с заданным интервалом.

**Способ 1: Через config.yaml**
```yaml
# config.yaml
interval: 60  # Проверка каждые 60 секунд
apis:
  - name: My API
    url: https://api.example.com
```

Запуск:
```bash
api-monitor run config.yaml
```

**Способ 2: Через команду watch**
```bash
# С интервалом из конфига
api-monitor watch config.yaml

# С кастомным интервалом
api-monitor watch config.yaml --interval 30
```

**Способ 3: Через bat-файл (Windows)**
```cmd
run_monitoring.bat
```

**Когда использовать:**
- ✅ Мониторинг production API
- ✅ Отслеживание доступности сервисов
- ✅ Сбор статистики производительности
- ✅ SLA мониторинг

---

## 🚀 Быстрый старт

### Разовая проверка
```bash
# Простая проверка
api-monitor run config.yaml

# С сохранением в файл
api-monitor run config.yaml --format json --output report.json
```

### Постоянный мониторинг
```bash
# Каждые 60 секунд (из config.yaml)
api-monitor watch config.yaml

# Каждые 30 секунд
api-monitor watch config.yaml --interval 30

# Каждые 5 минут (300 секунд)
api-monitor watch config.yaml --interval 300
```

---

## ⚙️ Настройка периодического мониторинга

### Пример config.yaml для постоянного мониторинга

```yaml
# Интервал проверки в секундах
interval: 60  # Проверка каждую минуту

# Файл для логов
log_file: monitor.log

# Формат вывода
output_format: table

apis:
  - name: Production API
    url: https://api.production.com/health
    method: GET
    timeout: 5.0
    expected_status: 200
  
  - name: Database Service
    url: https://db.production.com/status
    method: GET
    timeout: 3.0
    expected_status: 200
```

---

## 🛑 Остановка мониторинга

**В консоли:**
- Нажмите `Ctrl+C` для корректной остановки

**В Windows:**
- Закройте окно командной строки
- Или нажмите `Ctrl+C`

---

## 📊 Примеры использования

### Мониторинг каждую минуту
```bash
api-monitor watch config.yaml --interval 60
```

### Мониторинг каждые 5 минут
```bash
api-monitor watch config.yaml --interval 300
```

### Мониторинг с сохранением в HTML
```bash
api-monitor watch config.yaml --interval 60 --format html --output reports/api_report.html
```

### Мониторинг с логированием
```yaml
# config.yaml
interval: 60
log_file: monitor.log
output_format: json
```

---

## 🔧 Запуск как сервис/демон

### Windows (Task Scheduler)

1. Создайте bat-файл `start_monitoring.bat`:
```bat
@echo off
cd /d D:\Proekt\github\api-monitor
python -m api_monitor.cli watch config.yaml
```

2. Настройте Task Scheduler:
   - Откройте Планировщик заданий
   - Создайте новое задание
   - Триггер: При входе в систему
   - Действие: Запустить программу → `start_monitoring.bat`

### Linux/Mac (systemd или cron)

**systemd service:**
```ini
[Unit]
Description=API Health Monitor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/api-monitor
ExecStart=/usr/bin/python3 -m api_monitor.cli watch /path/to/config.yaml
Restart=always

[Install]
WantedBy=multi-user.target
```

**Cron:**
```bash
# Каждые 5 минут
*/5 * * * * /usr/local/bin/api-monitor run /path/to/config.yaml
```

---

## 💡 Рекомендации

### Интервалы проверки

- **Критичные API:** 30-60 секунд
- **Важные API:** 2-5 минут
- **Обычные API:** 5-15 минут
- **Тестовые API:** 1-5 минут

### Логирование

Всегда используйте `log_file` для постоянного мониторинга:
```yaml
log_file: monitor.log
```

### Сохранение истории

Для сохранения истории используйте JSON или CSV:
```bash
api-monitor watch config.yaml --format json --output reports/report_$(date +%Y%m%d_%H%M%S).json
```

---

## 🎯 Сценарии использования

### 1. Мониторинг production API
```yaml
interval: 60
log_file: production_monitor.log
apis:
  - name: Main API
    url: https://api.production.com/health
```

### 2. Мониторинг нескольких сервисов
```yaml
interval: 120
apis:
  - name: Frontend
    url: https://frontend.example.com
  - name: Backend
    url: https://backend.example.com/api/health
  - name: Database
    url: https://db.example.com/status
```

### 3. Мониторинг с уведомлениями (будущая функция)
```yaml
interval: 60
webhook_url: https://hooks.slack.com/your-webhook
apis:
  - name: Critical API
    url: https://api.example.com
```

---

## 📝 Примечания

- При периодическом мониторинге первая проверка выполняется сразу
- Используйте `Ctrl+C` для корректной остановки
- Логи сохраняются в указанный файл (если настроен `log_file`)
- Отчёты перезаписываются при каждом запуске (если не указан уникальный `output_file`)

---

**Готово к использованию! 🚀**

