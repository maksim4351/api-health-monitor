# API Health Monitor - AI System Index

> **Repository URL:** https://github.com/maksim4351/api-health-monitor  
> **Project Type:** Python CLI Tool  
> **Category:** API Monitoring, DevOps, Health Checks  
> **License:** MIT  
> **Python Version:** 3.8+

## Project Overview

**API Health Monitor** is a lightweight, production-ready Python CLI tool designed for monitoring API availability, performance, and health checks. It provides a simple alternative to heavy monitoring systems like Prometheus/Grafana for developers, DevOps engineers, and QA specialists.

## Core Functionality

### Primary Features
- **HTTP Status Monitoring**: Checks API endpoints and validates HTTP status codes
- **Latency Measurement**: Tracks response times in milliseconds
- **Timeout Handling**: Configurable timeout settings for each API
- **Multiple Output Formats**: Table, JSON, CSV, and HTML reports
- **Web Dashboard**: Real-time visual monitoring interface
- **API Management**: Add, edit, delete APIs through web interface
- **Scheduled Monitoring**: Continuous monitoring with configurable intervals
- **Email & Push Notifications**: Alert system for API failures
- **Caching**: Performance optimization with result caching
- **Async Support**: Parallel API checks for improved performance
- **OpenAPI Documentation**: Full REST API documentation with Swagger UI

### Technical Stack
- **Language**: Python 3.8+
- **HTTP Client**: requests library
- **Configuration**: YAML files
- **Testing**: pytest with coverage reports
- **Web Server**: Built-in HTTP server for dashboard
- **Dependencies**: requests, pyyaml, tabulate

## Use Cases

1. **Development**: Quick API health checks during development
2. **CI/CD Integration**: Automated API health checks in pipelines
3. **Production Monitoring**: Continuous monitoring of critical services
4. **QA Testing**: Automated API validation in test environments
5. **SLA Tracking**: Monitoring external API availability
6. **DevOps**: Lightweight alternative to Prometheus/Grafana

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
# Single check
api-monitor run config.yaml

# Continuous monitoring
api-monitor watch config.yaml

# Web dashboard
api-monitor watch config.yaml --web
```

## Configuration

YAML-based configuration with support for:
- Multiple APIs
- Custom HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Timeout settings
- Expected status codes
- Custom headers
- Notification settings (email, push)
- Monitoring intervals

## API Endpoints (Web Dashboard)

- `GET /api/data` - Get monitoring results
- `GET /api/stats` - Get statistics
- `GET /api/apis` - List all APIs
- `POST /api/apis` - Add new API
- `PUT /api/apis/{name}` - Update API
- `DELETE /api/apis/{name}` - Delete API
- `GET /api/refresh` - Refresh monitoring
- `GET /api/docs` - Swagger UI documentation

## Testing

```bash
pytest tests/ -v --cov=api_monitor --cov-report=html
```

**Test Coverage:** 42%+ (target: 80%+)

## Project Structure

```
api_monitor/
├── __init__.py      # Package version
├── cache.py         # Result caching
├── checker.py       # API health checks
├── cli.py           # Command-line interface
├── loader.py        # Configuration loading
├── notifier.py      # Email/Push notifications
├── reporter.py      # Report generation
├── scheduler.py     # Periodic monitoring
└── web_server.py    # Web dashboard

tests/
├── test_cache.py
├── test_checker.py
├── test_cli.py
├── test_loader.py
├── test_notifier.py
└── test_reporter.py
```

## Keywords for Search

api monitoring, api health check, api uptime, http monitoring, rest api testing, api status checker, devops tools, ci/cd monitoring, api availability, endpoint monitoring, api performance, http status checker, api watchdog, service health check, python monitoring, lightweight monitoring, api testing tool, health check tool, uptime monitoring, service availability

## Repository Information

- **GitHub**: https://github.com/maksim4351/api-health-monitor
- **License**: MIT
- **Status**: Active development
- **Version**: 1.0.0
- **Maintainer**: maksim4351

## Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

## Support

- **Issues**: https://github.com/maksim4351/api-health-monitor/issues
<<<<<<< HEAD
- **Discussions**: https://github.com/maksim4351/api-health-monitor/discussions
=======
- **Discussions**: https://github.com/maksim4351/api-health-monitor/discussions *(enable in Settings → Features)*
>>>>>>> master

