# Antigravity Scalper Bot

Bot di trading automatico per XRP su Binance Futures con **strategia avanzata** per scalping su timeframe 1 minuto con **16+ indicatori tecnici**.

## Caratteristiche

✅ **16+ Indicatori Tecnici**: EMA, RSI, MACD, Bollinger Bands, KDJ, SAR, Fibonacci, Pivot Points e molto altro  
✅ **Backtest Avanzato**: Testa la strategia con scoring multi-indicatore su dati storici
✅ **Trading Live**: Esegui il bot in real-time con i tuoi XRP  
✅ **Risk Management**: Gestione dinamica di stop loss e take profit basata su ATR e Fibonacci
✅ **Fear & Greed Index**: Indicatore di sentiment di mercato semplificato
✅ **Visualizzazione Avanzata**: Grafici completi con tutti gli indicatori
✅ **Logging**: Traccia tutti i trade e gli errori

## Setup

### 1. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Configura le API di Binance (per trading live)

1. Copia `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Modifica `.env` con le tue API keys da Binance:
   ```
   BINANCE_API_KEY=your_key_here
   BINANCE_SECRET_KEY=your_secret_here
   ```

3. **Importante**: Usa API keys con permessi **Futures only**, senza permessi di prelievo

### 3. Configura la strategia

Modifica `config.py` per personalizzare:
- **LEVERAGE**: Leva finanziaria (default: 5x)
- **RISK_PER_TRADE**: Rischio per singolo trade (default: 2%)
- **MAX_DAILY_LOSS**: Perdita massima giornaliera (default: 5%)
- **MA_FAST / MA_SLOW**: Periodi delle medie mobili
- **RSI_PERIOD**: Periodo RSI per overbought/oversold

## 📱 App Web & Mobile (SaaS Mode / Netlify)

Il bot include un'interfaccia grafica avanzata (Aether OS) che può essere pubblicata online gratuitamente o installata come App nativa sul tuo telefono.

### Pubblicare l'interfaccia pubblica:
1. Collega questo repository a **[Netlify](https://www.netlify.com/)** (non serve build, usa solo `index.html`).
2. Netlify genererà un link pubblico, es: `https://tuo-scalper.netlify.app`. 
3. *Sì, su Netlify basta caricare il repository così com'è. Penserà a tutto lui.*

### Installare l'App su iPhone / Android:
1. Apri il link di Netlify dal tuo smartphone (Safari su iOS, Chrome su Android).
2. Tocca l'icona **Condividi** e scegli **"Aggiungi alla schermata Home"**.
3. Avrai l'App nativa con icona. **Nota:** l'App richiede un backend Python attivo per inviare gli ordini.

### Collegare l'App Web al tuo Backend Locale (Gratis):
Se vuoi controllare il bot dal telefono mentre fa trading sul tuo PC a casa:
1. Avvia il server sul tuo PC: `python start_bot.py`
2. Esponi il tuo PC con Ngrok: `ngrok http 5000`
3. Apri l'App dal telefono, vai su **⚙️ IMPOSTAZIONI**.
4. Alla voce **"URL BACKEND"** incolla l'URL di Ngrok (aggiungendo `/api` alla fine, es. `https://1234.ngrok-free.app/api`).
5. Inserisci le tue API Keys di Bitget. (Le chiavi non vengono salvate da nessuna parte se non nella memoria temporanea del tuo browser/sessione).

## Utilizzo

### Backtest Avanzato (consigliato prima di andare live!)

```bash
python advanced_backtest.py
```

Questo testerà la strategia avanzata sui dati storici con **16+ indicatori** e genererà:
- Report dettagliato con statistiche di performance
- File `advanced_backtest_results.csv` con dettagli di ogni trade
- File `advanced_backtest_indicators.csv` con tutti gli indicatori

**Esempio output:**
```
🤖 ADVANCED SCALPER STRATEGY - BACKTEST
============================================================

📊 STATISTICHE GENERALI:
   Total Trades: 145
   Winning Trades: 92
   Losing Trades: 53
   Win Rate: 63.45%

💰 PROFITTI/PERDITE:
   Total PnL: $234.56
   ROI: 23.46%
   Initial Balance: $1000.00
   Final Balance: $1234.56

📈 METRICHE DI PERFORMANCE:
   Average Win: $5.23
   Average Loss: -$2.15
   Max Drawdown: 8.34%
   Profit Factor: 2.45
   Best Trade: $25.50
   Worst Trade: -$12.30
   Avg Bars Held: 3.2
```

