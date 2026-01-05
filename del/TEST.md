# Инструкция по тестированию и запуску

## Шаг 1: Проверка Python

Убедитесь, что Python установлен (версия 3.8 или выше):

```bash
python --version
# или
python3 --version
```

## Шаг 2: Установка зависимостей

Перейдите в директорию проекта:

```bash
cd api-monitor
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Или установите пакет в режиме разработки:

```bash
pip install -e .
```

## Шаг 3: Проверка установки

Проверьте, что команда доступна:

```bash
api-monitor --help
```

Должен вывестись список доступных команд.

## Шаг 4: Запуск с примером конфигурации

Запустите мониторинг с примером конфигурации:

```bash
api-monitor run config.yaml
```

Вы должны увидеть таблицу с результатами проверки API.

## Шаг 5: Тестирование разных форматов

### JSON формат:
```bash
api-monitor run config.yaml --format json
```

### CSV формат с сохранением:
```bash
api-monitor run config.yaml --format csv --output report.csv
```

После этого откройте файл `report.csv` - там будут результаты.

## Шаг 6: Проверка exit codes

Для проверки exit codes (важно для CI/CD):

```bash
# Запустите и проверьте код возврата
api-monitor run config.yaml
echo $?  # В Linux/Mac
# или
echo %ERRORLEVEL%  # В Windows CMD
```

Если все API доступны - код будет 0, если есть ошибки - 1.

## Альтернативный запуск (без установки пакета)

Если не хотите устанавливать пакет, можно запустить напрямую:

```bash
python -m api_monitor.cli run config.yaml
```

## Создание тестовой конфигурации

Создайте файл `test_config.yaml` для тестирования:

```yaml
output_format: table
apis:
  - name: HTTPBin Status 200
    url: https://httpbin.org/status/200
    method: GET
    timeout: 5.0
    expected_status: 200
  
  - name: HTTPBin Status 404
    url: https://httpbin.org/status/404
    method: GET
    timeout: 5.0
    expected_status: 404
```

Запустите:
```bash
api-monitor run test_config.yaml
```

## Возможные проблемы

### Проблема: "api-monitor: command not found"
**Решение**: Убедитесь, что установили пакет через `pip install -e .` или используйте `python -m api_monitor.cli`

### Проблема: "ModuleNotFoundError: No module named 'requests'"
**Решение**: Установите зависимости: `pip install -r requirements.txt`

### Проблема: "FileNotFoundError: config.yaml"
**Решение**: Убедитесь, что вы находитесь в директории `api-monitor` или укажите полный путь к конфигу

## Быстрый тест одной командой

```bash
cd api-monitor && pip install -r requirements.txt && pip install -e . && api-monitor run config.yaml
```


