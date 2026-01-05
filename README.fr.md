# API Health Monitor

> **Dépôt:** https://github.com/maksim4351/api-health-monitor  
> **Licence:** MIT  
> **Python:** 3.8+  
> **Statut:** ✅ Prêt pour la production

🚀 **Surveillance rapide de la disponibilité et de la latence des API sans systèmes complexes**

**API Health Monitor** est un outil CLI Python léger pour surveiller la disponibilité, les performances et la santé des API REST, des services web et des points de terminaison HTTP. Parfait pour les développeurs, les ingénieurs DevOps et les spécialistes QA qui ont besoin de vérifications rapides de la santé des API sans déployer de systèmes de surveillance lourds.

## 🔍 Mots-clés de recherche

`surveillance api` | `vérification santé api` | `temps de fonctionnement api` | `surveillance http` | `test api rest` | `vérificateur statut api` | `outils devops` | `surveillance ci/cd` | `disponibilité api` | `surveillance point de terminaison` | `performance api` | `vérificateur statut http` | `garde api` | `vérification santé service` | `surveillance python` | `surveillance légère` | `outil test api` | `outil vérification santé` | `surveillance temps de fonctionnement` | `disponibilité service`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Mots-clés:** `surveillance api`, `vérification santé api`, `temps de fonctionnement api`, `surveillance http`, `test api rest`, `vérificateur statut api`, `outils devops`, `surveillance ci/cd`, `disponibilité api`, `surveillance point de terminaison`, `performance api`, `vérificateur statut http`, `garde api`, `vérification santé service`, `surveillance python`, `surveillance légère`, `outil test api`, `outil vérification santé`, `surveillance temps de fonctionnement`, `disponibilité service`

## 📋 Description

**API Health Monitor** est un outil CLI simple mais puissant pour surveiller la disponibilité et les performances des API, des services web et des points de terminaison HTTP. L'outil vérifie les API spécifiées selon un calendrier ou manuellement, collecte des métriques (statut HTTP, latence, timeouts) et génère des rapports dans divers formats (tableau, JSON, CSV, HTML).

### 🎯 Cas d'utilisation principaux

- **Surveillance API en production** — suivi continu des services critiques
- **Intégration CI/CD** — vérifications automatiques de la santé des API avant le déploiement
- **Tests QA** — validation des API dans les environnements de test
- **Surveillance SLA** — suivi de la disponibilité des services externes
- **Développement** — vérifications rapides des API pendant le développement
- **DevOps** — alternative légère à Prometheus/Grafana

### 🔍 Avantages clés

- ⚡ **Démarrage rapide** — fonctionne immédiatement, configuration minimale
- 🎯 **Simplicité** — aucune infrastructure complexe requise
- 📊 **Rapports flexibles** — tableau, JSON, CSV pour l'intégration avec d'autres outils
- 🔧 **Prêt pour CI/CD** — codes de sortie appropriés pour l'automatisation
- 🐍 **Python 3.8+** — fonctionne sur tous les systèmes modernes
- 📝 **Configuration YAML** — claire et facile à modifier

## 🚀 Démarrage rapide

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Installer les dépendances
pip install -r requirements.txt

# Installation de développement
pip install -e .
```

### Utilisation

```bash
# Vérification unique
api-monitor run config.yaml

# Surveillance continue
api-monitor watch config.yaml

# Interface web
api-monitor watch config.yaml --web
```

## 📖 Documentation complète

📚 **Pour la documentation complète en anglais, voir:** [README.md](README.md)

- Guide complet: [README.md](README.md)
- Guide web monitoring: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Guide de contribution: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Fonctionnalités principales

- ✅ Surveillance HTTP et latence des API
- ✅ Timeouts configurables pour chaque API
- ✅ Support de toutes les méthodes HTTP (GET, POST, PUT, DELETE, PATCH)
- ✅ Validation du code de statut attendu
- ✅ En-têtes HTTP personnalisés
- ✅ Rapports en tableau, JSON, CSV, HTML
- ✅ Interface web en temps réel
- ✅ Notifications par email et push
- ✅ Mise en cache des résultats
- ✅ Vérifications asynchrones (requêtes parallèles)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**🔗 Liens utiles:**
- 📖 **Documentation complète:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Surveillance web:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **Index AI:** [AI_INDEX.md](AI_INDEX.md) - informations pour les systèmes IA

