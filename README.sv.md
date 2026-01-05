# API Health Monitor

> **Repository:** https://github.com/maksim4351/api-health-monitor  
> **Licens:** MIT  
> **Python:** 3.8+  
> **Status:** ✅ Produktionsredo

🚀 **Snabb API-tillgänglighets- och latensövervakning utan komplexa system**

**API Health Monitor** är ett lättviktigt Python CLI-verktyg för att övervaka tillgänglighet, prestanda och hälsa hos REST API:er, webbtjänster och HTTP-slutpunkter. Perfekt för utvecklare, DevOps-ingenjörer och QA-specialister som behöver snabba API-hälsokontroller utan att distribuera tunga övervakningssystem.

## 🔍 Sökord

`api övervakning` | `api hälsokontroll` | `api drifttid` | `http övervakning` | `rest api testning` | `api statuskontroll` | `devops verktyg` | `ci/cd övervakning` | `api tillgänglighet` | `slutpunkt övervakning` | `api prestanda` | `http statuskontroll` | `api watchdog` | `tjänst hälsokontroll` | `python övervakning` | `lättviktig övervakning` | `api testverktyg` | `hälsokontroll verktyg` | `drifttid övervakning` | `tjänst tillgänglighet`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Nyckelord:** `api övervakning`, `api hälsokontroll`, `api drifttid`, `http övervakning`, `rest api testning`, `api statuskontroll`, `devops verktyg`, `ci/cd övervakning`, `api tillgänglighet`, `slutpunkt övervakning`, `api prestanda`, `http statuskontroll`, `api watchdog`, `tjänst hälsokontroll`, `python övervakning`, `lättviktig övervakning`, `api testverktyg`, `hälsokontroll verktyg`, `drifttid övervakning`, `tjänst tillgänglighet`

## 📋 Beskrivning

**API Health Monitor** är ett enkelt men kraftfullt CLI-verktyg för att övervaka API-tillgänglighet och prestanda, webbtjänster och HTTP-slutpunkter. Verktyget kontrollerar angivna API:er enligt schema eller manuellt, samlar in mätvärden (HTTP-status, latens, timeout) och genererar rapporter i olika format (tabell, JSON, CSV, HTML).

### 🎯 Huvudsakliga användningsfall

- **Produktions-API-övervakning** — kontinuerlig spårning av kritiska tjänster
- **CI/CD-integration** — automatiserade API-hälsokontroller före distribution
- **QA-testning** — API-validering i testmiljöer
- **SLA-övervakning** — spårning av externa tjänsters tillgänglighet
- **Utveckling** — snabba API-kontroller under utveckling
- **DevOps** — lättviktigt alternativ till Prometheus/Grafana

### 🔍 Huvudsakliga fördelar

- ⚡ **Snabb start** — fungerar direkt, minimal konfiguration
- 🎯 **Enkelhet** — ingen komplex infrastruktur krävs
- 📊 **Flexibla rapporter** — tabell, JSON, CSV för integration med andra verktyg
- 🔧 **CI/CD-redo** — korrekta avslutskoder för automatisering
- 🐍 **Python 3.8+** — fungerar på alla moderna system
- 📝 **YAML-konfiguration** — tydlig och lätt att redigera

## 🚀 Snabbstart

### Installation

```bash
# Klona repository
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Installera beroenden
pip install -r requirements.txt

# Utvecklingsinstallation
pip install -e .
```

### Användning

```bash
# Enstaka kontroll
api-monitor run config.yaml

# Kontinuerlig övervakning
api-monitor watch config.yaml

# Webbgränssnitt
api-monitor watch config.yaml --web
```

## 📖 Fullständig dokumentation

📚 **För fullständig dokumentation på engelska, se:** [README.md](README.md)

- Fullständig guide: [README.md](README.md)
- Webbövervakningsguide: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Bidragsguide: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Huvudfunktioner

- ✅ HTTP-status- och latenskontroller för API:er
- ✅ Konfigurerbara timeout för varje API
- ✅ Stöd för alla HTTP-metoder (GET, POST, PUT, DELETE, PATCH)
- ✅ Validering av förväntad statuskod
- ✅ Anpassade HTTP-huvuden
- ✅ Rapporter i tabell-, JSON-, CSV- eller HTML-format
- ✅ Realtidswebbinstrumentpanel
- ✅ E-post- och push-meddelanden
- ✅ Resultatcachning
- ✅ Asynkrona kontroller (parallella förfrågningar)

## 📄 Licens

Detta projekt är licensierad under MIT. Se filen `LICENSE` för detaljer.

---

**🔗 Användbara länkar:**
- 📖 **Fullständig dokumentation:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Webbövervakning:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **AI-index:** [AI_INDEX.md](AI_INDEX.md) - information för AI-system

