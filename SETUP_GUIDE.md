# 🚀 SCALPER BOT · SETUP COMPLETO

## ✅ LISTA DI CONTROLLO INSTALLAZIONE

- [ ] Python 3.8+ installato
- [ ] Progetto scaricato: `/Users/jagodallagnol/Desktop/projects/scalper`
- [ ] File `requirements.txt` presente
- [ ] File `api_server.py` presente
- [ ] File `index.html` presente
- [ ] Cartella `js/` creata
- [ ] File `.env` configurato

---

## 📦 STEP 1: Installa Dipendenze

```bash
cd /Users/jagodallagnol/Desktop/projects/scalper
pip install -r requirements.txt
```

**Pacchetti installati:**
- `ccxt` - API Binance
- `pandas` - Analisi dati
- `numpy` - Calcoli numerici
- `ta` - Indicatori tecnici
- `requests` - HTTP client
- `python-dotenv` - Gestione variabili ambiente
- `Flask` - Server web
- `Flask-CORS` - CORS per API
- `matplotlib` - Visualizzazione grafici

---

## 🔑 STEP 2: Configura Credenziali Binance

### Opzione A: Via File .env (Automatico)

Crea file `.env` nella cartella scalper:

```env
# Binance API
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

# Trading Configuration
TRADING_PAIR=XRPUSDT
LEVERAGE=5

# Bot Parameters
MIN_AMOUNT=100
TARGET_GAIN=2
CHECK_INTERVAL=5
```

### Opzione B: Via Interfaccia Web (Consigliato)

1. Avvia il bot
2. Vai a **Settings** (⚙️)
3. Inserisci API Key e Secret
4. Clicca **SALVA CREDENZIALI**

---

## 🏃 STEP 3: Avvio Rapido

### Metodo Automatico (Consigliato)

```bash
python start_bot.py
```

Lo script farà automaticamente:
- ✅ Verifica dipendenze
- ✅ Avvia backend API (localhost:5000)
- ✅ Avvia web server (localhost:8080)
- ✅ Apre il browser

### Metodo Manuale (Avanzato)

**Terminal 1 - Backend:**
```bash
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
python -m http.server 8080
```

**Terminal 3 - Browser:**
```bash
open http://localhost:8080
```

---

## 🌐 STEP 4: Accedi al Bot

Apri il browser:
```
http://localhost:8080
```

Vedrai la dashboard con:
- 📊 Prezzo in tempo reale
- 💰 Saldo portafoglio
- 📈 Statistiche trading
- 🎮 Controlli trading

---

## ⚙️ STEP 5: Configurazione Iniziale

### 1. Collezione Portafoglio
- Vai a **Settings** (⚙️)
- Inserisci credenziali Binance
- Salva

### 2. Impostazioni Bot
- Nel tab **Settings**:
  - Importo minimo per trade: **100 USDT**
  - Guadagno target: **2%**
  - Intervallo controllo: **5 secondi**
- Clicca **SALVA PARAMETRI**

### 3. Prova Trade Manuale
- Vai a **Trade** (💹)
- Tipo: ACQUISTA
- Importo: 100
- Stop Loss: 2%
- Take Profit: 3%
- Clicca **ACQUISTA**

### 4. Avvia Bot Automatico
- Vai a **Trade** (💹)
- Sezione **STRATEGIE**
- Clicca **AVVIA BOT**
- Stato cambia a "RUNNING"

---

## 📊 INTERFACCIA UTENTE

### Layout

```
┌─ HEADER ─────────────────────────────┐
│  SCALPER BOT  [●]ONLINE  $0.0000 ±X% │
├─ TABS ───────────────────────────────┤
│ DASHBOARD | TRADE | POSIZIONI | SET  │
├───────────────────────────────────────┤
│                                       │
│  [CONTENUTO PRINCIPALE]               │
│                                       │
├─ FOOTER NAV ──────────────────────────┤
│  📊  💹  📈  ⚙️                       │
└───────────────────────────────────────┘
```

### Tab Dashboard

Visualizza:
- **Stato Mercato**: Prezzo, 24h HIGH/LOW, Volume
- **Performance**: Trade totali, Win Rate, P&L
- **Portafoglio**: Saldo totale, disponibile, in posizione

### Tab Trade

Funzioni:
- Esecuzione manuale buy/sell
- Impostazione SL/TP
- Avvia/arresta bot
- Visualizza strategia attiva

### Tab Posizioni

Mostra:
- Posizioni aperte
- Storico trade con dettagli
- P&L per ogni operazione

### Tab Impostazioni

Configura:
- Credenziali Binance
- Parametri estrategia
- Dati di sistema

---

## 🤖 BOT AUTOMATICO

### Come Funziona

1. Bot raccoglie dati price ogni 1-5 secondi
2. Calcola 19 indicatori tecnici
3. Genera segnale (LONG/SHORT/NONE)
4. Se segnale valido:
   - Calcola TP/SL dinamici
   - Apre posizione
   - Monitora fino a TP o SL

### Segnali

- **LONG**: Buy quando score > 0.35
- **SHORT**: Sell quando score < -0.35
- **NONE**: Aspetta quando -0.35 ≤ score ≤ 0.35

### TP/SL

- **Take Profit**: Entry + (2.5 × ATR)
- **Stop Loss**: Entry - (1 × ATR)

---

