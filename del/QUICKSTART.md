# Быстрый старт

## Установка

```bash
# Установите зависимости
pip install -r requirements.txt

# Или установите как пакет (рекомендуется)
pip install -e .
```

## Первый запуск

```bash
# Запустите с примером конфигурации
api-monitor run config.yaml
```

## Создание своей конфигурации

Скопируйте `config.yaml` и отредактируйте под свои API:

```yaml
output_format: table
apis:
  - name: Мой API
    url: https://api.example.com/health
    method: GET
    timeout: 5.0
    expected_status: 200
```

## Форматы вывода

```bash
# Таблица (по умолчанию)
api-monitor run config.yaml

# JSON
api-monitor run config.yaml --format json

# CSV с сохранением в файл
api-monitor run config.yaml --format csv --output report.csv
```

## Использование в CI/CD

Инструмент возвращает:
- `0` - все API доступны
- `1` - есть недоступные API

Пример для GitHub Actions:
```yaml
- name: Check APIs
  run: api-monitor run config.yaml
```


