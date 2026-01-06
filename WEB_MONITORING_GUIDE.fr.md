# 🌐 Guide de Surveillance Web API

## 🚀 Démarrage Rapide

### ⚡ Méthode la Plus Simple (Windows)

**Double-cliquez simplement sur le fichier :**
```
run_web_monitoring.bat
```

**Ce qui se passera :**
1. ✅ Vérifie automatiquement Python
2. ✅ Installe les dépendances
3. ✅ Vérifie `config.yaml`
4. ✅ Demande l'intervalle de vérification
5. ✅ Démarre le serveur web
6. ✅ Ouvre automatiquement le navigateur à `http://localhost:8080`

**💡 Important :**
- Si le port 8080 est occupé, le système trouve automatiquement un port libre
- Le navigateur s'ouvre sur le bon port automatiquement
- Appuyez sur `Ctrl+C` pour arrêter

## 🌐 Tableau de Bord Web - Fonctionnalités

### 📊 Onglet "Monitoring"

- Statistiques en temps réel
- Tableau des résultats avec indicateurs de couleur
- Mise à jour automatique toutes les 5 secondes

### 🎛️ Onglet "Gestion API"

**Ajouter de nouveaux API :**
- Formulaire avec validation
- Champs : Nom, URL, Méthode, Timeout, Statut attendu
- 20 API populaires pour ajout rapide
- Notifications de succès/erreur

**Gestion des API :**
- Voir tous les API ajoutés
- Modifier les API existants
- Supprimer les API avec confirmation

### 📚 Documentation OpenAPI

- **Swagger UI** disponible à `/api/docs`
- Documentation interactive pour tous les endpoints REST

## 🔔 Notifications

- Notifications push du navigateur
- Notifications email (si configuré)
- Alertes sur les erreurs API

## 🛠️ Méthodes de Lancement Alternatives

```bash
# Via ligne de commande
api-monitor watch config.yaml --web

# Avec intervalle personnalisé
api-monitor watch config.yaml --web --interval 30

# Avec port personnalisé
api-monitor watch config.yaml --web --port 9000
```

## 📚 Documentation Complète

**📖 Pour la documentation complète en anglais, voir :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Liens utiles:**
- 📖 **Documentation complète:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Projet:** https://github.com/maksim4351/api-health-monitor