## 📈 PERFORMANCE

### Metriche Importanti

```
Win Rate:       % trade vincenti
Profit Factor:  Profitti totali / Perdite totali
Max Drawdown:   Peggior calo di saldo
Sharpe Ratio:   Rendimento rischiustato
Daily P&L:      Profitto/perdita giornaliero
```

### Target Realistici

```
Win Rate:       50-65%
Profit Factor:  1.2-2.0
Max Drawdown:   10-25%
Sharpe Ratio:   >1.0
Daily Target:   0.5-2% su saldo
```

---

## 🔐 SICUREZZA

### Best Practices

✅ **DO:**
- Usa API con permessi limitati
- Disabilita "Allow Withdrawal" in Binance
- Ruota le API key regolarmente
- Monitora gli accessi a Binance

❌ **DON'T:**
- Non condividere API key
- Non salvare credenziali in plain text (salvo nel browser)
- Non usare la stessa API per più bot
- Non lasciar controllare il bot indefinitamente

---

## 🐛 ERRORI COMUNI

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install Flask Flask-CORS
```

### "binance api error: invalid api key"
- Verificare credenziali in .env
- Ricreate nuove API key su Binance

### "ConnectionError: localhost:5000"
- Verificare api_server.py in esecuzione
- Porta 5000 è disponibile?

### "No data received"
- Verificare connessione internet
- Binance è down?
- Prova diversa coppia trading

---

## 📝 COMANDI UTILI

```bash
# Visualizza log del bot
tail -f api_server.log

# Verifica processi in esecuzione
ps aux | grep python

# Ferma un processo (PID)
kill -9 <PID>

# Verifica porta occupata
lsof -i :5000
lsof -i :8080

# Installa dipendenza singola
pip install <package_name>

# Aggiorna tutte le dipendenze
pip install --upgrade -r requirements.txt
```

---

## 🎯 WORKFLOW GIORNALIERO

### Morning
1. Avvia bot: `python start_bot.py`
2. Controlla Dashboard
3. Verifica Win Rate e P&L

### During Trading
1. Monitora ogni 1-2 ore
2. Controlla tab Posizioni
3. Nota le condizioni di mercato

### Evening
1. Rivedi storico trade
2. Analizza performance
3. Aggiusta parametri se necessario

### Before Bed
1. Decidi se lasciare bot attivo
2. Imposta limiti massimi
3. Ferma se volatile

---

## 📊 BACKTESTING

Testa la strategia su dati storici:

```bash
python advanced_backtest.py
```

Genera report con:
- Trade analysis
- Equity curve
- Performance metrics
- Win rate storico

---

## 💰 GESTIONE RISCHIO

### Position Sizing

```
1% Rule:    Risk 1% del capitale per trade
2% Rule:    Esporre max 2% per posizione
Kelly:      f* = (bp - q) / b  (formula Kelly)
```

### Stop Loss Placement

```
ATR Multiple:   SL = Entry - 1.5 × ATR
Pivot Points:   SL = Nearest Pivot
Fibonacci:      SL = Fibonacci Level 0.236
```

### Profit Taking

```
Partial:    Chiudi 50% a +1% guadagno
Full:       Chiudi rimanente a +2% guadagno
Trailing:   SL dinamico a +0.5% dai massimi
```

---

## 🚀 PROSSIMO LIVELLO

### Ottimizzazione
- Backtesta con parametri diversi
- Trova il miglior SL/TP ratio
- Identifica orari migliori

### Monitoraggio
- Guarda le metriche di rischio
- Adatta a condizioni di mercato
- Ferma se drawdown eccessivo

### Scaling
- Aumenta importo lentamente
- Diversifica su più coppie
- Combina più strategie

---

## 📞 SUPPORTO VELOCE

| Problema | Soluzione |
|----------|-----------|
| Nessun segnale | Aumenta sensibilità indicatori |
| Troppi segnali falsi | Riduci sensibilità, aumenta filtri |
| Perdite continue | Aumenta SL, riduci TP % |
| Drawdown alto | Riduci importo minimo trade |
| API non risponde | Riavvia api_server.py |
| Browser non aggiorna | F5 refresh, verifica CORS |

---

## ✨ PROSSIME CARATTERISTICHE

- [ ] Grafico candele in tempo reale
- [ ] Visualizzazione indicatori live
- [ ] Telegram notifications
- [ ] Database trade storico
- [ ] Analisi backtest avanzata
- [ ] Risk calculator
- [ ] Multi-pair trading
- [ ] Strategy optimizer
- [ ] Mobile app native

---

## 📄 FILE STRUTTURA

```
scalper/
├── index.html                 # Web UI principale
├── api_server.py             # Backend Flask
├── start_bot.py              # Script avvio automatico
├── js/
│   ├── app.js               # Logica interfaccia
│   ├── binance.js           # WebSocket Binance
│   └── trading.js           # Engine trading
├── advanced_scalper_strategy.py
├── advanced_backtester.py
├── advanced_config.py
├── data_manager.py
├── requirements.txt         # Dipendenze Python
├── .env                     # Configurazione locale
├── WEB_UI_README.md        # Documentazione UI
├── QUICK_START_WEB.py      # Guida rapida
└── SETUP_GUIDE.md          # Questo file
```

---

Made with ❤️ for Crypto Traders

**v1.0.0 · Advanced Scalping Bot**
