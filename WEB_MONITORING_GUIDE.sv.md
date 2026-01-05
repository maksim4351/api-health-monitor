# 🌐 API Webbövervakningsguide

## 🚀 Snabbstart

### ⚡ Enklaste Sättet (Windows)

**Dubbelklicka bara på filen:**
```
run_web_monitoring.bat
```

**Vad som händer:**
1. ✅ Kontrollerar automatiskt Python
2. ✅ Installerar beroenden
3. ✅ Kontrollerar `config.yaml`
4. ✅ Frågar efter kontrollintervall
5. ✅ Startar webbserver
6. ✅ Öppnar automatiskt webbläsare på `http://localhost:8080`

**💡 Viktigt:**
- Om port 8080 är upptagen, hittar systemet automatiskt en ledig port
- Webbläsaren öppnas automatiskt på rätt port
- Tryck på `Ctrl+C` för att stoppa

## 🌐 Webbinstrumentpanel - Funktioner

### 📊 Fliken "Monitoring"

- Realtidsstatistik
- Resultattabell med färgindikatorer
- Automatisk uppdatering var 5:e sekund

### 🎛️ Fliken "API-hantering"

**Lägg till nya API:er:**
- Formulär med validering
- Fält: Namn, URL, Metod, Timeout, Förväntad status
- 20 populära API:er för snabb tillägg
- Meddelanden om framgång/fel

**API-hantering:**
- Visa alla tillagda API:er
- Redigera befintliga API:er
- Ta bort API:er med bekräftelse

### 📚 OpenAPI-dokumentation

- **Swagger UI** tillgänglig på `/api/docs`
- Interaktiv dokumentation för alla REST-endpunkter

## 🔔 Meddelanden

- Webbläsar-push-meddelanden
- E-postmeddelanden (om konfigurerat)
- Varningar om API-fel

## 🛠️ Alternativa Startmetoder

```bash
# Via kommandorad
api-monitor watch config.yaml --web

# Med anpassat intervall
api-monitor watch config.yaml --web --interval 30

# Med anpassad port
api-monitor watch config.yaml --web --port 9000
```

## 📚 Fullständig Dokumentation

**📖 För fullständig dokumentation på engelska, se :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Användbara länkar:**
- 📖 **Fullständig dokumentation:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Projekt:** https://github.com/maksim4351/api-health-monitor

