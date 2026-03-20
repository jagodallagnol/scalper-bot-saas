"""
SCALPER BOT · BACKEND API SERVER
Flask server for real-time Binance API integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from advanced_scalper_strategy import AdvancedScalperStrategy
from data_manager import DataManager
import ccxt
import threading
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables
exchange = None
strategy = None
data_manager = DataManager()
bot_running = False
bot_thread = None
portfolio_data = {
    'totalBalance': 1000,
    'availableBalance': 1000,
    'positionBalance': 0,
    'trades': [],
    'positions': []
}

def init_exchange(api_key=None, api_secret=None, password=None):
    """Initialize Bitget exchange connection"""
    global exchange
    
    api_key = api_key or os.getenv('BITGET_API_KEY')
    api_secret = api_secret or os.getenv('BITGET_SECRET_KEY')
    password = password or os.getenv('BITGET_PASSWORD')
    
    if not api_key or not api_secret or not password:
        return False
    
    try:
        exchange = ccxt.bitget({
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
        print(f"Errore nell'inizializzazione exchange: {e}")
        return False

def init_strategy():
    """Initialize advanced strategy"""
    global strategy
    try:
        strategy = AdvancedScalperStrategy()
        return True
    except Exception as e:
        print(f"Errore nell'inizializzazione strategia: {e}")
        return False

# ═══════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════

@app.route('/api/status', methods=['GET'])
def get_status():
    """Check API server status"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'exchange_connected': exchange is not None,
        'bot_running': bot_running
    })

@app.route('/api/price', methods=['GET'])
def get_price():
    """Get current price and market data"""
    try:
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        if not exchange:
            init_exchange()
            if not exchange:
                return jsonify({'error': 'Exchange not connected'}), 503
        
        # Fetch ticker
        ticker = exchange.fetch_ticker(symbol)
        
        # Fetch 24h stats
        ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=1440)
        
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
    """Get portfolio balance and trades info"""
    try:
        if not exchange:
            init_exchange()
            if not exchange:
                return jsonify(portfolio_data)
        
        # Fetch balance
        balance = exchange.fetch_balance()
        
        total = balance['total'].get('USDT', 0)
        free = balance['free'].get('USDT', 0)
        used = balance['used'].get('USDT', 0)
        
        portfolio_data['totalBalance'] = total
        portfolio_data['availableBalance'] = free
        portfolio_data['positionBalance'] = used
        
        return jsonify(portfolio_data)
    except Exception as e:
        print(f"Errore nel fetching portafoglio: {e}")
        return jsonify(portfolio_data)

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """Get current indicators values"""
    try:
        if not strategy:
            init_strategy()
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        # Fetch historical data
        df = data_manager.download_data(symbol, '1m', limit=500)
        
        if df.empty:
            return jsonify({'error': 'No data'}), 400
        
        # Calculate indicators
        indicators = strategy.calculate_all_indicators(df)
        
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
        if not strategy:
            init_strategy()
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        # Fetch historical data
        df = data_manager.download_data(symbol, '1m', limit=500)
        
        if df.empty:
            return jsonify({'error': 'No data'}), 400
        
        # Get signal
        signal = strategy.generate_signals(df)
        
        return jsonify({
            'signal': signal,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Errore nel calcolo del segnale: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/credentials', methods=['POST'])
def set_credentials():
    """Set Bitget API credentials"""
    try:
        data = request.json
        api_key = data.get('apiKey')
        api_secret = data.get('apiSecret')
        password = data.get('password')
        
        if init_exchange(api_key, api_secret, password):
            return jsonify({'status': 'success', 'message': 'Credenziali salvate'})
        else:
            return jsonify({'status': 'error', 'message': 'Credenziali non valide'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trade/execute', methods=['POST'])
def execute_trade():
    """Execute a trade"""
    try:
        if not exchange:
            return jsonify({'status': 'error', 'message': 'Exchange not connected'}), 503
        
        data = request.json
        trade_type = data.get('type', 'buy')  # 'buy' or 'sell'
        amount = float(data.get('amount', 100))
        stop_loss = float(data.get('stopLoss', 2))
        take_profit = float(data.get('takeProfit', 3))
        
        symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
        
        # Get current price
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        
        # Calculate quantity
        quantity = amount / current_price
        
        try:
            if trade_type == 'buy':
                order = exchange.create_market_buy_order(symbol, quantity)
            else:
                order = exchange.create_market_sell_order(symbol, quantity)
            
            # Add to trades history
            portfolio_data['trades'].append({
                'id': order['id'],
                'symbol': symbol,
                'type': trade_type,
                'amount': amount,
                'price': current_price,
                'stopLoss': stop_loss,
                'takeProfit': take_profit,
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
    """Start the trading bot"""
    global bot_running, bot_thread
    
    try:
        if bot_running:
            return jsonify({'status': 'already_running', 'message': 'Bot è già in esecuzione'})
        
        if not exchange:
            init_exchange()
            if not exchange:
                return jsonify({'status': 'error', 'message': 'Impossibile connettere Bitget'}), 503
        
        if not strategy:
            init_strategy()
        
        bot_running = True
        bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
        bot_thread.start()
        
        return jsonify({'status': 'started', 'message': 'Bot avviato'})
    except Exception as e:
        bot_running = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the trading bot"""
    global bot_running
    
    bot_running = False
    return jsonify({'status': 'stopped', 'message': 'Bot fermato'})

def run_bot_loop():
    """Main bot trading loop"""
    import time
    
    check_interval = int(os.getenv('CHECK_INTERVAL', 5))
    min_amount = float(os.getenv('MIN_AMOUNT', 100))
    target_gain = float(os.getenv('TARGET_GAIN', 2))
    
    while bot_running:
        try:
            symbol = os.getenv('TRADING_PAIR', 'XRP/USDT')
            
            # Fetch data
            df = data_manager.download_data(symbol, '1m', limit=500)
            
            if df.empty:
                time.sleep(check_interval)
                continue
            
            # Get signal
            signal = strategy.generate_signals(df)
            
            # Execute trade on signal
            if signal['signal'] in ['LONG', 'SHORT']:
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker['last']
                quantity = min_amount / current_price
                
                trade_type = 'buy' if signal['signal'] == 'LONG' else 'sell'
                
                try:
                    if trade_type == 'buy':
                        order = exchange.create_market_buy_order(symbol, quantity)
                    else:
                        order = exchange.create_market_sell_order(symbol, quantity)
                    
                    print(f"[{datetime.now()}] Trade {trade_type} eseguito: {quantity} @ ${current_price}")
                except:
                    pass
            
            time.sleep(check_interval)
        except Exception as e:
            print(f"Errore nel bot loop: {e}")
            time.sleep(check_interval)

# ═══════════════════════════════════
# SERVER STARTUP
# ═══════════════════════════════════

if __name__ == '__main__':
    # Initialize on startup
    init_exchange()
    init_strategy()
    
    print("=" * 50)
    print("SCALPER BOT · API SERVER")
    print("=" * 50)
    print(f"Exchange connected: {exchange is not None}")
    print(f"Strategy initialized: {strategy is not None}")
    print("=" * 50)
    
    app.run(host='localhost', port=5000, debug=False)
