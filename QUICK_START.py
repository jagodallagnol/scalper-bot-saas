"""
QUICK START GUIDE - Advanced Scalper Strategy
Guida rapida per iniziare con la strategia avanzata
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   XRP SCALPER BOT - ADVANCED EDITION                         ║
║                    Quick Start Guide - 16+ Indicatori                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 STEP 1: INSTALLAZIONE DIPENDENZE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    pip install -r requirements.txt

    Se ricevi errore su ta-lib, usa (macOS):
    brew install ta-lib
    pip install ta-lib

📥 STEP 2: SCARICARE I DATI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    python download_data.py

    Questo scaricherà:
    - Ultimi 7 giorni di dati 1m (timeframe di trading)
    - 6 mesi di dati giornalieri (filtro trend)

🧪 STEP 3: ESEGUIRE IL BACKTEST AVANZATO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    python advanced_backtest.py

    Output:
    ✅ advanced_backtest_results.csv - Tutti i trades
    ✅ advanced_backtest_indicators.csv - Indicatori per ogni candle
    
    Report stampato a schermo:
    - Total Trades
    - Win Rate
    - ROI
    - Max Drawdown
    - Profit Factor
    - Best/Worst Trade

📊 STEP 4: VISUALIZZARE I RISULTATI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    python advanced_visualize.py

    Selezionare opzione:
    1. Tutti gli indicatori (8 grafici)
    2. Pivot Points & Fibonacci
    3. Esecuzione Trades
    4. Tutte le visualizzazioni
    
    Genera PNG:
    - advanced_strategy_analysis.png (8 grafici completi)
    - pivot_fibonacci_analysis.png (support/resistance)
    - trades_execution.png (entry/exit)

🎯 STEP 5: CONFIGURARE LA STRATEGIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Modifica advanced_config.py per personalizzare:
    
    - EMA_FAST, EMA_MEDIUM, EMA_SLOW
    - RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD
    - KDJ_PERIOD, BB_PERIOD, MACD_*
    - LONG_SIGNAL_THRESHOLD, SHORT_SIGNAL_THRESHOLD
    - WEIGHT_* (pesi degli indicatori)
    - TP_ATR_MULTIPLIER, SL_ATR_MULTIPLIER

    Dopo modifiche: torna al STEP 3 per nuovo backtest

🚀 STEP 6: OTTIMIZZAZIONE (OPZIONALE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    python optimize.py

    Ottimizza automaticamente i parametri per migliore ROI
    Output: optimization_results.csv

💰 STEP 7: TRADING LIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ⚠️  SOLO SE IL BACKTEST È POSITIVO!

    1. Copia .env.example a .env
    2. Aggiungi BINANCE_API_KEY e BINANCE_SECRET_KEY
    3. Esegui: python live_trading.py
    
    ⚠️  RISCHI:
    - Trading reale con denaro vero
    - Leva finanziaria amplifica perdite
    - Nessuna garanzia di profitto
    - Inizia con piccole quantità

═══════════════════════════════════════════════════════════════════════════════

🎓 INDICATORI PRINCIPALI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 TREND INDICATORS (Individuano il trend)
  • EMA 5/13/50: Media mobile esponenziale (lungo+medio+corto)
  • ADX: Forza del trend (>25 = trend forte)
  • SAR: Punti di inversione parabolici
  • TSI: Forza della tendenza

📊 MOMENTUM INDICATORS (Individuano la velocità)
  • RSI: Overbought/Oversold (>70 o <30)
  • MACD: Convergenza/divergenza medie
  • KDJ: Stochastic oscillator
  • Momentum: Velocità di cambio prezzo

🎯 VOLATILITY INDICATORS (Individuano l'incertezza)
  • Bollinger Bands: Fasce di volatilità
  • ATR: Gamma vera media
  • Historical Volatility: Volatilità storica

💧 VOLUME INDICATORS (Confermano i trend)
  • OBV: On-Balance Volume
  • ADL: Accumulation/Distribution Line
  • Volume Ratio: Volume vs media

🔧 SUPPORT/RESISTANCE
  • Pivot Points: S3, S2, S1, P, R1, R2, R3
  • Fibonacci: Livelli di ritracciamento ed estensione

😨 SENTIMENT
  • Fear & Greed: Indice di sentiment semplificato

═══════════════════════════════════════════════════════════════════════════════

⚙️  SISTEMA DI SCORING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ogni indicatore contribuisce con un score da -1 a 1:

┌─────────────────────────────────────────────────────────┐
│ EMA Alignment (15%)        → -1 (short) ... +1 (long)   │
│ RSI (12%)                  → Overbought/Oversold        │
│ KDJ (12%)                  → Stochastic levels          │
│ Bollinger Bands (12%)      → Mean reversion             │
│ MACD (12%)                 → Trend direction            │
│ Volume/OBV (12%)           → Volume confirmation        │
│ ADL (8%)                   → Accumulation signal        │
│ Momentum (8%)              → Momentum direction         │
│ SAR (5%)                   → Pivot reversal             │
│ ADX (5%)                   → Trend strength             │
│ TSI (3%)                   → Trend quality              │
│ Fear & Greed (3%)          → Sentiment                  │
├─────────────────────────────────────────────────────────┤
│ TOTAL SCORE = -1 a +1                                   │
│                                                          │
│ Score > +0.35  → LONG SIGNAL ✅                         │
│ Score < -0.35  → SHORT SIGNAL ✅                        │
│ -0.35 < Score < +0.35 → HOLD ⏸️                         │
└─────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

💡 CONSIGLI PER MIGLIORI RISULTATI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ Test sempre su backtest prima di live
2. ✅ Verifica la qualità dei dati storici
3. ✅ Non scambiare durante report economici
4. ✅ Inizia con RISK_PER_TRADE basso (1-2%)
5. ✅ Monitora le commissioni Binance
6. ✅ Usa stop loss SEMPRE
7. ✅ Comincia con piccole quantità
8. ✅ Registra tutti i trades per analizzare

❌ Errori comuni:
1. Leverage troppo alto
2. Risk per trade troppo alto
3. Nessun stop loss
4. Trading su dati di bassa qualità
5. Aspettative di profitti garantiti
6. Ignorare il drawdown
7. Fare trading quando emotions prevalgono
8. Non diversificare timeframe

═══════════════════════════════════════════════════════════════════════════════

📞 SUPPORTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Se hai problemi:

1. Controlla trading.log per errori
2. Leggi README.md sezione Troubleshooting
3. Verifica configurazione in config.py
4. Esegui di nuovo download_data.py
5. Controlla connessione internet e Binance API

═══════════════════════════════════════════════════════════════════════════════

⚖️  DISCLAIMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  QUESTO BOT È PER SCOPI EDUCATIVI
⚠️  IL TRADING CON LEVA COMPORTA RISCHI SIGNIFICATIVI
⚠️  NESSUNA GARANZIA DI PROFITTO
⚠️  USA SOLO CAPITALE CHE PUOI PERMETTERTI DI PERDERE

═══════════════════════════════════════════════════════════════════════════════
""")
