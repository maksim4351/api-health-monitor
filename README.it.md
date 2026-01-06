# API Health Monitor

> **Repository:** https://github.com/maksim4351/api-health-monitor  
> **Licenza:** MIT  
> **Python:** 3.8+  
> **Stato:** ✅ Pronto per la produzione

🚀 **Monitoraggio rapido della disponibilità e latenza delle API senza sistemi complessi**

**API Health Monitor** è uno strumento CLI Python leggero per monitorare la disponibilità, le prestazioni e lo stato delle API REST, servizi web ed endpoint HTTP. Perfetto per sviluppatori, ingegneri DevOps e specialisti QA che necessitano di controlli rapidi dello stato delle API senza implementare sistemi di monitoraggio pesanti.

## 🔍 Parole chiave di ricerca

`monitoraggio api` | `controllo salute api` | `tempo attività api` | `monitoraggio http` | `test api rest` | `verificatore stato api` | `strumenti devops` | `monitoraggio ci/cd` | `disponibilità api` | `monitoraggio endpoint` | `prestazioni api` | `verificatore stato http` | `sentinella api` | `controllo salute servizio` | `monitoraggio python` | `monitoraggio leggero` | `strumento test api` | `strumento controllo salute` | `monitoraggio tempo attività` | `disponibilità servizio`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Parole chiave:** `monitoraggio api`, `controllo salute api`, `tempo attività api`, `monitoraggio http`, `test api rest`, `verificatore stato api`, `strumenti devops`, `monitoraggio ci/cd`, `disponibilità api`, `monitoraggio endpoint`, `prestazioni api`, `verificatore stato http`, `sentinella api`, `controllo salute servizio`, `monitoraggio python`, `monitoraggio leggero`, `strumento test api`, `strumento controllo salute`, `monitoraggio tempo attività`, `disponibilità servizio`

## 📋 Descrizione

**API Health Monitor** è uno strumento CLI semplice ma potente per monitorare la disponibilità e le prestazioni delle API, servizi web ed endpoint HTTP. Lo strumento verifica le API specificate secondo un programma o manualmente, raccoglie metriche (stato HTTP, latenza, timeout) e genera report in vari formati (tabella, JSON, CSV, HTML).

### 🎯 Casi d'uso principali

- **Monitoraggio API in produzione** — tracciamento continuo di servizi critici
- **Integrazione CI/CD** — controlli automatici dello stato delle API prima del deployment
- **Test QA** — validazione delle API in ambienti di test
- **Monitoraggio SLA** — tracciamento della disponibilità di servizi esterni
- **Sviluppo** — controlli rapidi delle API durante lo sviluppo
- **DevOps** — alternativa leggera a Prometheus/Grafana

### 🔍 Vantaggi chiave

- ⚡ **Avvio rapido** — funziona immediatamente, configurazione minima
- 🎯 **Semplicità** — nessuna infrastruttura complessa richiesta
- 📊 **Report flessibili** — tabella, JSON, CSV per l'integrazione con altri strumenti
- 🔧 **Pronto per CI/CD** — codici di uscita appropriati per l'automazione
- 🐍 **Python 3.8+** — funziona su tutti i sistemi moderni
- 📝 **Configurazione YAML** — chiara e facile da modificare

## 🚀 Avvio rapido

### Installazione

```bash
# Clonare il repository
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Installare le dipendenze
pip install -r requirements.txt

# Installazione di sviluppo
pip install -e .
```

### Utilizzo

```bash
# Controllo singolo
api-monitor run config.yaml

# Monitoraggio continuo
api-monitor watch config.yaml

# Interfaccia web
api-monitor watch config.yaml --web
```

## 📖 Documentazione completa

📚 **Per la documentazione completa in inglese, vedere:** [README.md](README.md)

- Guida completa: [README.md](README.md)
- Guida monitoraggio web: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Guida contributi: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Caratteristiche principali

- ✅ Controlli di stato HTTP e latenza per API
- ✅ Timeout configurabili per ogni API
- ✅ Supporto per tutti i metodi HTTP (GET, POST, PUT, DELETE, PATCH)
- ✅ Validazione del codice di stato atteso
- ✅ Intestazioni HTTP personalizzate
- ✅ Report in formati tabella, JSON, CSV, HTML
- ✅ Dashboard web in tempo reale
- ✅ Notifiche email e push
- ✅ Caching dei risultati
- ✅ Controlli asincroni (richieste parallele)

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedere il file `LICENSE` per i dettagli.

---

**🔗 Link utili:**
- 📖 **Documentazione completa:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Monitoraggio web:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **Indice AI:** [AI_INDEX.md](AI_INDEX.md) - informazioni per sistemi AI

