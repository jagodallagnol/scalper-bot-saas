"""
SCALPER BOT — Backend Flask Server v2
API per Futures Trading su Bitget (API v2)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json
import hmac
import hashlib
import base64
import threading
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── CONFIGURAZIONE ──────────────────────────────────────────────
BITGET_API_KEY      = os.getenv('BITGET_API_KEY', '')
BITGET_API_SECRET   = os.getenv('BITGET_API_SECRET', '')
BITGET_PASSPHRASE   = os.getenv('BITGET_PASSWORD', '')

SYMBOL          = os.getenv('SYMBOL', 'XRPUSDT')
PRODUCT_TYPE    = 'USDT-FUTURES'

BASE_URL = 'https://api.bitget.com'

HEADERS_PUBLIC = {
    'User-Agent': 'python-requests/2.28.0',
    'Content-Type': 'application/json'
}

# ── STATO GLOBALE ────────────────────────────────────────────────
bot_state = {
    'running': False,
    'symbol': SYMBOL,
    'current_price': 0.0,
    'trades': [],
    'last_update': datetime.now().isoformat()
}

# Cache prezzi (aggiornata dal thread di background)
price_cache = {
    'price': 0.0,
    'high24h': 0.0,
    'low24h': 0.0,
    'change24h': 0.0,
    'volume24h': 0.0,
    'bid': 0.0,
    'ask': 0.0,
    'timestamp': None
}
price_lock = threading.Lock()

# ── FIRMA BITGET ─────────────────────────────────────────────────
def _sign(timestamp: str, method: str, path: str, body: str = '') -> str:
    message = timestamp + method.upper() + path + body
    mac = hmac.new(
        BITGET_API_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    )
    return base64.b64encode(mac.digest()).decode()

def auth_headers(method: str, path: str, body: str = '') -> dict:
    ts = str(int(datetime.now().timestamp() * 1000))
    return {
        'User-Agent': 'python-requests/2.28.0',
        'Content-Type': 'application/json',
        'ACCESS-KEY': BITGET_API_KEY,
        'ACCESS-SIGN': _sign(ts, method, path, body),
        'ACCESS-TIMESTAMP': ts,
        'ACCESS-PASSPHRASE': BITGET_PASSPHRASE,
        'locale': 'it-IT'
    }

# ── FETCH TICKER (PUBLIC) ────────────────────────────────────────
def fetch_ticker(symbol: str = SYMBOL) -> dict | None:
    path = f'/api/v2/mix/market/ticker?productType={PRODUCT_TYPE}&symbol={symbol}'
    try:
        r = requests.get(BASE_URL + path, headers=HEADERS_PUBLIC, timeout=6)
        if r.status_code == 200:
            d = r.json()
            if d.get('code') == '00000' and d.get('data'):
                t = d['data'][0]
                last = float(t.get('lastPr', 0))
                open_ = float(t.get('openUtc', last) or last)
                chg = ((last - open_) / open_ * 100) if open_ else 0.0
                return {
                    'price':     last,
                    'high24h':   float(t.get('high24h', 0)),
                    'low24h':    float(t.get('low24h', 0)),
                    'change24h': chg,
                    'volume24h': float(t.get('baseVolume', 0)),
                    'bid':       float(t.get('bidPr', 0)),
                    'ask':       float(t.get('askPr', 0)),
                    'timestamp': datetime.now().isoformat()
                }
    except Exception as e:
        print(f'[Ticker] Errore: {e}')
    return None

# ── FETCH CANDELE (PUBLIC) ───────────────────────────────────────
def fetch_candles(symbol: str = SYMBOL, granularity: str = '1m', limit: int = 60) -> list:
    path = f'/api/v2/mix/market/candles?productType={PRODUCT_TYPE}&symbol={symbol}&granularity={granularity}&limit={limit}'
    try:
        r = requests.get(BASE_URL + path, headers=HEADERS_PUBLIC, timeout=6)
        if r.status_code == 200:
            d = r.json()
            if d.get('code') == '00000':
                return d.get('data', [])
    except Exception as e:
        print(f'[Candles] Errore: {e}')
    return []

# ── CALCOLO INDICATORI ────────────────────────────────────────────
def calc_indicators(candles: list) -> dict:
    if len(candles) < 20:
        return {}
    # Bitget v2: [ts, open, high, low, close, vol, quoteVol]
    closes = [float(c[4]) for c in candles]
    ema5  = sum(closes[-5:]) / 5
    ema20 = sum(closes[-20:]) / 20
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains  = sum(d for d in deltas if d > 0) or 0.001
    losses = sum(-d for d in deltas if d < 0) or 0.001
    rsi    = 100 - (100 / (1 + gains / losses))
    signal = 'ACQUISTA' if ema5 > ema20 and rsi < 65 else ('VENDI' if ema5 < ema20 and rsi > 35 else 'ATTENDI')
    return {
        'ema5':   round(ema5, 4),
        'ema20':  round(ema20, 4),
        'rsi':    round(rsi, 2),
        'signal': signal
    }

# ── AUTO TRADER (STRATEGIA 5m SUPER HIGH RISK) ───────────────────
def auto_trader():
    print('[AutoTrader] Thread scalping 5m (High Risk) avviato')
    time.sleep(10) # attesa iniziale
    while True:
        if bot_state.get('running', False):
            try:
                # Scalping su TF 5m
                candles = fetch_candles(bot_state['symbol'], granularity='5m', limit=30)
                if len(candles) >= 30:
                    closes = [float(c[4]) for c in candles]
                    current_price = closes[-1]
                    
                    # EMA 9 e 21
                    ema9 = sum(closes[-9:]) / 9
                    ema21 = sum(closes[-21:]) / 21
                    
                    # RSI 14
                    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
                    gains  = sum(d for d in deltas[-14:] if d > 0) or 0.001
                    losses = sum(-d for d in deltas[-14:] if d < 0) or 0.001
                    rsi    = 100 - (100 / (1 + gains / losses))
                    
                    side = None
                    # Super High Risk: crossover veloce + extreme RSI per rimbalzo
                    if rsi < 25 and current_price > ema9:
                        side = 'BUY'
                    elif rsi > 75 and current_price < ema9:
                        side = 'SELL'
                    
                    if side:
                        size_usdt = 50.0  # Fissato a 50 USDT per i trade automatici ad alto rischio
                        print(f"[{datetime.now().time()}] Scalping Signal! {side} {size_usdt} USDT su {bot_state['symbol']}")
                        
                        if BITGET_API_KEY:
                            path = '/api/v2/mix/order/place-order'
                            raw_side = 'buy' if side == 'BUY' else 'sell'
                            size_coin = round(size_usdt / bot_state['current_price'], 4)
                            body = json.dumps({
                                'symbol':     bot_state['symbol'],
                                'productType': PRODUCT_TYPE,
                                'marginMode': 'crossed',
                                'marginCoin': 'USDT',
                                'size':       str(size_coin),
                                'side':       raw_side,
                                'orderType':  'market'
                            })
                            r = requests.post(BASE_URL + path, headers=auth_headers('POST', path, body), data=body, timeout=8)
                            resp = r.json()
                            if resp.get('code') == '00000':
                                ordine = {
                                    'side': side, 'quantity': size_usdt, 'price': bot_state['current_price'],
                                    'timestamp': datetime.now().isoformat(), 'status': 'eseguito auto', 'modalita': 'live'
                                }
                                bot_state['trades'].append(ordine)
                                print(f"[AutoTrader] Eseguito: {resp}")
                            else:
                                print(f"[AutoTrader] Errore: {resp}")
                        else:
                            # Demo log
                            bot_state['trades'].append({
                                'side': side, 'quantity': size_usdt, 'price': bot_state['current_price'],
                                'timestamp': datetime.now().isoformat(), 'status': 'simulato auto', 'modalita': 'demo'
                            })
            except Exception as e:
                print(f"[AutoTrader] Eccezione: {e}")
                
        # Pausa 5 minuti (300 secondi)
        time.sleep(300)

# ── THREAD AGGIORNAMENTO PREZZI ──────────────────────────────────
def price_updater():
    print('[PriceUpdater] Thread avviato')
    while True:
        data = fetch_ticker(bot_state['symbol'])
        if data:
            with price_lock:
                price_cache.update(data)
                bot_state['current_price'] = data['price']
        time.sleep(3)

# ── ROUTE: HOME ──────────────────────────────────────────────────
@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

# ── ROUTE: STATO ─────────────────────────────────────────────────
@app.route('/api/status', methods=['GET'])
def get_status():
    with price_lock:
        prezzo = price_cache['price']
    return jsonify({
        'running':       bot_state['running'],
        'status':        'ATTIVO' if bot_state['running'] else 'OFFLINE',
        'symbol':        bot_state['symbol'],
        'current_price': prezzo,
        'timestamp':     datetime.now().isoformat()
    })

# ── ROUTE: PREZZO ────────────────────────────────────────────────
@app.route('/api/price', methods=['GET'])
def get_price():
    with price_lock:
        data = dict(price_cache)
    if data.get('price', 0) == 0:
        # Prima chiamata: fetch diretto
        fresh = fetch_ticker(bot_state['symbol'])
        if fresh:
            with price_lock:
                price_cache.update(fresh)
                bot_state['current_price'] = fresh['price']
            data = fresh
        else:
            return jsonify({'errore': 'Impossibile ottenere il prezzo'}), 503
    return jsonify({
        'symbol':    bot_state['symbol'],
        **data
    })

# ── ROUTE: DATI DI MERCATO (indicatori) ──────────────────────────
@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    with price_lock:
        ticker = dict(price_cache)
    candles    = fetch_candles(bot_state['symbol'])
    indicators = calc_indicators(candles)
    return jsonify({
        'ticker':         ticker,
        'indicators':     indicators,
        'candles_count':  len(candles),
        'timestamp':      datetime.now().isoformat()
    })

# ── ROUTE: SALDO ─────────────────────────────────────────────────
@app.route('/api/balance', methods=['GET'])
def get_balance():
    if not BITGET_API_KEY:
        return jsonify({
            'totale':       1000.0,
            'disponibile':  1000.0,
            'in_posizione': 0.0,
            'modalita':     'demo',
            'timestamp':    datetime.now().isoformat()
        })
    path = '/api/v2/mix/account/accounts?productType=USDT-FUTURES'
    try:
        r = requests.get(BASE_URL + path, headers=auth_headers('GET', path), timeout=6)
        if r.status_code == 200:
            d = r.json()
            if d.get('code') == '00000' and d.get('data'):
                acc = d['data'][0] if d['data'] else {}
                totale = float(acc.get('usdtEquity', 0))
                disp   = float(acc.get('available', 0))
                return jsonify({
                    'totale':       totale,
                    'disponibile':  disp,
                    'in_posizione': totale - disp,
                    'modalita':     'live',
                    'timestamp':    datetime.now().isoformat()
                })
    except Exception as e:
        print(f'[Balance] Errore: {e}')
    return jsonify({'errore': 'Impossibile ottenere il saldo'}), 503

# ── ROUTE: POSIZIONI APERTE ──────────────────────────────────────
@app.route('/api/posizioni', methods=['GET'])
@app.route('/api/positions', methods=['GET'])
def get_positions():
    if not BITGET_API_KEY:
        return jsonify({'posizioni': [], 'modalita': 'demo'})
    path = f'/api/v2/mix/position/all-position?productType=USDT-FUTURES&marginCoin=USDT'
    try:
        r = requests.get(BASE_URL + path, headers=auth_headers('GET', path), timeout=6)
        if r.status_code == 200:
            d = r.json()
            poss = []
            for p in d.get('data', []):
                qty = float(p.get('total', 0))
                if qty > 0:
                    entry = float(p.get('openPriceAvg', 0))
                    with price_lock:
                        curr = price_cache.get('price', entry)
                    pnl = (curr - entry) * qty if p.get('holdSide') == 'long' else (entry - curr) * qty
                    poss.append({
                        'simbolo':      p.get('symbol', ''),
                        'direzione':    p.get('holdSide', '').upper(),
                        'quantita':     qty,
                        'prezzo_entrata': entry,
                        'prezzo_attuale': curr,
                        'pnl':          round(pnl, 2),
                        'leva':         p.get('leverage', 1)
                    })
            return jsonify({'posizioni': poss, 'modalita': 'live'})
    except Exception as e:
        print(f'[Posizioni] Errore: {e}')
    return jsonify({'errore': 'Impossibile ottenere le posizioni'}), 503

# ── ROUTE: STORICO TRADES ────────────────────────────────────────
@app.route('/api/trades', methods=['GET'])
def get_trades():
    return jsonify({
        'trades':  bot_state['trades'],
        'totale':  len(bot_state['trades']),
        'modalita':'demo' if not BITGET_API_KEY else 'live',
        'timestamp': datetime.now().isoformat()
    })

# ── ROUTE: ESEGUI TRADE (manuale) ────────────────────────────────
@app.route('/api/trade', methods=['POST'])
def execute_trade():
    data   = request.get_json() or {}
    side   = data.get('side', 'BUY').upper()
    amount_usdt = float(data.get('quantity', 0))
    if amount_usdt <= 0:
        return jsonify({'errore': 'Importo non valido'}), 400

    # Ordine reale Bitget
    if BITGET_API_KEY:
        path = '/api/v2/mix/order/place-order'
        raw_side = 'buy' if side == 'BUY' else 'sell'
        base_price = bot_state.get('current_price') or 1.0
        # Convertiamo USDT in crypto. Ritocchiamo a 4 decimali, tipico per gran parte di altcoin, BTC supporta 3-4 dec.
        size_coin = round(amount_usdt / base_price, 4) if base_price > 0 else amount_usdt
        body = json.dumps({
            'symbol':     bot_state['symbol'],
            'productType': PRODUCT_TYPE,
            'marginMode': 'crossed',
            'marginCoin': 'USDT',
            'size':       str(size_coin),
            'side':       raw_side,
            'orderType':  'market'
        })
        try:
            r = requests.post(BASE_URL + path, headers=auth_headers('POST', path, body), data=body, timeout=8)
            resp = r.json()
            if resp.get('code') == '00000':
                ordine = {
                    'side':      side,
                    'quantity':  amount_usdt,
                    'price':     bot_state['current_price'],
                    'timestamp': datetime.now().isoformat(),
                    'status':    'eseguito',
                    'modalita':  'live',
                    'orderId':   resp.get('data', {}).get('orderId', '')
                }
                bot_state['trades'].append(ordine)
                return jsonify({'successo': True, 'trade': ordine})
            return jsonify({'errore': resp.get('msg', 'Errore ordine')}), 500
        except Exception as e:
            return jsonify({'errore': str(e)}), 500

    # Simulazione (demo)
    with price_lock:
        prezzo = price_cache.get('price', 0)
    ordine = {
        'side':      side,
        'quantity':  amount_usdt,
        'price':     prezzo,
        'timestamp': datetime.now().isoformat(),
        'status':    'simulato',
        'modalita':  'demo'
    }
    bot_state['trades'].append(ordine)
    return jsonify({'successo': True, 'trade': ordine, 'modalita': 'demo'})

# ── ROUTE: BOT START/STOP ────────────────────────────────────────
@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    bot_state['running'] = True
    print('[Bot] Avviato')
    return jsonify({'successo': True, 'status': 'ATTIVO'})

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    bot_state['running'] = False
    print('[Bot] Fermato')
    return jsonify({'successo': True, 'status': 'FERMATO'})

@app.route('/api/bot/status', methods=['GET'])
def bot_status():
    return jsonify({
        'running':      bot_state['running'],
        'symbol':       bot_state['symbol'],
        'trades_totali': len(bot_state['trades']),
        'timestamp':    datetime.now().isoformat()
    })

# ── ROUTE: ASTROLOGIA ───────────────────────────────────────────
import math

PIANETI = ['☉', '☽', '☿', '♀', '♂', '♃', '♄']
NOMI_PIANETI = ['Sole', 'Luna', 'Mercurio', 'Venere', 'Marte', 'Giove', 'Saturno']
VELOCITA = [1.0, 13.2, 4.09, 1.6, 0.52, 0.083, 0.034]  # gradi/giorno

SEGNI = [
    'Ariete ♈', 'Toro ♉', 'Gemelli ♊', 'Cancro ♋',
    'Leone ♌', 'Vergine ♍', 'Bilancia ♎', 'Scorpione ♏',
    'Sagittario ♐', 'Capricorno ♑', 'Aquario ♒', 'Pesci ♓'
]

# Longitudine eclittica approssimata (J2000 = 1 Jan 2000)
J2000_OFFSETS = [280.46, 218.32, 252.25, 181.98, 355.45, 34.40, 50.08]

def calc_pianeti(dt: datetime) -> list:
    # Giorni dal 1 Jan 2000 (J2000)
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    giorni = (dt - j2000).total_seconds() / 86400
    pianeti = []
    for i, nome in enumerate(NOMI_PIANETI):
        lon = (J2000_OFFSETS[i] + VELOCITA[i] * giorni) % 360
        segno_idx = int(lon / 30)
        gradi = lon % 30
        pianeti.append({
            'simbolo':  PIANETI[i],
            'nome':     nome,
            'longitudine': round(lon, 2),
            'segno':    SEGNI[segno_idx],
            'gradi':    round(gradi, 1)
        })
    return pianeti

def calc_aspetti(pianeti: list) -> list:
    aspetti = []
    nomi_aspetti = {0:'Congiunzione', 60:'Sestile', 90:'Quadratura',
                    120:'Trigono', 150:'Quinconce', 180:'Opposizione'}
    colori = {0:'#ccff00', 60:'#00ff88', 90:'#ff3333',
              120:'#00ff88', 150:'#888', 180:'#ff3333'}
    orbs = 8  # gradi di orb
    lons = [p['longitudine'] for p in pianeti]
    for i in range(len(lons)):
        for j in range(i + 1, len(lons)):
            ang = abs(lons[i] - lons[j]) % 360
            if ang > 180: ang = 360 - ang
            for angolo_target, nome in nomi_aspetti.items():
                if abs(ang - angolo_target) <= orbs:
                    aspetti.append({
                        'p1':     pianeti[i]['nome'],
                        'p2':     pianeti[j]['nome'],
                        'tipo':   nome,
                        'angolo': round(ang, 1),
                        'colore': colori.get(angolo_target, '#888')
                    })
    return aspetti

def calc_sentiment_astro(aspetti: list, luna_lon: float) -> dict:
    score = 0.0
    pesi = {'Trigono': 2, 'Sestile': 1, 'Congiunzione': 0.5,
            'Quadratura': -2, 'Opposizione': -2, 'Quinconce': -0.5}
    for a in aspetti:
        score += pesi.get(a['tipo'], 0)

    # Luna in segni bullish (Ariete, Leone, Sagittario = fuoco)
    segno_luna = int(luna_lon / 30)
    fuoco = segno_luna in [0, 4, 8]
    terra  = segno_luna in [1, 5, 9]
    if fuoco: score += 1.5
    if terra:  score -= 0.5

    # Normalizza
    max_score = 10
    norm = max(-1, min(1, score / max_score))
    if norm > 0.2:
        sentiment = 'RIALZISTA 🟢'
        colore = '#00ff88'
    elif norm < -0.2:
        sentiment = 'RIBASSISTA 🔴'
        colore = '#ff3333'
    else:
        sentiment = 'NEUTRO 🟡'
        colore = '#ccff00'

    return {
        'score':     round(norm, 3),
        'pct':       round((norm + 1) / 2 * 100, 1),
        'sentiment': sentiment,
        'colore':    colore,
        'fase_luna': _fase_luna(luna_lon)
    }

def _fase_luna(luna_lon: float) -> str:
    sole_lon = (J2000_OFFSETS[0] + 1.0 * ((datetime.now() - datetime(2000,1,1,12)).total_seconds()/86400)) % 360
    diff = (luna_lon - sole_lon) % 360
    if diff < 22.5 or diff >= 337.5:   return '🌑 Luna Nuova'
    elif diff < 67.5:                   return '🌒 Luna Crescente'
    elif diff < 112.5:                  return '🌓 Primo Quarto'
    elif diff < 157.5:                  return '🌔 Gibbosa Cres.'
    elif diff < 202.5:                  return '🌕 Luna Piena'
    elif diff < 247.5:                  return '🌖 Gibbosa Cal.'
    elif diff < 292.5:                  return '🌗 Ultimo Quarto'
    else:                               return '🌘 Luna Calante'

@app.route('/api/astro', methods=['GET'])
def get_astro():
    """Dati astrologici: posizioni pianeti, aspetti, sentiment di mercato"""
    ora = datetime.now()
    pianeti = calc_pianeti(ora)
    aspetti = calc_aspetti(pianeti)
    luna_lon = pianeti[1]['longitudine']
    sentiment = calc_sentiment_astro(aspetti, luna_lon)

    return jsonify({
        'pianeti':   pianeti,
        'aspetti':   aspetti[:8],  # top 8 aspetti
        'sentiment': sentiment,
        'timestamp': ora.isoformat()
    })

# ── ROUTE: CAMBIO SIMBOLO ────────────────────────────────────────
@app.route('/api/symbol', methods=['POST'])
def change_symbol():
    data   = request.get_json() or {}
    symbol = data.get('symbol', '').upper().strip()
    if not symbol:
        return jsonify({'errore': 'Simbolo non valido'}), 400
    # Verifica che esista su Bitget
    test = fetch_ticker(symbol)
    if not test:
        return jsonify({'errore': f'Simbolo {symbol} non trovato su Bitget'}), 404
    bot_state['symbol'] = symbol
    with price_lock:
        price_cache.update(test)
    return jsonify({'successo': True, 'symbol': symbol, 'prezzo': test['price']})

# ── ROUTE: SALVATAGGIO IMPOSTAZIONI ─────────────────────────────
@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.get_json() or {}
    # Per ora solo acknowledge — in futuro potrebbe aggiornare .env
    return jsonify({'successo': True, 'messaggio': 'Impostazioni ricevute'})

# ── MAIN ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8889))

    print(f"""
╔══════════════════════════════════════════════════════╗
║         SCALPER BOT — SERVER BACKEND v2              ║
║  🚀 http://localhost:{port}                              ║
║  📡 Exchange: Bitget Futures (USDT-FUTURES)           ║
║  💱 Simbolo:  {bot_state['symbol']:<10}                      ║
║  🔑 API Key:  {'✅ Configurata' if BITGET_API_KEY else '❌ Non configurata (demo)'}            ║
╚══════════════════════════════════════════════════════╝
""")

    # Thread aggiornamento prezzi
    t = threading.Thread(target=price_updater, daemon=True)
    t.start()
    
    # Thread Auto Trader (5m Scalping)
    t_auto = threading.Thread(target=auto_trader, daemon=True)
    t_auto.start()

    app.run(debug=False, host='0.0.0.0', port=port)
