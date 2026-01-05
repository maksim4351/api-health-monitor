# 🌐 API Web-Überwachungsleitfaden

## 🚀 Schnellstart

### ⚡ Einfachste Methode (Windows)

**Doppelklicken Sie einfach auf die Datei:**
```
run_web_monitoring.bat
```

**Was passiert:**
1. ✅ Prüft automatisch Python
2. ✅ Installiert Abhängigkeiten
3. ✅ Prüft `config.yaml`
4. ✅ Fragt nach Prüfintervall
5. ✅ Startet Webserver
6. ✅ Öffnet automatisch Browser bei `http://localhost:8080`

**💡 Wichtig:**
- Wenn Port 8080 belegt ist, findet das System automatisch einen freien Port
- Browser öffnet sich automatisch auf dem richtigen Port
- Drücken Sie `Ctrl+C` zum Beenden

## 🌐 Web-Dashboard - Funktionen

### 📊 Tab "Monitoring"

- Echtzeitstatistiken
- Ergebnistabelle mit Farbindikatoren
- Automatische Aktualisierung alle 5 Sekunden

### 🎛️ Tab "API-Verwaltung"

**Neue APIs hinzufügen:**
- Formular mit Validierung
- Felder: Name, URL, Methode, Timeout, Erwarteter Status
- 20 beliebte APIs für schnelles Hinzufügen
- Erfolgs-/Fehlermeldungen

**API-Verwaltung:**
- Alle hinzugefügten APIs anzeigen
- Bestehende APIs bearbeiten
- APIs mit Bestätigung löschen

### 📚 OpenAPI-Dokumentation

- **Swagger UI** verfügbar unter `/api/docs`
- Interaktive Dokumentation für alle REST-Endpunkte

## 🔔 Benachrichtigungen

- Browser-Push-Benachrichtigungen
- E-Mail-Benachrichtigungen (falls konfiguriert)
- Warnungen bei API-Fehlern

## 🛠️ Alternative Startmethoden

```bash
# Über Befehlszeile
api-monitor watch config.yaml --web

# Mit benutzerdefiniertem Intervall
api-monitor watch config.yaml --web --interval 30

# Mit benutzerdefiniertem Port
api-monitor watch config.yaml --web --port 9000
```

## 📚 Vollständige Dokumentation

**📖 Für die vollständige Dokumentation auf Englisch, siehe :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Nützliche Links:**
- 📖 **Vollständige Dokumentation:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Projekt:** https://github.com/maksim4351/api-health-monitor

