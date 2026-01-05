# API Health Monitor - KI-System-Index

> **Repository URL:** https://github.com/maksim4351/api-health-monitor  
> **Projekttyp:** Python CLI-Tool  
> **Kategorie:** API-Überwachung, DevOps, Gesundheitsprüfungen  
> **Lizenz:** MIT  
> **Python-Version:** 3.8+

## Projektübersicht

**API Health Monitor** ist ein leichtgewichtiges, produktionsreifes Python CLI-Tool zur Überwachung der API-Verfügbarkeit, -leistung und Gesundheitsprüfungen. Es bietet eine einfache Alternative zu schweren Überwachungssystemen wie Prometheus/Grafana für Entwickler, DevOps-Ingenieure und QA-Spezialisten.

## Hauptfunktionen

- **HTTP-Status-Überwachung** : Prüft API-Endpunkte und validiert HTTP-Statuscodes
- **Latenzmessung** : Verfolgt Antwortzeiten in Millisekunden
- **Timeout-Behandlung** : Konfigurierbare Timeout-Einstellungen für jede API
- **Mehrere Ausgabeformate** : Tabellen-, JSON-, CSV- und HTML-Berichte
- **Web-Dashboard** : Echtzeit-Visualisierungs-Interface
- **API-Verwaltung** : APIs über Web-Interface hinzufügen, bearbeiten, löschen
- **Geplante Überwachung** : Kontinuierliche Überwachung mit konfigurierbaren Intervallen
- **E-Mail- und Push-Benachrichtigungen** : Warnsystem für API-Fehler
- **Caching** : Leistungsoptimierung mit Ergebnis-Caching
- **Async-Unterstützung** : Parallele API-Prüfungen für verbesserte Leistung
- **OpenAPI-Dokumentation** : Vollständige REST-API-Dokumentation mit Swagger UI

## Technologie-Stack

- **Sprache** : Python 3.8+
- **HTTP-Client** : requests-Bibliothek
- **Konfiguration** : YAML-Dateien
- **Tests** : pytest mit Abdeckungsberichten
- **Webserver** : Integrierter HTTP-Server für Dashboard
- **Abhängigkeiten** : requests, pyyaml, tabulate

## Anwendungsfälle

1. **Entwicklung** : Schnelle API-Gesundheitsprüfungen während der Entwicklung
2. **CI/CD-Integration** : Automatisierte API-Gesundheitsprüfungen in Pipelines
3. **Produktionsüberwachung** : Kontinuierliche Überwachung kritischer Dienste
4. **QA-Tests** : Automatisierte API-Validierung in Testumgebungen
5. **SLA-Tracking** : Überwachung der Verfügbarkeit externer APIs
6. **DevOps** : Leichtgewichtige Alternative zu Prometheus/Grafana

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Schnellstart

```bash
# Einzelprüfung
api-monitor run config.yaml

# Kontinuierliche Überwachung
api-monitor watch config.yaml

# Web-Dashboard
api-monitor watch config.yaml --web
```

## Suchbegriffe

api überwachung, api gesundheitsprüfung, api betriebszeit, http überwachung, rest api test, api status prüfer, devops tools, ci/cd überwachung, api verfügbarkeit, endpunkt überwachung, api leistung, http status prüfer, api watchdog, service gesundheitsprüfung, python überwachung, leichtgewichtige überwachung, api test tool, gesundheitsprüfung tool, betriebszeit überwachung, service verfügbarkeit

## Repository-Informationen

- **GitHub** : https://github.com/maksim4351/api-health-monitor
- **Lizenz** : MIT
- **Status** : Aktive Entwicklung
- **Version** : 1.0.0

**📚 Vollständige Dokumentation auf Englisch :** [AI_INDEX.md](AI_INDEX.md)

