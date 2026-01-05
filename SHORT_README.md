# API Health Monitor

🚀 **Fast API availability and latency monitoring without complex systems**

**API Health Monitor** is a lightweight Python CLI tool for monitoring availability, performance, and health of REST APIs and HTTP endpoints.  
Built for developers, DevOps engineers, and CI/CD pipelines that need fast and reliable API health checks without deploying heavy monitoring stacks.

## Key Features
- HTTP status and latency checks
- Configurable timeouts and headers
- CLI output: table, JSON, CSV, HTML
- Proper exit codes for CI/CD automation
- YAML-based configuration
- Optional web dashboard for continuous monitoring

## Installation
```bash
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
api-monitor run config.yaml
```

## CI/CD Usage

```bash
api-monitor run config.yaml
# Exit code 0 — all checks passed
# Exit code 1 — one or more checks failed
```

---

**📖 For full documentation, see [README.md](README.md)**

