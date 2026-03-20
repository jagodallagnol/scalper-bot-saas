# 🔄 Guida Setup Exchange - Binance & Bitget

## Stato Attuale

### ✅ Binance
- **API Pubblica**: Completamente funzionante
- **Dati Disponibili**: Prezzo, Volume, Indicatori tecnici
- **Trading Demo**: Sì (simulato)
- **Credenziali Richieste**: No (opzionali per trading reale)

### ⚠️ Bitget
- **API Pubblica**: Bloccata da Cloudflare (protezione DDoS)
- **Struttura Backend**: Implementata e pronta
- **Credenziali Richieste**: Sì
- **Status**: In preparazione - richiede API key

---

## Come Usare Binance (Default)

Binance funziona out-of-the-box:

```bash
# Il bot usa Binance per default
curl http://localhost:8889/api/exchange/current

# Risposta
{
    "exchange": "binance",
    "symbol": "XRPUSDT",
    "available_exchanges": ["binance", "bitget"]
}
```

### Aggiungere Credenziali Binance (Opzionale)

1. Vai su **Settings** nell'interfaccia web
2. Aggiungi API Key e Secret
3. Clicca **SALVA CREDENZIALI**

---

## Come Aggiungere Bitget

Bitget è già implementato nel backend! Ecco come configurarlo:

### Passo 1: Ottieni Credenziali Bitget
- Vai su https://www.bitget.com
- Accedi al tuo account
- Vai a **Settings → API Management**
- Crea una nuova API key (con permessi di lettura)

### Passo 2: Aggiungi Credenziali nel Bot
1. Nell'app, vai su **Settings**
2. Seleziona **BITGET** dal menu **EXCHANGE**
3. Inserisci la Bitget API Key e Secret
4. Clicca **CAMBIA EXCHANGE**

### Passo 3: Verifica il Cambio
```bash
# Controlla che sia attivo
curl http://localhost:8889/api/exchange/current

# Dovrebbe rispondere:
{
    "exchange": "bitget",
    "symbol": "XRPUSDT"
}
```

---

## Cambio Exchange da Terminale

```bash
# Cambia a Bitget
curl -X POST http://localhost:8889/api/exchange/switch \
  -H "Content-Type: application/json" \
  -d '{"exchange":"bitget"}'

# Cambia a Binance
curl -X POST http://localhost:8889/api/exchange/switch \
  -H "Content-Type: application/json" \
  -d '{"exchange":"binance"}'
```

---

## API Endpoints Disponibili

### Status Exchange
```bash
GET /api/exchange/current
```

### Cambia Exchange
```bash
POST /api/exchange/switch
Body: {"exchange": "binance|bitget"}
```

### Prezzo Attuale
```bash
GET /api/price
# Usa l'exchange attualmente selezionato
```

### Dati di Mercato
```bash
GET /api/market-data
# Restituisce indicatori tecnici (EMA, RSI, Signal)
```

---

## Troubleshooting

### Bitget non risponde
**Causa**: Cloudflare protection
**Soluzione**: 
- Usare credenziali API per accesso autenticato
- O mantenere Binance come default

### Exchange non cambia
**Causa**: Credenziali errate o API non disponibile
**Soluzione**:
- Verifica i log: `tail -f /tmp/server.log`
- Controlla che l'exchange sia disponibile

### Prezzo non si aggiorna
**Causa**: Exchange offline
**Soluzione**:
- Cambia a Binance (sempre disponibile)
- Verifica la connessione internet

---

## Prossimi Step

1. ✅ Binance Public API - FUNZIONANTE
2. ✅ Bitget Backend - PRONTO
3. ⏳ Integrazione Bitget API con autenticazione - IN PROGRESS
4. ⏳ Altri exchange (Kraken, OKX, etc.) - FUTURE

---

## Comandi Veloci

```bash
# Verifica bot status
curl http://localhost:8889/api/status

# Vedi prezzo XRP attuale
curl http://localhost:8889/api/price

# Ottieni saldo (mock se public API)
curl http://localhost:8889/api/balance

# Storico trades
curl http://localhost:8889/api/trades

# Dati tecnici
curl http://localhost:8889/api/market-data
```

---

**Versione**: 1.0.0
**Data Aggiornamento**: 19 Marzo 2026
**Status**: Binance ✅ | Bitget ⏳
