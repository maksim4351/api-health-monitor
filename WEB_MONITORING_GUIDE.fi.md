# 🌐 API Verkkoseuranta-opas

## 🚀 Pikakäynnistys

### ⚡ Yksinkertaisin tapa (Windows)

**Kaksoisnapsauta tiedostoa:**
```
run_web_monitoring.bat
```

**Mitä tapahtuu:**
1. ✅ Tarkistaa automaattisesti Pythonin
2. ✅ Asentaa riippuvuudet
3. ✅ Tarkistaa `config.yaml`
4. ✅ Kysyy tarkistusväliä
5. ✅ Käynnistää web-palvelimen
6. ✅ Avaa automaattisesti selaimen osoitteessa `http://localhost:8080`

**💡 Tärkeää:**
- Jos portti 8080 on varattu, järjestelmä löytää automaattisesti vapaan portin
- Selain avautuu automaattisesti oikealle portille
- Paina `Ctrl+C` lopettaaksesi

## 🌐 Verkkokäyttöliittymä - Ominaisuudet

### 📊 "Seuranta"-välilehti

- Reaaliaikaiset tilastot
- Tulostaulukko värillisillä indikaattoreilla
- Automaattinen päivitys 5 sekunnin välein

### 🎛️ "API-hallinta"-välilehti

**Lisää uusia API:ja:**
- Lomake validoinnilla
- Kentät: Nimi, URL, Metodi, Aikakatkaisu, Odotettu tila
- 20 suosittua API:a nopeaa lisäystä varten
- Onnistumis-/virheilmoitukset

**API-hallinta:**
- Näytä kaikki lisätyt API:t
- Muokkaa olemassa olevia API:ja
- Poista API:t vahvistuksella

### 📚 OpenAPI-dokumentaatio

- **Swagger UI** saatavilla osoitteessa `/api/docs`
- Interaktiivinen dokumentaatio kaikille REST-päätepisteille

## 🔔 Ilmoitukset

- Selaimen push-ilmoitukset
- Sähköposti-ilmoitukset (jos määritelty)
- Varoitukset API-virheistä

## 🛠️ Vaihtoehtoiset käynnistysmenetelmät

```bash
# Komentorivin kautta
api-monitor watch config.yaml --web

# Mukautetulla välillä
api-monitor watch config.yaml --web --interval 30

# Mukautetulla portilla
api-monitor watch config.yaml --web --port 9000
```

## 📚 Täydellinen dokumentaatio

**📖 Täydelliselle englanninkieliselle dokumentaatiolle, katso :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Hyödylliset linkit:**
- 📖 **Täydellinen dokumentaatio:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Projekti:** https://github.com/maksim4351/api-health-monitor

