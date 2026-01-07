"""Setup script for API Health Monitor."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="api-health-monitor",
    version="1.0.0",
    description="Lightweight Python CLI tool for monitoring API availability, performance, and health checks. Perfect for developers, DevOps teams, and CI/CD pipelines. Features web dashboard, email notifications, caching, and OpenAPI documentation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="maksim4351",
    author_email="maksim4351@users.noreply.github.com",
    url="https://github.com/maksim4351/api-health-monitor",
    project_urls={
        "Bug Reports": "https://github.com/maksim4351/api-health-monitor/issues",
        "Source": "https://github.com/maksim4351/api-health-monitor",
        "Documentation": "https://github.com/maksim4351/api-health-monitor#readme",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pyyaml>=6.0",
        "tabulate>=0.9.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "api-monitor=api_monitor.cli:main",
        ],
    },
    keywords=[
        "api",
        "monitoring",
        "health-check",
        "uptime",
        "http",
        "rest",
        "api-testing",
        "devops",
        "ci-cd",
        "endpoint",
        "status-checker",
        "service-monitoring",
        "api-watchdog",
        "availability",
        "performance",
        "latency",
        "http-status",
        "yaml",
        "cli",
        "python",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Testing",
    ],
)


