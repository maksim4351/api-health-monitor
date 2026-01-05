# API Health Monitor

> **Repository:** https://github.com/maksim4351/api-health-monitor  
> **Lizenz:** MIT  
> **Python:** 3.8+  
> **Status:** ✅ Produktionsbereit

🚀 **Schnelle API-Verfügbarkeits- und Latenzüberwachung ohne komplexe Systeme**

**API Health Monitor** ist ein leichtgewichtiges Python CLI-Tool zur Überwachung der Verfügbarkeit, Leistung und Gesundheit von REST-APIs, Webdiensten und HTTP-Endpunkten. Perfekt für Entwickler, DevOps-Ingenieure und QA-Spezialisten, die schnelle API-Gesundheitsprüfungen ohne den Einsatz schwerer Überwachungssysteme benötigen.

## 🔍 Suchbegriffe

`api überwachung` | `api gesundheitsprüfung` | `api betriebszeit` | `http überwachung` | `rest api test` | `api status prüfer` | `devops tools` | `ci/cd überwachung` | `api verfügbarkeit` | `endpunkt überwachung` | `api leistung` | `http status prüfer` | `api watchdog` | `service gesundheitsprüfung` | `python überwachung` | `leichtgewichtige überwachung` | `api test tool` | `gesundheitsprüfung tool` | `betriebszeit überwachung` | `service verfügbarkeit`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Schlüsselwörter:** `api überwachung`, `api gesundheitsprüfung`, `api betriebszeit`, `http überwachung`, `rest api test`, `api status prüfer`, `devops tools`, `ci/cd überwachung`, `api verfügbarkeit`, `endpunkt überwachung`, `api leistung`, `http status prüfer`, `api watchdog`, `service gesundheitsprüfung`, `python überwachung`, `leichtgewichtige überwachung`, `api test tool`, `gesundheitsprüfung tool`, `betriebszeit überwachung`, `service verfügbarkeit`

## 📋 Beschreibung

**API Health Monitor** ist ein einfaches, aber leistungsstarkes CLI-Tool zur Überwachung der API-Verfügbarkeit und -leistung, von Webdiensten und HTTP-Endpunkten. Das Tool prüft angegebene APIs nach Zeitplan oder manuell, sammelt Metriken (HTTP-Status, Latenz, Timeouts) und generiert Berichte in verschiedenen Formaten (Tabelle, JSON, CSV, HTML).

### 🎯 Hauptanwendungsfälle

- **Produktions-API-Überwachung** — kontinuierliche Verfolgung kritischer Dienste
- **CI/CD-Integration** — automatisierte API-Gesundheitsprüfungen vor dem Deployment
- **QA-Tests** — API-Validierung in Testumgebungen
- **SLA-Überwachung** — Verfolgung der Verfügbarkeit externer Dienste
- **Entwicklung** — schnelle API-Prüfungen während der Entwicklung
- **DevOps** — leichtgewichtige Alternative zu Prometheus/Grafana

### 🔍 Hauptvorteile

- ⚡ **Schneller Start** — funktioniert sofort, minimale Einrichtung
- 🎯 **Einfachheit** — keine komplexe Infrastruktur erforderlich
- 📊 **Flexible Berichte** — Tabelle, JSON, CSV für die Integration mit anderen Tools
- 🔧 **CI/CD-Bereit** — ordnungsgemäße Exit-Codes für die Automatisierung
- 🐍 **Python 3.8+** — funktioniert auf allen modernen Systemen
- 📝 **YAML-Konfiguration** — klar und einfach zu bearbeiten

## 🚀 Schnellstart

### Installation

```bash
# Repository klonen
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Abhängigkeiten installieren
pip install -r requirements.txt

# Entwicklungsumgebung installieren
pip install -e .
```

### Verwendung

```bash
# Einmalige Prüfung
api-monitor run config.yaml

# Kontinuierliche Überwachung
api-monitor watch config.yaml

# Web-Interface
api-monitor watch config.yaml --web
```

## 📖 Vollständige Dokumentation

📚 **Für die vollständige Dokumentation auf Englisch, siehe:** [README.md](README.md)

- Vollständiger Leitfaden: [README.md](README.md)
- Web-Monitoring-Leitfaden: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Beitragsleitfaden: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Hauptfunktionen

- ✅ HTTP-Status- und Latenzprüfungen für APIs
- ✅ Konfigurierbare Timeouts für jede API
- ✅ Unterstützung aller HTTP-Methoden (GET, POST, PUT, DELETE, PATCH)
- ✅ Validierung des erwarteten Statuscodes
- ✅ Benutzerdefinierte HTTP-Header
- ✅ Berichte in Tabellen-, JSON-, CSV- oder HTML-Formaten
- ✅ Web-Dashboard in Echtzeit
- ✅ E-Mail- und Push-Benachrichtigungen
- ✅ Ergebnis-Caching
- ✅ Asynchrone Prüfungen (parallele Anfragen)

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die Datei `LICENSE` für Details.

---

**🔗 Nützliche Links:**
- 📖 **Vollständige Dokumentation:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Web-Überwachung:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **AI-Index:** [AI_INDEX.md](AI_INDEX.md) - Informationen für KI-Systeme

