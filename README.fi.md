# API Health Monitor

> **Repository:** https://github.com/maksim4351/api-health-monitor  
> **Lisenssi:** MIT  
> **Python:** 3.8+  
> **Tila:** ✅ Tuotantovalmis

🚀 **Nopea API-saannollisuuden ja viiveen seuranta ilman monimutkaisia järjestelmiä**

**API Health Monitor** on kevyt Python CLI-työkalu REST API:iden, verkkopalveluiden ja HTTP-päätepisteiden saannollisuuden, suorituskyvyn ja terveyden seurantaan. Täydellinen kehittäjille, DevOps-insinööreille ja QA-asiantuntijoille, jotka tarvitsevat nopeita API-terveystarkistuksia ilman raskaiden seurantajärjestelmien käyttöönottoa.

## 🔍 Hakusanat

`api seuranta` | `api terveystarkistus` | `api käyttöaika` | `http seuranta` | `rest api testaus` | `api tila tarkistin` | `devops työkalut` | `ci/cd seuranta` | `api saannollisuus` | `päätepiste seuranta` | `api suorituskyky` | `http tila tarkistin` | `api watchdog` | `palvelu terveystarkistus` | `python seuranta` | `kevyt seuranta` | `api testaus työkalu` | `terveystarkistus työkalu` | `käyttöaika seuranta` | `palvelu saannollisuus`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Avainsanat:** `api seuranta`, `api terveystarkistus`, `api käyttöaika`, `http seuranta`, `rest api testaus`, `api tila tarkistin`, `devops työkalut`, `ci/cd seuranta`, `api saannollisuus`, `päätepiste seuranta`, `api suorituskyky`, `http tila tarkistin`, `api watchdog`, `palvelu terveystarkistus`, `python seuranta`, `kevyt seuranta`, `api testaus työkalu`, `terveystarkistus työkalu`, `käyttöaika seuranta`, `palvelu saannollisuus`

## 📋 Kuvaus

**API Health Monitor** on yksinkertainen mutta tehokas CLI-työkalu API-saannollisuuden ja -suorituskyvyn, verkkopalveluiden ja HTTP-päätepisteiden seurantaan. Työkalu tarkistaa määritellyt API:t aikataulun mukaan tai manuaalisesti, kerää mittareita (HTTP-tila, viive, aikakatkaisut) ja luo raportteja eri muodoissa (taulukko, JSON, CSV, HTML).

### 🎯 Päällimmäiset käyttötapaukset

- **Tuotanto-API-seuranta** — kriittisten palveluiden jatkuva seuranta
- **CI/CD-integraatio** — automatisoituja API-terveystarkistuksia ennen käyttöönottoa
- **QA-testaus** — API-validoinnit testiympäristöissä
- **SLA-seuranta** — ulkoisten palveluiden saannollisuuden seuranta
- **Kehitys** — nopeat API-tarkistukset kehityksen aikana
- **DevOps** — kevyt vaihtoehto Prometheus/Grafana:lle

### 🔍 Keskeiset edut

- ⚡ **Nopea käynnistys** — toimii heti, minimaalinen asennus
- 🎯 **Yksinkertaisuus** — ei monimutkaista infrastruktuuria tarvita
- 📊 **Joustavat raportit** — taulukko, JSON, CSV integraatiota varten muiden työkalujen kanssa
- 🔧 **CI/CD-valmis** — oikeat poistumiskoodit automatisointia varten
- 🐍 **Python 3.8+** — toimii kaikilla nykyaikaisilla järjestelmillä
- 📝 **YAML-konfiguraatio** — selkeä ja helppo muokata

## 🚀 Pikakäynnistys

### Asennus

```bash
# Kloonaa repository
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Asenna riippuvuudet
pip install -r requirements.txt

# Kehitysympäristön asennus
pip install -e .
```

### Käyttö

```bash
# Yksittäinen tarkistus
api-monitor run config.yaml

# Jatkuva seuranta
api-monitor watch config.yaml

# Verkkokäyttöliittymä
api-monitor watch config.yaml --web
```

## 📖 Täydellinen dokumentaatio

📚 **Täydelliselle englanninkieliselle dokumentaatiolle, katso:** [README.md](README.md)

- Täydellinen opas: [README.md](README.md)
- Verkkoseuranta-opas: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Osallistumisopas: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Päällimmäiset ominaisuudet

- ✅ HTTP-tilan ja viiveen tarkistukset API:ille
- ✅ Konfiguroitavat aikakatkaisut jokaiselle API:lle
- ✅ Tuki kaikille HTTP-metodeille (GET, POST, PUT, DELETE, PATCH)
- ✅ Odotetun tilakoodin validointi
- ✅ Mukautetut HTTP-otsakkeet
- ✅ Raportit taulukko-, JSON-, CSV- tai HTML-muodoissa
- ✅ Reaaliaikainen verkkokäyttöliittymä
- ✅ Sähköposti- ja push-ilmoitukset
- ✅ Tulosten välimuistitus
- ✅ Asynkroniset tarkistukset (rinnakkaiset pyynnöt)

## 📄 Lisenssi

Tämä projekti on MIT-lisenssillä. Katso `LICENSE`-tiedosto yksityiskohdista.

---

**🔗 Hyödylliset linkit:**
- 📖 **Täydellinen dokumentaatio:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Verkkoseuranta:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **AI-indeksi:** [AI_INDEX.md](AI_INDEX.md) - tietoa AI-järjestelmiä varten

