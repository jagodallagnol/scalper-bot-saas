#!/usr/bin/env python3
"""
SCALPER BOT · QUICK START
Guida rapida all'uso dell'interfaccia web
"""

def print_guide():
    guide = """
╔════════════════════════════════════════════════════════════════╗
║           🚀 SCALPER BOT · WEB UI QUICK START                  ║
╚════════════════════════════════════════════════════════════════╝

📖 INDICE
═══════════════════════════════════════════════════════════════

1️⃣  INSTALLAZIONE
2️⃣  PRIMO AVVIO
3️⃣  CONFIGURAZIONE BINANCE
4️⃣  USO DELL'INTERFACCIA
5️⃣  STRATEGIE DI TRADING
6️⃣  TROUBLESHOOTING


═══════════════════════════════════════════════════════════════

1️⃣  INSTALLAZIONE

Passaggio 1: Installa le dipendenze
──────────────────────────────────
$ cd /Users/jagodallagnol/Desktop/projects/scalper
$ pip install -r requirements.txt

Questa operazione installa:
  ✅ Flask (server web)
  ✅ ccxt (API Binance)
  ✅ pandas (analisi dati)
  ✅ ta (indicatori tecnici)
  ✅ requests (HTTP client)


═══════════════════════════════════════════════════════════════

2️⃣  PRIMO AVVIO

OPZIONE A: Script Automatico (Consigliato)
──────────────────────────────────────────
$ python start_bot.py

Questo avvia automaticamente:
  • Backend API (Flask) su localhost:5000
  • Server Web su localhost:8080
  • Apre il browser

OPZIONE B: Terminali Separati (Manuale)
────────────────────────────────────────

Terminal 1 - Backend:
  $ python api_server.py
  
Terminal 2 - Frontend:
  $ python -m http.server 8080

Terminal 3 - Apri Browser:
  $ open http://localhost:8080


═══════════════════════════════════════════════════════════════

3️⃣  CONFIGURAZIONE BINANCE

Step 1: Vai a Settings (Impostazioni)
─────────────────────────────────────
  1. Clicca il tab ⚙️ IMPOSTAZIONI in basso
  2. Scorri fino a CONFIGURAZIONE


Step 2: Inserisci Credenziali Binance
──────────────────────────────────────
  1. Accedi a Binance.com
  2. Vai su API Management
  3. Crea una nuova API Key:
     
     ✅ Spot Trading ON
     ✅ Futures Trading ON
     ✅ Read Permissions
     ❌ Withdraw = OFF (disabilitato)

  4. Copia la API Key
  5. Copia la API Secret
  6. Incolla nel web UI nel tab Settings


Step 3: Salva i Parametri
─────────────────────────
  Nella sezione "PARAMETRI SCALPER":
  
  QUANTITÀ MINIMA (USDT): 100
  GUADAGNO TARGET (%): 2.0
  INTERVALLO CONTROLLO (sec): 5

  Clicca: SALVA PARAMETRI


═══════════════════════════════════════════════════════════════

4️⃣  USO DELL'INTERFACCIA

DASHBOARD (📊)
──────────────
  Visualizza:
  • Prezzo attuale XRP/USDT
  • Variazione 24h (%)
  • Saldo totale portafoglio
  • Performance trading (Win Rate %)
  • P&L totale ($)

  Aggiornamento: Ogni 1 secondo


TRADE (💹)
─────────
  Esecuzione manuale:
  
  1. Seleziona ACQUISTA o VENDI
  2. Inserisci importo USDT (es: 100)
  3. Imposta Stop Loss % (es: 2%)
  4. Imposta Take Profit % (es: 3%)
  5. Clicca ACQUISTA o VENDI
  
  Bot Automatico:
  
  1. Vai su STRATEGIE
  2. Seleziona strategia (SCALPING)
  3. Clicca AVVIA BOT
  4. Il bot eseguirà trade automatici
  5. Clicca FERMA BOT per interrompere


POSIZIONI (📈)
──────────────
  Vedi:
  • Posizioni aperte attuali
  • Entry price
  • P&L corrente
  • Storico completo trade
  • Timestamp di ogni operazione


IMPOSTAZIONI (⚙️)
─────────────────
  Configura:
  • Credenziali Binance
  • Parametri strategie
  • Limite ordini minimo
  • Intervallo controllo bot


═══════════════════════════════════════════════════════════════

5️⃣  STRATEGIE DI TRADING

STRATEGIA AVANZATA (19 INDICATORI)
─────────────────────────────────

Indicatori Utilizzati:
  
  Trend (6):
    • EMA 5, 13, 50
    • SMA 50
    • ADX
    • SAR (Parabolic)
  
  Momentum (6):
    • RSI
    • MACD
    • KDJ Stochastic
    • TRIX
    • ROC
    • TSI
  
  Volatilità (3):
    • Bollinger Bands
    • ATR
    • Historical Vol
  
  Volume (3):
    • OBV
    • ADL
    • Volume Ratio
  
  Support/Resist (2):
    • Pivot Points
    • Fibonacci


SEGNALI DI TRADING
──────────────────

Score Sistema:
  -1.0 ————————————————— 0 ————————————— +1.0
  
  Score < -0.35  →  VENDI (SHORT)
  Score > +0.35  →  ACQUISTA (LONG)
  Tra questi     →  NO SEGNALE


TAKE PROFIT & STOP LOSS
───────────────────────

Dinamico (Calcolato Automaticamente):
  
  Take Profit = Entry Price + (2.5 × ATR)
                O
                Fibonacci Extension (se migliore)
  
  Stop Loss = Entry Price - (1 × ATR)
              O
              Pivot Support (se più vicino)


SCALPING (Tempo Reale)
──────────────────────

Caratteristiche:
  ✅ Timeframe: 1 minuto
  ✅ Holding: 1-30 minuti
  ✅ Target: 0.5% - 2% per trade
  ✅ Frequenza: Molti piccoli trade
  ✅ Rischio: 1-2% per posizione


═══════════════════════════════════════════════════════════════

6️⃣  TROUBLESHOOTING

PROBLEMA: "Backend API not connected"
─────────────────────────────────────

Soluzione 1: Verifica porta 5000
  $ lsof -i :5000
  
  Se in uso, cambia porta in api_server.py

Soluzione 2: Riavvia il server
  1. Premi CTRL+C nel terminal del backend
  2. $ python api_server.py

Soluzione 3: Installa Flask
  $ pip install Flask Flask-CORS


PROBLEMA: "Exchange connected: False"
────────────────────────────────────

Cause:
  ❌ API Key non valida
  ❌ API Secret non valida
  ❌ Permessi insufficienti
  ❌ API disabilitata su Binance

Soluzione:
  1. Accedi a Binance.com
  2. Vai a API Management
  3. Verifica la chiave sia attiva
  4. Crea una nuova chiave se necessario
  5. Assicurati siano abilitate le operazioni:
     • Spot Trading
     • Futures Trading
     • Read Permissions


PROBLEMA: "No trades are executing"
──────────────────────────────────

Verifica:
  1. ✅ Credenziali Binance corrette?
  2. ✅ Saldo disponibile > 100 USDT?
  3. ✅ Bot è in stato RUNNING?
  4. ✅ Console web (F12) mostra errori?

Azioni:
  1. Vai su Dashboard - vedi il saldo?
  2. Se sì: bot è connesso
  3. Se no: riconfigura credenziali
  4. Prova trade manuale per verificare


PROBLEMA: "Prezzo non si aggiorna"
─────────────────────────────────

Verifica:
  1. Sei online? (Check icon in alto)
  2. Server API è in esecuzione?
  3. Console browser (F12) mostra errori di rete?

Soluzione:
  1. Aggiorna pagina (F5 o CMD+R)
  2. Riavvia api_server.py
  3. Ricollega il portafoglio


PROBLEMA: Browser non si apre automaticamente
──────────────────────────────────────────────

Soluzione Manuale:
  Apri il browser e vai a:
  
  http://localhost:8080


═══════════════════════════════════════════════════════════════

📊 MONITORAGGIO BOT IN AZIONE

Cosa controllare:
  
  1. Dashboard → Prezzo aggiornato ogni secondo
  2. Status → "ONLINE" in verde
  3. Performance → Win rate e P&L aggiornati
  4. Posizioni → Nuovi trade compaiono in tempo reale
  5. Storico → Tutti i trade registrati


Performance Metriche:
  
  ✅ Win Rate > 55% = Buono
  ✅ Sharpe Ratio > 1.0 = Accettabile
  ✅ Max Drawdown < 20% = Prudente
  ✅ Profit Factor > 1.5 = Solido


═══════════════════════════════════════════════════════════════

💡 CONSIGLI PROFESSIONALI

1. INIZIO CAUTELA
   ─────────────
   Inizia con importi piccoli (100-500 USDT)
   Prima di aumentare l'esposizione

2. MONITORA REGOLARMENTE
   ────────────────────
   Non attivare e dimenticare!
   Controlla almeno 2-3 volte al giorno

3. ADATTA I PARAMETRI
   ──────────────────
   Se win rate < 50%:
     → Aumenta take profit %
     → Riduci stop loss %
   
   Se drawdown troppo alto:
     → Riduci importo minimo
     → Aumenta stop loss %

4. DIVERSIFICA
   ──────────
   Non mettere tutto in un'unica coppia
   Prova diverse strategie

5. MANTIENI BACKUP
   ───────────────
   Salva i log di trading
   Documenta i parametri vincenti


═══════════════════════════════════════════════════════════════

🎯 PROSSIMI PASSI

1. Installa dipendenze
2. Avvia il bot con python start_bot.py
3. Aggiungi credenziali Binance
4. Imposta parametri di scalping
5. Fai un test trade manuale
6. Avvia il bot automatico
7. Monitora il primo giorno
8. Ottimizza i parametri


═══════════════════════════════════════════════════════════════

📞 SUPPORTO

Se hai problemi:

1. Controlla i log:
   $ tail -f api_server.log

2. Apri console browser (F12):
   → Guarda la tab "Console"
   → Cerca messaggi di errore rossi

3. Verifica .env file:
   $ cat .env

4. Prova riavvio completo:
   Ctrl+C su tutti i terminali
   Riavvia con: python start_bot.py


═══════════════════════════════════════════════════════════════

Made with ❤️  for Crypto Scalpers

Buon trading! 🚀📈

═══════════════════════════════════════════════════════════════
"""
    print(guide)

if __name__ == '__main__':
    print_guide()
