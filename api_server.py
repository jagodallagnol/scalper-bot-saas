"""
SCALPER BOT · BACKEND API SERVER (MULTI-USER SAAS)
Flask server for real-time Binance/Bitget API integration, supporting multiple concurrent users.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
from advanced_scalper_strategy import AdvancedScalperStrategy
from data_manager import DataManager
import ccxt
import threading
import json
from datetime import datetime, timedelta
import time

load_dotenv()

app = Flask(__name__)
# Enable CORS for all origins so Netlify can connect to this backend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global shared instances (Stateless)
global_strategy = None
global_data_manager = DataManager()

# Session memory store
# Format: { 'session_id': { 'exchange': ccxt_instance, 'bot_running': bool, 'bot_thread': Thread, 'portfolio_data': dict, 'last_active': datetime } }
sessions = {}

def init_global_strategy():
    """Initialize advanced strategy once for all users"""
    global global_strategy
    try:
        if not global_strategy:
            global_strategy = AdvancedScalperStrategy()
        return True
    except Exception as e:
        print(f"Errore nell'inizializzazione strategia: {e}")
        return False

def cleanup_inactive_sessions():
    """Background thread to remove inactive sessions and stop their bots to free memory"""
    while True:
        try:
            now = datetime.now()
            to_remove = []
            for session_id, session in sessions.items():
                # If inactive for > 1 hour
                if now - session['last_active'] > timedelta(hours=1):
                    to_remove.append(session_id)
            
            for session_id in to_remove:
                print(f"[CLEANUP] Removing inactive session: {session_id}")
                session = sessions[session_id]
                session['bot_running'] = False # Stop thread
                del sessions[session_id]
                
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(600) # Check every 10 minutes

threading.Thread(target=cleanup_inactive_sessions, daemon=True).start()

def get_session():
    """Retrieves or creates a user session based on the X-Session-ID header"""
    session_id = request.headers.get('X-Session-ID')
    
    if not session_id:
        return None, jsonify({'error': 'Missing X-Session-ID header. Required for multi-user support.'}), 401
        
    if session_id not in sessions:
        sessions[session_id] = {
            'exchange': None,
            'bot_running': False,
            'bot_thread': None,
            'portfolio_data': {
                'totalBalance': 0,
                'availableBalance': 0,
                'positionBalance': 0,
                'trades': [],
                'positions': []
            },
            'last_active': datetime.now()
        }
    
    sessions[session_id]['last_active'] = datetime.now()
    return sessions[session_id], None, None

def init_exchange(session, api_key, api_secret, password):
    """Initialize Bitget exchange connection for a specific session"""
    if not api_key or not api_secret or not password:
        return False
    
    try:
        session['exchange'] = ccxt.bitget({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap'
            }
        })
        return True
    except Exception as e:
        print(f"Errore nell'inizializzazione exchange per utente: {e}")
        return False

# ═══════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════

@app.route('/', methods=['GET'])
def index():
    return """
    <html>
        <body style="background-color: #050505; color: #00ff00; font-family: monospace; padding: 50px; text-align: center;">
            <h1 style="color: #00ff00;">◬ ANTIGRAVITY SCALPER API</h1>
            <p>Il Motore Python è ONLINE e operativo 24/7.</p>
            <p>Status: <span style="color: #00ff00;">Running</span></p>
            <p style="color: #888; font-size: 12px; margin-top: 50px;">Apri l'App Netlify dal tuo telefono per controllare il bot.</p>
        </body>
    </html>
    """

@app.route('/api/status', methods=['GET'])
def get_status():
    """Check API server status and user's bot status"""
    session, err_resp, code = get_session()
    if err_resp: return err_resp, code
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'exchange_connected': session['exchange'] is not None,
        'bot_running': session['bot_running']
    })

