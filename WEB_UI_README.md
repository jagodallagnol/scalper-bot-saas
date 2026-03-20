# 🚀 SCALPER BOT · Web Interface

## 📋 Descrizione

Interfaccia web moderna per il bot di scalping trading su Binance con:
- ✅ Dashboard real-time con dati Binance
- ✅ Integrazione Binance API per prezzi live
- ✅ Esecuzione trading manuale e automatico
- ✅ Visualizzazione portafoglio e storico trade
- ✅ Controllo bot da interfaccia
- ✅ Design futuristico con tema ÆTHER

---

## 🛠️ Installazione

### 1. Installa le dipendenze

```bash
cd /Users/jagodallagnol/Desktop/projects/scalper
pip install -r requirements.txt
```

### 2. Configura le credenziali Binance

Crea o modifica il file `.env`:

```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TRADING_PAIR=XRPUSDT
LEVERAGE=5
MIN_AMOUNT=100
TARGET_GAIN=2
CHECK_INTERVAL=5
```

⚠️ **IMPORTANTE**: Le API key devono avere i permessi:
- ✅ Spot Trading (LONG)
- ✅ Futures Trading (LONG/SHORT)
- ✅ Read permissions on account

---

## 🚀 Avvio

### Metodo 1: Terminale Separati (Consigliato)

**Terminal 1 - Backend API Server:**
```bash
cd /Users/jagodallagnol/Desktop/projects/scalper
python api_server.py
```

Output atteso:
```
==================================================
SCALPER BOT · API SERVER
==================================================
Exchange connected: True
Strategy initialized: True
==================================================
 * Running on http://localhost:5000
```

**Terminal 2 - Web Server (HTTP simple):**
```bash
cd /Users/jagodallagnol/Desktop/projects/scalper
python -m http.server 8080
```

Output atteso:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

### 3. Apri il Browser

Vai su: **http://localhost:8080**

---

## 📱 Funzionalità

### Dashboard
- 📊 Prezzo attuale XRP/USDT
- 📈 Variazione 24h
- 💰 Saldo portafoglio
- 📉 Performance trading
- 🎯 Win rate e P&L totale

### Trade
- 🎮 Esecuzione manuale LONG/SHORT
- ⚙️ Impostazione Stop Loss e Take Profit
- 🤖 Avvio/Arresto bot automatico
- 📊 Visualizzazione strategia attiva

### Posizioni
- 📍 Posizioni aperte attuali
- 📜 Storico completo trade
- 💵 P&L per posizione

### Impostazioni
- 🔑 Salvataggio credenziali Binance
- ⚙️ Parametri bot (min amount, target gain)
- ℹ️ Informazioni sistema

---

## 🔌 API Endpoints

### Status
```
GET /api/status
```
Restituisce stato server e connessione

### Prezzo Real-Time
```
GET /api/price
```
Prezzo attuale, 24h high/low, volume

### Portfolio
```
GET /api/portfolio
```
Saldo totale, disponibile, in posizione, storico trade

### Indicatori
```
GET /api/indicators
```
Tutti i 19 indicatori tecnici

### Segnale Attuale
```
GET /api/signal
```
Segnale trading attuale (LONG/SHORT/NONE)

### Esegui Trade
```
POST /api/trade/execute
```
```json
{
    "type": "buy",
    "amount": 100,
    "stopLoss": 2,
    "takeProfit": 3
}
```

### Bot Control
```
POST /api/bot/start
POST /api/bot/stop
```

---

## 🎯 Indicatori Implementati (19 Totali)

### Trend (6)
- EMA 5, 13, 50
- SMA 50
- ADX
- SAR (Parabolic SAR)

### Momentum (6)
- RSI
- KDJ Stochastic
- MACD
- TRIX
- ROC (Rate of Change)
- TSI (True Strength Index)

### Volatilità (3)
- Bollinger Bands
- ATR
- Historical Volatility

### Volume (3)
- OBV
- ADL
- Volume Ratio

### Support/Resistance (2)
- Pivot Points
- Fibonacci Retracement/Extension

---

## 📊 Strategia Avanzata

### Scoring System
- Ogni indicatore contribuisce con un peso
- Score totale: -1 a +1
- LONG: score > 0.35
- SHORT: score < -0.35
- NO SIGNAL: -0.35 ≤ score ≤ 0.35

### TP/SL Dinamico
- **Take Profit**: 2.5 × ATR o Fibonacci extension
- **Stop Loss**: 1 × ATR o Pivot support

---

## 🔐 Sicurezza

- ✅ Le credenziali NON vengono salvate in localStorage per impostazione predefinita
- ✅ Comunicazione HTTPS consigliata in produzione
- ✅ CORS abilitato solo da localhost
- ✅ Rate limiting su exchange

### Protezioni Built-in
- Importo minimo per trade
- Limite P&L per stop della sessione
- Controllo saldo disponibile
- Validazione ordini

---

## 🐛 Troubleshooting

### "Connection refused: localhost:5000"
- Assicurati che api_server.py sia in esecuzione
- Verifica che Flask sia installato: `pip install Flask Flask-CORS`

### "Exchange connected: False"
- Controlla le credenziali Binance nel .env
- Verifica i permessi API su Binance
- Prova con un nuovo API key

### "Strategy initialized: False"
- Assicurati che advanced_scalper_strategy.py esista
- Esegui: `pip install -r requirements.txt`

### WebSocket Connection Error
- Normale durante la connessione iniziale
- Il bot tenterà di riconnettersi automaticamente

---

## 📈 Performance

### Backtesting
```bash
python advanced_backtest.py
```

### Quick Test
```bash
python quick_test.py
```

---

## 📄 File Principali

```
scalper/
├── index.html              # Web UI
├── api_server.py           # Backend Flask
├── js/
│   ├── app.js             # Logica app principale
│   ├── binance.js         # WebSocket Binance
│   └── trading.js         # Engine trading
├── advanced_scalper_strategy.py
├── advanced_backtester.py
├── data_manager.py
├── config.py
├── .env                   # Configurazione
└── requirements.txt
```

---

## 🚨 Disclaimer

⚠️ **ATTENZIONE**: Questo è uno strumento di trading automatico. 

- Il trading comporta rischi
- Non garantiamo profitti
- Testare sempre con importi minimi prima
- Monitorare regolarmente le posizioni

---

## 📞 Support

Per problemi:
1. Verifica i log di api_server.py
2. Controlla la console del browser (F12)
3. Verifica connessione Binance API

---

## ✨ Versione

**v1.0.0** - Release Iniziale

---

## 🎨 Design

- **Dark Theme**: #050505
- **Accent**: #ccff00 (Lime)
- **Font**: Share Tech Mono, Orbitron
- **CRT Effect**: Simulazione monitor vintage
- **Mobile Responsive**: Funziona su smartphone

---

Made with ❤️ for Crypto Traders
