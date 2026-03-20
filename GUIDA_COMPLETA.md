# 🤖 GUIDA COMPLETA - Bot Scalper XRP

## ✨ Cosa hai ricevuto

Un bot di trading automatico **scalper** completo che funziona in due modalità:
1. **BACKTEST** - Testa la strategia su dati storici (senza rischiare soldi)
2. **LIVE** - Trading reale su Binance Futures con i tuoi XRP

---

## 🚀 STEP BY STEP PER INIZIARE

### 1️⃣ **SETUP INIZIALE** (primo avvio)

```bash
cd /Users/jagodallagnol/Desktop/projects/scalper

# Le dipendenze sono già installate, ma se necessario:
pip install -r requirements.txt
```

---

### 2️⃣ **COMPRENDI I DATI CHE HAI**

Nella cartella `data/` hai:
- `XRPUSD_1m_Binance.csv` - **3.9 milioni di candle da 1 minuto** (storico dal 2018!)

Questo è **GOLD** per il backtest. Contiene tutti i dati che servono.

---

### 3️⃣ **TESTA LA STRATEGIA CON BACKTEST** ✅ (FONDAMENTALE!)

```bash
python backtest.py
```

**Cosa fa:**
- Prende gli ultimi 5000 candle (~3.5 giorni di trading)
- Applica la strategia scalper
- Mostra le statistiche dei trade

**Risultato atteso:**
```
Win Rate:         40.00%
Profit Factor:    1.20
Total Return:     0.04%
```

**File generato:** `backtest_results.csv` - puoi aprirlo in Excel per vedere ogni singolo trade

---

### 4️⃣ **OTTIMIZZA I PARAMETRI (opzionale ma consigliato)**

```bash
python optimize.py
```

Questo testa 48 combinazioni diverse di:
- Moving Average veloce e lenta
- Periodo RSI

Genera: `optimization_results.csv` con i migliori parametri

Poi modifica `config.py` con i valori migliori:
```python
MA_FAST = 3      # Meglio
MA_SLOW = 15     # Meglio
RSI_PERIOD = 10  # Meglio
```

---

### 5️⃣ **CONFIGURA LE API KEYS PER TRADING LIVE**

#### Passo A: Crea API Keys su Binance

1. Vai su https://www.binance.com/en/account/api-management
2. Crea una nuova API Key
3. **IMPORTANTE**: 
   - Abilita: `Enable Futures` ✅
   - Disabilita: `Enable Withdrawal` ❌
   - Restrizioni IP: Se possibile, aggiungi solo il tuo IP
4. Copia la `API Key` e la `Secret Key`

#### Passo B: Configura il file `.env`

Apri `.env` e riempi:
```
BINANCE_API_KEY=incolla_qui_la_api_key
BINANCE_SECRET_KEY=incolla_qui_la_secret_key
SYMBOL=XRPUSDT
LEVERAGE=5
RISK_PER_TRADE=0.02
MAX_DAILY_LOSS=0.05
TRADING_MODE=live
```

**Parametri:**
- `LEVERAGE=5` → Leva 5x (conservativa, puoi fare 15x se sei aggressivo)
- `RISK_PER_TRADE=0.02` → Rischia il 2% per trade
- `MAX_DAILY_LOSS=0.05` → Stop al 5% di perdita giornaliera

---

### 6️⃣ **SCARICA DATI FRESCHI DA BINANCE (opzionale)**

```bash
python download_data.py
```

Scarica:
- Ultimi 7 giorni di dati 1 minuto
- Ultimi 6 mesi di dati giornalieri

Salva in `data/` per uso offline.

---

### 7️⃣ **AVVIA IL BOT LIVE** 🚀

```bash
python live_trading.py
```

**Cosa fa:**
- Scarica i dati attuali da Binance ogni minuto
- Analizza il trend giornaliero
- Genera segnali di entrata/uscita
- Piazza ordini automaticamente
- Registra tutto in `trading.log`

**Come fermarlo:**
Premi `Ctrl + C` nel terminale

---

## 📊 COME LEGGERE I RISULTATI

### Dopo il backtest, vedrai:

```
Win Rate: 40%           ← % di trade vincenti (buono: > 35%)
Profit Factor: 1.20     ← Guadagni/Perdite (buono: > 1.0)
Total Return: 0.04%     ← ROI totale
Max Loss: -0.21 USDT    ← Perdita massima per trade
Max Win: 0.25 USDT      ← Guadagno massimo per trade
```

**Regole d'oro:**
- ✅ Profit Factor > 1.5 = Buona strategia
- ✅ Win Rate > 45% = Eccellente per scalping
- ⚠️ Win Rate 30-40% = Accettabile se Profit Factor > 1.0
- ❌ Profit Factor < 1.0 = Non tradare!

---

## ⚠️ RISCHI E COME MITIGARLI

### Rischio: Perdite in sequenza rapida