@app.route('/api/price', methods=['GET'])
def get_price():
    """Get current price. Public endpoint, doesn't require API key."""
    try:
        session, err_resp, code = get_session()
        if err_resp: return err_resp, code
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        # Use user exchange if available, otherwise just use a generic unauthenticated one
        ex = session['exchange'] if session['exchange'] else ccxt.bitget()
        
        # Fetch ticker
        ticker = ex.fetch_ticker(symbol)
        
        # Fetch 24h stats
        ohlcv = ex.fetch_ohlcv(symbol, '1m', limit=1440)
        
        high_24h = max([candle[2] for candle in ohlcv[-1440:]])
        low_24h = min([candle[3] for candle in ohlcv[-1440:]])
        
        open_24h = ohlcv[-1440][1]
        change_24h = ((ticker['last'] - open_24h) / open_24h * 100) if open_24h > 0 else 0
        
        return jsonify({
            'price': ticker['last'],
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'high24h': high_24h,
            'low24h': low_24h,
            'change24h': change_24h,
            'volume': ticker.get('quoteVolume', 0),
            'quoteAssetVolume': ticker.get('quoteVolume', 0) * ticker['last'],
            'timestamp': ticker.get('timestamp')
        })
    except Exception as e:
        print(f"Errore nel fetching del prezzo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio balance and trades info for the session"""
    try:
        session, err_resp, code = get_session()
        if err_resp: return err_resp, code
        
        if not session['exchange']:
            return jsonify(session['portfolio_data'])
        
        # Fetch balance
        balance = session['exchange'].fetch_balance()
        
        total = balance['total'].get('USDT', 0)
        free = balance['free'].get('USDT', 0)
        used = balance['used'].get('USDT', 0)
        
        session['portfolio_data']['totalBalance'] = total
        session['portfolio_data']['availableBalance'] = free
        session['portfolio_data']['positionBalance'] = used
        
        return jsonify(session['portfolio_data'])
    except Exception as e:
        print(f"Errore nel fetching portafoglio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """Get current indicators values"""
    try:
        init_global_strategy()
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        # Fetch historical data (using the global data manager)
        df = global_data_manager.fetch_ohlcv_live(symbol, '1m', limit=500)
        
        if df.empty:
            return jsonify({'error': 'No data'}), 400
        
        # Calculate indicators
        indicators = global_strategy.calculate_all_indicators(df)
        
        return jsonify({
            'indicators': indicators,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Errore nel calcolo degli indicatori: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/signal', methods=['GET'])
def get_signal():
    """Get current trading signal"""
    try:
        init_global_strategy()
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        df = global_data_manager.fetch_ohlcv_live(symbol, '1m', limit=500)
        
        if df.empty:
            return jsonify({'error': 'No data'}), 400
        
        # Get signal
        signal = global_strategy.generate_signals(df)
        
        return jsonify({
            'signal': signal,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Errore nel calcolo del segnale: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/symbol', methods=['POST'])
def set_symbol():
    """Update active trading symbol for the session"""
    session, err_resp, code = get_session()
    if err_resp: return err_resp, code
    
    data = request.json
    symbol = data.get('symbol', 'XRPUSDT').upper()
    
    # We could store it in session if we want to run multiple pairs, 
    # but for now we just return success so the frontend updates internally.
    try:
        # Just verify it's a valid symbol by fetching ticker
        ex = session['exchange'] if session['exchange'] else ccxt.bitget()
        ticker = ex.fetch_ticker(symbol.replace('USDT', '/USDT'))
        return jsonify({'successo': True, 'prezzo': ticker['last']})
    except Exception as e:
        return jsonify({'successo': False, 'errore': 'Coppia non valida o non trovata.'})

@app.route('/api/credentials', methods=['POST'])
def set_credentials():
    """Set Bitget API credentials for the current user's session"""
    try:
        session, err_resp, code = get_session()
        if err_resp: return err_resp, code
        
        data = request.json
        api_key = data.get('apiKey')
        api_secret = data.get('apiSecret')
        password = data.get('password')
        
        # Clear existing bot if running on old keys
        session['bot_running'] = False
        
        if init_exchange(session, api_key, api_secret, password):
            return jsonify({'status': 'success', 'message': 'Credenziali sicure caricate in memoria temporanea sessione'})
        else:
            return jsonify({'status': 'error', 'message': 'Credenziali API non valide'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trade/execute', methods=['POST'])
def execute_trade():
    """Execute a trade for the specific user"""
    try:
        session, err_resp, code = get_session()
        if err_resp: return err_resp, code
        
        if not session['exchange']:
            return jsonify({'status': 'error', 'message': 'API Key non connessa. Inserisci in Impostazioni.'}), 403
        
        data = request.json
        trade_type = data.get('type', 'buy')
        amount = float(data.get('amount', 100))
        stop_loss = float(data.get('stopLoss', 2))
        take_profit = float(data.get('takeProfit', 3))
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        ticker = session['exchange'].fetch_ticker(symbol)
        current_price = ticker['last']
        quantity = amount / current_price
        
        try:
            if trade_type == 'buy':
                order = session['exchange'].create_market_buy_order(symbol, quantity)
            else:
                order = session['exchange'].create_market_sell_order(symbol, quantity)
            
            # Add to user's trades history
            session['portfolio_data']['trades'].append({
                'id': order['id'],
                'symbol': symbol,
                'type': trade_type,
                'amount': amount,
                'price': current_price,
                'timestamp': datetime.now().isoformat(),
                'pnl': 0
            })
            
            return jsonify({
                'status': 'success',
                'message': f'Trade {trade_type} eseguito',
                'orderId': order['id'],
                'price': current_price,
                'quantity': quantity
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the trading bot for the user's session"""
    try:
        session, err_resp, code = get_session()
        if err_resp: return err_resp, code
        
        if session['bot_running']:
            return jsonify({'status': 'already_running', 'message': 'Bot già in esecuzione'})
        
        if not session['exchange']:
            return jsonify({'status': 'error', 'message': 'Manca API Key. Vai nelle impostazioni.'}), 403
        
        init_global_strategy()
        
        session['bot_running'] = True
        session['bot_thread'] = threading.Thread(target=run_bot_loop, args=(session,), daemon=True)
        session['bot_thread'].start()
        
        return jsonify({'status': 'started', 'message': 'Bot Automatico Avviato'})
    except Exception as e:
        if session: session['bot_running'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the trading bot for the user's session"""
    session, err_resp, code = get_session()
    if err_resp: return err_resp, code
    
    session['bot_running'] = False
    return jsonify({'status': 'stopped', 'message': 'Bot Fermato'})

def run_bot_loop(session):
    """Main bot trading loop mapped to exactly one session"""
    check_interval = int(os.getenv('CHECK_INTERVAL', 5))
    min_amount = float(os.getenv('MIN_AMOUNT', 100))
    
    while session.get('bot_running', False):
        try:
            symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
            
            df = global_data_manager.fetch_ohlcv_live(symbol, '1m', limit=500)
            
            if df.empty:
                time.sleep(check_interval)
                continue
            
            signal = global_strategy.generate_signals(df)
            
            if signal['signal'] in ['LONG', 'SHORT']:
                ticker = session['exchange'].fetch_ticker(symbol)
                current_price = ticker['last']
                quantity = min_amount / current_price
                
                trade_type = 'buy' if signal['signal'] == 'LONG' else 'sell'
                
                try:
                    if trade_type == 'buy':
                        order = session['exchange'].create_market_buy_order(symbol, quantity)
                    else:
                        order = session['exchange'].create_market_sell_order(symbol, quantity)
                    
                    print(f"[SessionBot] Trade {trade_type} eseguito: {quantity} @ ${current_price}")
                except Exception as ex:
                    print(f"[SessionBot] Errore esecuzione ordine: {ex}")
            
            time.sleep(check_interval)
        except Exception as e:
            print(f"Errore nel bot loop di questa sessione: {e}")
            time.sleep(check_interval)

# ═══════════════════════════════════
# SERVER STARTUP
# ═══════════════════════════════════

if __name__ == '__main__':
    init_global_strategy()
    
    print("=" * 50)
    print("SCALPER BOT · SAAS MULTI-USER API SERVER")
    print("=" * 50)
    print("Server pronto per ricevere connessioni Web!")
    print("=" * 50)
    
    # Listen on all interfaces (0.0.0.0) so Render/Platform can port map
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
