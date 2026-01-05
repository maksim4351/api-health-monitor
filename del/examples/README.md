# Примеры использования API Health Monitor

## Базовые примеры

### Пример 1: Простая проверка API

```yaml
# config.yaml
output_format: table
apis:
  - name: Google
    url: https://www.google.com
    method: GET
    timeout: 5.0
    expected_status: 200
```

```bash
api-monitor run config.yaml
```

### Пример 2: Проверка нескольких API

```yaml
output_format: json
apis:
  - name: GitHub API
    url: https://api.github.com
    method: GET
    timeout: 5.0
    expected_status: 200
    headers:
      User-Agent: api-monitor
  
  - name: JSONPlaceholder
    url: https://jsonplaceholder.typicode.com/posts/1
    method: GET
    timeout: 5.0
    expected_status: 200
```

### Пример 3: Экспорт в CSV

```bash
api-monitor run config.yaml --format csv --output report.csv
```

## Интеграция с CI/CD

### GitHub Actions

```yaml
name: API Health Check
on: [push, pull_request]

jobs:
  check-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      - name: Check API Health
        run: api-monitor run config.yaml
```

### GitLab CI

```yaml
api-check:
  image: python:3.10
  before_script:
    - pip install -r requirements.txt
    - pip install -e .
  script:
    - api-monitor run config.yaml
```

## Мониторинг критичных сервисов

```yaml
output_format: table
log_file: monitor.log
apis:
  - name: Production API
    url: https://api.production.com/health
    method: GET
    timeout: 3.0
    expected_status: 200
  
  - name: Database Service
    url: https://db.production.com/status
    method: GET
    timeout: 2.0
    expected_status: 200
```

## Cron job для периодических проверок

```bash
# Добавить в crontab
*/5 * * * * /usr/local/bin/api-monitor run /path/to/config.yaml --format json --output /var/log/api-monitor.json
```

## Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
CMD ["api-monitor", "run", "config.yaml"]
```