### Visualizzazione Avanzata

```bash
python advanced_visualize.py
```

Genera grafici completi con:
- **Price & Moving Averages** (EMA 5, 13, 50)
- **Bollinger Bands** con banda di prezzo
- **RSI & KDJ** (Stochastic)
- **MACD** con istogramma
- **Volume & OBV** (On-Balance Volume)
- **Momentum & ADL** (Accumulation/Distribution Line)
- **ATR & Volatility** (storica e attuale)
- **Signal Strength** & Fear/Greed Index
- **Pivot Points** & Fibonacci Levels
- **Trades Execution** con entry/exit

### Backtest Classico (veloce)

```bash
python backtest.py
```

Usa la strategia originale (più veloce, meno indicatori)

### Download dati attuali da Binance

```bash
python download_data.py
```

Scarica gli ultimi 7 giorni di dati 1m e 6 mesi di dati giornalieri.

### Trading Live

```bash
python live_trading.py
```

⚠️ **ATTENZIONE**: 
- Questo è trading **reale** con denaro vero
- Assicurati che il backtest sia positivo prima di andare live
- Inizia con importi piccoli per testare
- Monitora il bot durante il trading

## Strategia Avanzata - 16+ Indicatori

### Sistema di Scoring Multi-Indicatore

Ogni indicatore ha un peso nella decisione finale. La strategia genera segnali quando lo score totale supera le soglie.

| Indicatore | Weight | Descrizione |
|----------|--------|-----------|
| **EMA Alignment** | 15% | Allineamento EMA 5-13-50 |
| **RSI** | 12% | Overbought/Oversold detection |
| **KDJ Stochastic** | 12% | Stochastic Oscillator (K,D,J) |
| **Bollinger Bands** | 12% | Mean reversion e volatility |
| **MACD** | 12% | Trend e momentum |
| **Volume/OBV** | 12% | On-Balance Volume |
| **ADL** | 8% | Accumulation/Distribution Line |
| **Momentum** | 8% | Price momentum ROC |
| **SAR** | 5% | Parabolic SAR |
| **ADX** | 5% | Average Directional Index |
| **TSI** | 3% | Trend Strength Index |
| **Fear & Greed** | 3% | Sentiment Index |

### Indicatori Inclusi

1. **EMA (Exponential Moving Averages)**
   - EMA 5 (veloce)
   - EMA 13 (media)
   - EMA 50 (lenta)
   - SMA 50

2. **Momentum Indicators**
   - RSI (14)
   - KDJ/Stochastic (9,3)
   - MACD (12,26,9)
   - Momentum (10)
   - TRIX

3. **Volatility Indicators**
   - Bollinger Bands (20,2)
   - ATR (14)
   - Historical Volatility (20)
   - Current Volatility (5)

4. **Trend Indicators**
   - ADX (14)
   - Di+ / Di-
   - SAR (Parabolic)
   - TSI (Trend Strength)

5. **Volume Indicators**
   - OBV (On-Balance Volume)
   - ADL (Accumulation/Distribution)
   - Volume MA (20)
   - Volume Ratio

6. **Support/Resistance**
   - Pivot Points (S3, S2, S1, P, R1, R2, R3)
   - Fibonacci Retracement (23.6%, 38.2%, 50%, 61.8%, 100%)
   - Fibonacci Extensions (138.2%, 161.8%, 200%)

7. **Sentiment**
   - Fear & Greed Index (basato su RSI + Volume + Momentum)
   - Classificazione: Fear → Neutral → Greed → Euphoria

### Segnali di Entrata

**LONG** quando:
- Score totale > 0.35
- Combinazione di indicatori bullish
- Volatility e Volume concordano

**SHORT** quando:
- Score totale < -0.35
- Combinazione di indicatori bearish
- Volatility e Volume concordano

### Exit Dinamico

- **Take Profit**: Basato su ATR (2.5x) + Fibonacci Extensions
- **Stop Loss**: Basato su ATR (1x) + Support/Resistance
- **Segnale Opposto**: Chiude la posizione

### Parametri Configurabili

Modifica `advanced_scalper_strategy.py` per personalizzare:

## File Structure

