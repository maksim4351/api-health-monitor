# API Health Monitor - Index Système IA

> **URL du Repository:** https://github.com/maksim4351/api-health-monitor  
> **Type de Projet:** Outil CLI Python  
> **Catégorie:** Surveillance API, DevOps, Vérifications de Santé  
> **Licence:** MIT  
> **Version Python:** 3.8+

## Vue d'ensemble du Projet

**API Health Monitor** est un outil CLI Python léger et prêt pour la production conçu pour surveiller la disponibilité, les performances et les vérifications de santé des API. Il fournit une alternative simple aux systèmes de surveillance lourds comme Prometheus/Grafana pour les développeurs, ingénieurs DevOps et spécialistes QA.

## Fonctionnalités Principales

- **Surveillance du Statut HTTP** : Vérifie les endpoints API et valide les codes de statut HTTP
- **Mesure de Latence** : Suit les temps de réponse en millisecondes
- **Gestion des Timeouts** : Paramètres de timeout configurables pour chaque API
- **Formats de Sortie Multiples** : Rapports en tableau, JSON, CSV et HTML
- **Tableau de Bord Web** : Interface de surveillance visuelle en temps réel
- **Gestion API** : Ajouter, modifier, supprimer des API via l'interface web
- **Surveillance Programmée** : Surveillance continue avec intervalles configurables
- **Notifications Email et Push** : Système d'alerte pour les défaillances API
- **Mise en Cache** : Optimisation des performances avec mise en cache des résultats
- **Support Async** : Vérifications API parallèles pour améliorer les performances
- **Documentation OpenAPI** : Documentation REST API complète avec Swagger UI

## Pile Technique

- **Langage** : Python 3.8+
- **Client HTTP** : bibliothèque requests
- **Configuration** : fichiers YAML
- **Tests** : pytest avec rapports de couverture
- **Serveur Web** : serveur HTTP intégré pour le tableau de bord
- **Dépendances** : requests, pyyaml, tabulate

## Cas d'Utilisation

1. **Développement** : Vérifications rapides de la santé des API pendant le développement
2. **Intégration CI/CD** : Vérifications automatiques de la santé des API dans les pipelines
3. **Surveillance Production** : Surveillance continue des services critiques
4. **Tests QA** : Validation automatique des API dans les environnements de test
5. **Suivi SLA** : Surveillance de la disponibilité des API externes
6. **DevOps** : Alternative légère à Prometheus/Grafana

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Démarrage Rapide

```bash
# Vérification unique
api-monitor run config.yaml

# Surveillance continue
api-monitor watch config.yaml

# Tableau de bord web
api-monitor watch config.yaml --web
```

## Mots-clés pour la Recherche

surveillance api, vérification santé api, temps de fonctionnement api, surveillance http, test api rest, vérificateur statut api, outils devops, surveillance ci/cd, disponibilité api, surveillance point de terminaison, performance api, vérificateur statut http, garde api, vérification santé service, surveillance python, surveillance légère, outil test api, outil vérification santé, surveillance temps de fonctionnement, disponibilité service

## Informations du Repository

- **GitHub** : https://github.com/maksim4351/api-health-monitor
- **Licence** : MIT
- **Statut** : Développement actif
- **Version** : 1.0.0

**📚 Documentation complète en anglais :** [AI_INDEX.md](AI_INDEX.md)

