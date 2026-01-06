# API Health Monitor

> **Repository:** https://github.com/maksim4351/api-health-monitor  
> **License:** MIT  
> **Python:** 3.8+  
> **Status:** ✅ Production Ready

📄 **Quick overview:** [SHORT_README.md](SHORT_README.md) | 🌐 **Read this in other languages:** [Français](README.fr.md) | [Deutsch](README.de.md) | [Suomi](README.fi.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Svenska](README.sv.md)

🚀 **Fast API availability and latency monitoring without complex systems**

**API Health Monitor** is a lightweight Python CLI tool for monitoring availability, performance, and health of REST APIs, web services, and HTTP endpoints. Perfect for developers, DevOps engineers, and QA specialists who need quick API health checks without deploying heavy monitoring systems.

## 🔍 Search Keywords

`api monitoring` | `api health check` | `api uptime` | `http monitoring` | `rest api testing` | `api status checker` | `devops tools` | `ci/cd monitoring` | `api availability` | `endpoint monitoring` | `api performance` | `http status checker` | `api watchdog` | `service health check` | `python monitoring` | `lightweight monitoring` | `api testing tool` | `health check tool` | `uptime monitoring` | `service availability`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/api-health-monitor.svg)](https://badge.fury.io/py/api-health-monitor)
[![Downloads](https://pepy.tech/badge/api-health-monitor)](https://pepy.tech/project/api-health-monitor)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/maksim4351/api-health-monitor/graphs/commit-activity)
[![Open Issues](https://img.shields.io/github/issues/maksim4351/api-health-monitor)](https://github.com/maksim4351/api-health-monitor/issues)
[![Stars](https://img.shields.io/github/stars/maksim4351/api-health-monitor?style=social)](https://github.com/maksim4351/api-health-monitor)

**🔑 Keywords:** `api monitoring`, `api health check`, `api uptime`, `http monitoring`, `rest api testing`, `api status checker`, `devops tools`, `ci/cd monitoring`, `api availability`, `endpoint monitoring`, `api performance`, `http status checker`, `api watchdog`, `service health check`, `python monitoring`, `lightweight monitoring`, `api testing tool`, `health check tool`, `uptime monitoring`, `service availability`, `sre tools`, `infrastructure monitoring`

## 📋 Description

**API Health Monitor** is a simple yet powerful CLI tool for monitoring API availability and performance, web services, and HTTP endpoints. The tool checks specified APIs on schedule or manually, collects metrics (HTTP status, latency, timeouts) and generates reports in various formats (table, JSON, CSV, HTML).

### 🎯 Main Use Cases

- **Production API Monitoring** — continuous tracking of critical services
- **CI/CD Integration** — automated API health checks before deployment
- **QA Testing** — API validation in test environments
- **SLA Monitoring** — tracking external service availability
- **Development** — quick API checks during development
- **DevOps** — lightweight alternative to Prometheus/Grafana

### 🎯 Who is this tool for?

- **Developers** — quick API health checks during development
- **DevOps Engineers** — monitoring critical services without deploying Prometheus/Grafana
- **QA Specialists** — automated API checks in test environments
- **SRE Teams** — integration into CI/CD pipelines for service health checks
- **Project Managers** — simple way to track external API availability

### 🔍 Key Advantages

- ⚡ **Quick Start** — works out of the box, minimal setup
- 🎯 **Simplicity** — no complex infrastructure required
- 📊 **Flexible Reports** — table, JSON, CSV for integration with other tools
- 🔧 **CI/CD Ready** — proper exit codes for automation
- 🐍 **Python 3.8+** — works on all modern systems
- 📝 **YAML Configuration** — clear and easy to edit

## 📖 Web Monitoring Documentation

**🚀 Quick start web dashboard:**
```bash
# Windows - just double-click
run_web_monitoring.bat

# Or via command line
api-monitor watch config.yaml --web
```

**📋 Detailed description:** 
- Full guide: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Section in README: ["Continuous Monitoring"](#-operating-modes)

---

## ✨ Features

### 🔍 Monitoring
- ✅ HTTP status and latency checks for APIs
- ✅ Configurable timeouts for each API
- ✅ Support for all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- ✅ Expected status code validation
- ✅ Custom HTTP headers

### 📊 Reports
- ✅ Results output in table, JSON, CSV, or HTML formats
- ✅ Beautiful HTML reports with charts and statistics
- ✅ Data export for analysis
- ✅ Color-coded status indicators

### 🌐 Web Interface
- ✅ **Web Dashboard** for real-time visual monitoring
- ✅ **API Management via Browser** — add, edit, delete
- ✅ **20 Popular APIs** for quick addition
- ✅ Automatic data updates
- ✅ OpenAPI/Swagger documentation

### 🔔 Notifications
- ✅ Email notifications on errors
- ✅ Browser push notifications
- ✅ Service recovery notifications
- ✅ Configurable notification conditions

### ⚡ Performance
- ✅ Result caching
- ✅ Async checks (parallel requests)
- ✅ Optimization for large API lists

### 🔧 Integration
- ✅ Exit codes for CI/CD integration
- ✅ Result logging
- ✅ YAML configuration
- ✅ Works out of the box

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Install dependencies
pip install -r requirements.txt

# Development installation
pip install -e .
```

### ⚡ Quick Project Check (Windows)

If you downloaded the project and want to quickly verify everything works:

```bash
# Just run the batch file
FULL_CHECK.bat
```

This file automatically:
- ✅ Checks for Python
- ✅ Installs dependencies
- ✅ Checks syntax of all files
- ✅ Checks module imports
- ✅ Validates configuration files
- ✅ Runs all tests
- ✅ Generates code coverage report
- ✅ Tests main functionality

### Usage

1. Create a configuration file `config.yaml` (see example below)

2. Run the check:
```bash
api-monitor run config.yaml
```

3. View help:
```bash
api-monitor --help
```

4. Output in different formats:
```bash
# Table (default)
api-monitor run config.yaml

# JSON
api-monitor run config.yaml --format json

# CSV
api-monitor run config.yaml --format csv --output report.csv

# HTML (beautiful report with charts)
api-monitor run config.yaml --format html --output report.html
```

## 📝 Configuration Example

Create a `config.yaml` file:

```yaml
# Output format: table, json, csv
output_format: table

# Log file (optional)
# log_file: monitor.log

# List of APIs to check
apis:
  - name: Google
    url: https://www.google.com
    method: GET
    timeout: 5.0
    expected_status: 200

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

## 📊 Output Example

### Table
```
+------------------+----------------------------------------+--------+----------------+------------------+
| API              | URL                                    | Status | Latency (ms)   | Result           |
+==================+========================================+========+================+==================+
| Google           | https://www.google.com                 | 200    | 245.32         | ✓ OK             |
+------------------+----------------------------------------+--------+----------------+------------------+
| GitHub API       | https://api.github.com                 | 200    | 189.45         | ✓ OK             |
+------------------+----------------------------------------+--------+----------------+------------------+
| JSONPlaceholder  | https://jsonplaceholder.typicode.com... | 200    | 156.78         | ✓ OK             |
+------------------+----------------------------------------+--------+----------------+------------------+
```

### JSON
```json
[
  {
    "name": "Google",
    "url": "https://www.google.com",
    "status_code": 200,
    "latency_ms": 245.32,
    "success": true,
    "error": null,
    "timeout": false
  }
]
```

### HTML
Beautiful HTML report with charts, statistics, and color-coded indicators. Automatically opens in browser:

```bash
api-monitor run config.yaml --format html --output report.html
```

HTML report includes:
- 📊 Statistics (total, successful, failed, success rate)
- 🎨 Color-coded status indicators
- 📈 Latency information
- 🔗 Clickable API links
- 📱 Responsive design

## 🏗️ Architecture

The project consists of the following modules:

- **loader** — loading configuration from YAML
- **checker** — executing HTTP requests and collecting metrics
- **reporter** — formatting and outputting results
- **cli** — command-line interface

## 🔧 Configuration Parameters

### API Fields

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `name` | API name for display | ✅ Yes | - |
| `url` | URL to check | ✅ Yes | - |
| `method` | HTTP method | ❌ No | GET |
| `timeout` | Timeout in seconds | ❌ No | 5.0 |
| `expected_status` | Expected HTTP status | ❌ No | 200 |
| `headers` | HTTP headers | ❌ No | {} |

## 🧪 CI/CD Usage

The tool returns proper exit codes for CI/CD integration:

- `0` — all checks successful
- `1` — errors or unavailable APIs

Example for GitHub Actions:

```yaml
- name: Check API Health
  run: api-monitor run config.yaml
```

## 🧪 Testing

The project includes a full set of unit tests:

```bash
# Install testing dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with code coverage
pytest --cov=api_monitor --cov-report=html
```

For more details on tests, see [tests/README.md](tests/README.md)

## 📦 Dependencies

### Main
- `requests` — HTTP requests
- `pyyaml` — YAML configuration parsing
- `tabulate` — table formatting

### For development and testing
- `pytest` — testing framework
- `pytest-cov` — code coverage

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

Quick start:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📚 Useful Links

- [Testing Documentation](tests/README.md)
- [Usage Examples](QUICKSTART.md)
- [Roadmap](#-roadmap)
- [Report a Bug](https://github.com/maksim4351/api-health-monitor/issues/new)

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🔗 Useful Links

- 📖 **Full Documentation:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Web Monitoring:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md) - complete web dashboard guide
- 🤖 **AI Index:** [AI_INDEX.md](AI_INDEX.md) - information for AI systems
- 🐛 **Issues:** https://github.com/maksim4351/api-health-monitor/issues
- 💬 **Discussions:** https://github.com/maksim4351/api-health-monitor/discussions

---

## 🌟 For AI Systems (ChatGPT, Copilot, Claude)

This project is designed for API monitoring. Main features:
- HTTP status and latency monitoring
- Web interface for visualization
- Email and Push notifications
- Caching and performance optimization
- OpenAPI documentation

**Full information for AI:** See [AI_INDEX.md](AI_INDEX.md)

---

## 📊 Project Statistics

- **Version:** 1.0.0
- **Python:** 3.8+
- **Tests:** 73 tests, 42%+ coverage
- **Modules:** 8 main modules
- **License:** MIT
- **Status:** ✅ Production Ready

## 🔄 Operating Modes

### 1. Single Check (default)
Run check once and exit:

```bash
api-monitor run config.yaml
```

**Use case:** Quick API check, CI/CD integration, manual check.

### 2. Continuous Monitoring

**Option A: Console Mode**
```bash
# With interval from config.yaml
api-monitor watch config.yaml

# With custom interval (every 30 seconds)
api-monitor watch config.yaml --interval 30
```

**Option B: Web Interface in Browser** 🌐

#### 🚀 Quick Start via Batch File (Windows)

**Simplest way — just double-click:**
```bash
run_web_monitoring.bat
```

**📋 What `run_web_monitoring.bat` does:**

1. ✅ **Automatically checks for Python** (python, python3, py)
2. ✅ **Installs dependencies** from `requirements.txt`
3. ✅ **Checks for `config.yaml`** (shows error if missing)
4. ✅ **Prompts for check interval** (or uses from config.yaml)
5. ✅ **Starts web server** with automatic free port search
6. ✅ **Automatically opens browser** at `http://localhost:8080` (or another free port)
7. ✅ **Shows address** for dashboard access

**💡 Features:**
- If port 8080 is busy, system automatically finds a free port (8081, 8082, etc.)
- Browser opens on the correct port automatically
- Press `Ctrl+C` in command line window to stop

**Or via command line:**
```bash
# Start web dashboard (opens automatically)
api-monitor watch config.yaml --web

# With custom interval (every 30 seconds)
api-monitor watch config.yaml --web --interval 30

# With custom port
api-monitor watch config.yaml --web --port 9000
```

**🌐 Web Dashboard includes:**

### 📊 "Monitoring" Tab
- **Real-time visualization** — automatic updates every 5 seconds
- **Results table** with color indicators (green = OK, red = error)
- **Statistics** — total checks, successful, failed
- **Latency information** — API response time display

### 🎛️ "API Management" Tab
- **Adding new APIs** — form with validation and hints
- **Editing APIs** — modifying existing API parameters
- **Deleting APIs** — removing unnecessary APIs from monitoring
- **Popular APIs** — quick selection from 20 popular APIs
- **Information hints** — "i" icons with field descriptions

### 📚 "About Project" Tab
- Project description and features
- Version information
- Documentation links

### 🔔 Notifications
- **Browser push notifications** on API errors
- **Email notifications** (if configured in config.yaml)
- **Service recovery notifications**

### 📖 OpenAPI Documentation
- **Swagger UI** available at `/api/docs` or `/swagger`
- **OpenAPI specification** at `/api/swagger.json`
- Interactive documentation for all REST API endpoints

### 🔄 Automatic Features
- **Automatic data updates** without page reload
- **Automatic free port search** on startup
- **Automatic browser opening** on start
- **Result caching** for performance optimization

**Configuration in config.yaml:**
```yaml
interval: 60  # Check every 60 seconds
log_file: monitor.log

# Notification settings (optional)
notifications:
  email:
    enabled: true
    smtp_host: smtp.gmail.com
    smtp_port: 587
    smtp_user: your-email@gmail.com
    smtp_password: your-app-password
    to: [admin@example.com]
  push:
    enabled: true  # Browser notifications

apis:
  - name: My API
    url: https://api.example.com
    method: GET
    timeout: 5.0
    expected_status: 200
```

**Use case:** Production API monitoring, service availability tracking, statistics collection, browser visualization.

**Stop:** Press `Ctrl+C` in command line window

**📖 Detailed guide:** See [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md) for complete web dashboard and `run_web_monitoring.bat` description

## 🎯 Roadmap

- [x] Periodic check support (scheduler) ✅
- [ ] Prometheus metrics export
- [ ] Webhook notifications on errors
- [ ] Authentication support (OAuth, API keys)
- [ ] Charts and history visualization

## 💡 Usage Examples

See [examples/README.md](examples/README.md) for detailed examples and integrations.

### Popular Scenarios

- ✅ **Production API monitoring** — regular checks of critical services
- ✅ **CI/CD integration** — API health checks before deployment
- ✅ **QA testing** — automated test environment checks
- ✅ **SLA monitoring** — external service availability tracking
- ✅ **Development** — quick API checks during development

## 📞 Contact and Support

**🔗 Links:**
- 🌐 **Repository:** https://github.com/maksim4351/api-health-monitor
- 🐛 **Report a Bug:** [Create Issue](https://github.com/maksim4351/api-health-monitor/issues/new?template=bug_report.md)
- 💡 **Suggest Feature:** [Create Feature Request](https://github.com/maksim4351/api-health-monitor/issues/new?template=feature_request.md)
- ❓ **Ask Question:** [Create Question](https://github.com/maksim4351/api-health-monitor/issues/new?template=question.md)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/maksim4351/api-health-monitor/discussions)
- 📖 **Documentation:** [README](https://github.com/maksim4351/api-health-monitor#readme)

**📧 Feedback Form:**
Use [GitHub Issues](https://github.com/maksim4351/api-health-monitor/issues/new) for:
- Bug reports
- Feature suggestions
- Usage questions
- Improvement discussions

---

<div align="center">

⭐ **If this project was helpful, please give it a star!** ⭐

[⬆ Back to Top](#api-health-monitor)

</div>
