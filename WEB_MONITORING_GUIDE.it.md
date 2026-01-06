# 🌐 Guida al Monitoraggio Web API

## 🚀 Avvio Rapido

### ⚡ Metodo Più Semplice (Windows)

**Basta fare doppio clic sul file:**
```
run_web_monitoring.bat
```

**Cosa succederà:**
1. ✅ Verifica automaticamente Python
2. ✅ Installa dipendenze
3. ✅ Verifica `config.yaml`
4. ✅ Richiede intervallo di verifica
5. ✅ Avvia server web
6. ✅ Apre automaticamente il browser su `http://localhost:8080`

**💡 Importante:**
- Se la porta 8080 è occupata, il sistema trova automaticamente una porta libera
- Il browser si apre automaticamente sulla porta corretta
- Premere `Ctrl+C` per fermare

## 🌐 Dashboard Web - Caratteristiche

### 📊 Scheda "Monitoring"

- Statistiche in tempo reale
- Tabella risultati con indicatori di colore
- Aggiornamento automatico ogni 5 secondi

### 🎛️ Scheda "Gestione API"

**Aggiungere nuovi API:**
- Modulo con validazione
- Campi: Nome, URL, Metodo, Timeout, Stato atteso
- 20 API popolari per aggiunta rapida
- Notifiche di successo/errore

**Gestione API:**
- Visualizza tutti gli API aggiunti
- Modifica API esistenti
- Elimina API con conferma

### 📚 Documentazione OpenAPI

- **Swagger UI** disponibile su `/api/docs`
- Documentazione interattiva per tutti gli endpoint REST

## 🔔 Notifiche

- Notifiche push del browser
- Notifiche email (se configurato)
- Avvisi su errori API

## 🛠️ Metodi di Avvio Alternativi

```bash
# Tramite riga di comando
api-monitor watch config.yaml --web

# Con intervallo personalizzato
api-monitor watch config.yaml --web --interval 30

# Con porta personalizzata
api-monitor watch config.yaml --web --port 9000
```

## 📚 Documentazione Completa

**📖 Per la documentazione completa in inglese, vedere :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Link utili:**
- 📖 **Documentazione completa:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Progetto:** https://github.com/maksim4351/api-health-monitor