```
scalper/
├── config.py                      # Configurazione parametri
├── data_manager.py                # Gestione dati (locale e live)
├── strategy.py                    # Strategia originale
├── advanced_scalper_strategy.py   # ⭐ Nuova strategia avanzata (16+ indicatori)
├── backtester.py                  # Engine backtest originale
├── advanced_backtester.py         # ⭐ Engine backtest avanzato
├── backtest.py                    # Script backtest originale
├── advanced_backtest.py           # ⭐ Script backtest avanzato (usa 16+ indicatori)
├── advanced_visualize.py          # ⭐ Visualizzazione avanzata con grafici
├── live_trader.py                 # Bot per trading live
├── live_trading.py                # Script principale trading live
├── download_data.py               # Download dati da Binance
├── requirements.txt               # Dipendenze Python
├── .env.example                   # Template configurazione
├── README.md                      # Questo file
└── data/                          # Cartella dati storici
    └── XRPUSD_1m_Binance.csv
```

## Output Files

### Dalla Strategia Avanzata

- **`advanced_backtest_results.csv`** - Dettagli di tutti i trades (entry, exit, PnL, etc)
- **`advanced_backtest_indicators.csv`** - Tutti gli indicatori per ogni candle
- **`advanced_strategy_analysis.png`** - Grafico completo con tutti gli indicatori
- **`pivot_fibonacci_analysis.png`** - Grafico con Pivot Points e Fibonacci
- **`trades_execution.png`** - Grafico con i trades eseguiti

### Dal Backtest Classico

- **`backtest_results.csv`** - Dettagli dei trades
- **`backtest.log`** - Log di esecuzione

## Sicurezza

- ❌ Non committare `.env` con le API keys in Git
- ❌ Non usare API keys con permessi di prelievo
- ✅ Usa API keys separate per backtest e live (se possibile)
- ✅ Testa sempre in backtest prima di andare live

## Troubleshooting

### "ModuleNotFoundError: No module named 'ta'"
```bash
pip install ta
```

### "ModuleNotFoundError: No module named 'ccxt'"
```bash
pip install ccxt
```

### "ModuleNotFoundError: No module named 'advanced_scalper_strategy'"
Assicurati di essere nella directory corretta e di aver eseguito `pip install -r requirements.txt`

### "Errore nel caricamento dei dati"
- Controlla la connessione internet
- Verifica che il file CSV esista in `data/`
- Esegui `python download_data.py` per scaricare i dati

### "Segnali troppo deboli o assenti"
- Modifica la soglia `min_signal_strength` in `advanced_backtest.py` (default: 0.35)
- Regola i pesi degli indicatori in `advanced_scalper_strategy.py`
- Aumenta il lookback period per i pivot points

### Performance scadente nel backtest
1. Verifica che i dati siano di qualità
2. Prova a ottimizzare i parametri degli indicatori
3. Aumenta `RISK_PER_TRADE` nel config (con cautela!)
4. Esegui `python optimize.py` per l'ottimizzazione automatica

## Note Tecniche

### Indicatori Calcolati da `ta-lib`:

```python
# EMA
EMAIndicator(close, window).ema_indicator()

# RSI
RSIIndicator(close, window).rsi()

# Stochastic (KDJ)
StochasticOscillator(high, low, close, window, smooth_window).stoch()

# Bollinger Bands
BollingerBands(close, window, window_dev)

# MACD
MACD(close, window_fast, window_slow, window_sign)

# ATR
AverageTrueRange(high, low, close, window).average_true_range()

# OBV
OnBalanceVolumeIndicator(close, volume).on_balance_volume()

# ADL
AccDistIndexIndicator(high, low, close, volume).acc_dist_index()
```

### Calcoli Personalizzati:

- **Parabolic SAR**: Algoritmo proprietario con AF 0.02-0.2
- **Fibonacci Levels**: Basati su max/min ultimi 50 candle
- **Pivot Points**: Calcolo standard (P, S1, S2, S3, R1, R2, R3)
- **Fear & Greed Index**: Media ponderata RSI (35%) + Volume (35%) + Momentum (30%)
- **TSI**: Triple EMA smoothing su momentum

## Disclaimer

⚠️ **Questo bot è per scopi educativi**. Il trading con leva comporta rischi significativi di perdita. Non è garantito il profitto. Usa solo capitale che puoi permetterti di perdere.

## Support

Per errori o domande, controlla:
1. Il file `trading.log` per i dettagli degli errori
2. I parametri in `config.py` e `advanced_scalper_strategy.py`
3. La qualità dei dati storici in `data/`
4. Esegui il backtest avanzato per validare la strategia

## Versione

- **v2.0** - Advanced Edition con 16+ indicatori
- **v1.0** - Original Edition (strategy.py + backtest.py)