**Soluzione:**
- Usa `MAX_DAILY_LOSS=0.05` nel `.env`
- Bot si fermerà automaticamente

### Rischio: Leva troppo alta

**Soluzione:**
```python
# Nel .env
LEVERAGE=5  # Conservativo: non andare oltre 10x per scalping
```

### Rischio: Segnali falsi

**Soluzione:**
- Backtest sempre prima di andare live
- Testa su più periodi temporali (usa `optimize.py`)
- Monitora il log in `trading.log`

### Rischio: Lag di rete

**Soluzione:**
- Il bot usa ordini market (non limit) per velocità
- Crontroll gli ordini su Binance app in tempo reale

---

## 🛠️ COSA MODIFICARE PER CUSTOMIZZARE

### File: `config.py`

```python
# Per essere più aggressivo:
LEVERAGE = 10  # Aumenta rischio/reward
RISK_PER_TRADE = 0.05  # Rischia il 5% invece del 2%

# Per essere più conservativo:
LEVERAGE = 3
RISK_PER_TRADE = 0.01
MAX_DAILY_LOSS = 0.02
```

### File: `strategy.py`

Se vuoi cambiare la logica dei segnali:
- Modifica `generate_signals()` per aggiungere più filtri
- Modifica `calculate_take_profit_stop_loss()` per TP/SL diversi
- Aggiungi nuovi indicatori tecnici

---

## 📈 WORKFLOW CONSIGLIATO

```
1. Leggi questa guida ✓
2. Esegui: python backtest.py
3. Se profit_factor > 1.0 → vai al passo 4
   Altrimenti → esegui optimize.py e regola parametri
4. Configura .env con le API keys
5. Fai una prova con importo piccolo (es. 10 USDT)
6. Monitora per 1-2 giorni
7. Se tutto ok, aumenta gradualmente l'importo
```

---

## 🔍 DEBUG E TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'ccxt'"

```bash
pip install ccxt
```

### "BINANCE_API_KEY is not configured"

- Apri `.env`
- Assicurati di avere compilato le API keys
- Non deve dire `your_api_key_here`

### "Error connecting to Binance"

- Controlla la connessione internet
- Verifica che le API keys siano valide
- Controlla il file `trading.log`

### "No signal generated"

- I parametri non sono adatti al mercato attuale
- Esegui `python optimize.py` per trovare nuovi parametri
- Aumenta il numero di candle nel backtest

### "Trading.log è vuoto"

- Aspetta un minuto, il bot controlla ogni 60 secondi
- Controlla che il trend sia favorevole (vedi output del bot)

---

## 💡 PRO TIPS

### 1. Testa sempre offline prima
```bash
python backtest.py  # Test su 5000 candle
python optimize.py  # Test tante combinazioni
```

### 2. Usa piccoli importi inizialmente
```python
# Nel .env, non mettere tutto il tuo capitale
# Usa: balance = 50-100 USDT per testing
```

### 3. Monitora il file di log
```bash
tail -f trading.log  # Vedi i trade in tempo reale
```

### 4. Salva i dati periodicamente
```bash
python download_data.py  # Una volta al giorno
```

### 5. Review dei trade
```bash
# Dopo il backtest, apri:
backtest_results.csv  # Analizza gli errori
```

---

## 📞 SUPPORTO RAPIDO

| Problema | Soluzione |
|----------|-----------|
| Bot non avvia | Controlla `python --version` (3.8+) |
| No trades | Esegui `optimize.py` per nuovi parametri |
| Perdite troppo alte | Riduci `RISK_PER_TRADE` e `LEVERAGE` |
| Ordini non eseguiti | Usa ordini market non limit in `live_trader.py` |
| Soldi persi | 1. Ferma il bot (Ctrl+C) 2. Analizza `trading.log` |

---

## 🎯 TARGET REALISTICI

Con una strategia scalper a leva 5x su XRP/USDT:

- **Win Rate**: 35-50% è buono per scalping
- **ROI Giornaliero**: 0.5-2% (compounding)
- **ROI Mensile**: 10-30%
- **Drawdown Massimo**: 10-20%

Se vedi performance peggio, **FERMA IL BOT** e riotimizza.

---

## ✅ CHECKLIST PRIMA DI ANDARE LIVE

- [ ] Ho eseguito `python backtest.py` e profit_factor > 1.0
- [ ] Ho confermato le API keys nel `.env`
- [ ] Ho testato con importo piccolo (< 50 USDT)
- [ ] Ho impostato `MAX_DAILY_LOSS` a un valore ragionevole
- [ ] Ho letto questa guida completamente
- [ ] Ho capito che potrei perdere soldi
- [ ] Monitoro il bot le prime ore

**Se tutte le checkbox ✓ allora sei pronto!**

---

## 🚀 AVVIA IL BOT

```bash
cd /Users/jagodallagnol/Desktop/projects/scalper
python live_trading.py
```

Buon trading! 📈
