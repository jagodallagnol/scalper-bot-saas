import time
import pandas as pd
from datetime import datetime
import ccxt
from data_manager import DataManager
from strategy import ScalperStrategy
import config
import logging

# Setup logging
logging.basicConfig(
    filename='trading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LiveTrader:
    def __init__(self):
        self.exchange = ccxt.bitget({
            'apiKey': config.BITGET_API_KEY,
            'secret': config.BITGET_SECRET_KEY,
            'password': config.BITGET_PASSWORD,
            'enableRateLimit': True,
            'options': {'defaultType': 'swap'}
        })
        self.exchange.set_sandbox_mode(False)  # Cambia a True per testare in sandbox
        
        self.symbol = config.SYMBOL
        self.leverage = config.LEVERAGE
        self.data_manager = DataManager()
        self.strategy = ScalperStrategy()
        
        self.position = None
        self.balance_history = []
        self.daily_loss = 0
        
        self._setup_leverage()
    
    def _setup_leverage(self):
        """Configura la leva sul pair"""
        try:
            self.exchange.set_leverage(self.leverage, self.symbol)
            logging.info(f"Leva impostata a {self.leverage}x")
        except Exception as e:
            logging.error(f"Errore nel setup della leva: {e}")
    
    def get_balance(self):
        """Ottiene il balance del conto"""
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance['USDT']['free']
            return usdt_balance
        except Exception as e:
            logging.error(f"Errore nel fetch del balance: {e}")
            return None
    
    def place_order(self, side, amount, order_type='market', price=None):
        """Piazza un ordine
        
        Args:
            side: 'buy' o 'sell'
            amount: Quantità in USDT
            order_type: 'market' o 'limit'
            price: Prezzo (richiesto per 'limit')
        """
        try:
            if order_type == 'market':
                order = self.exchange.create_market_order(
                    self.symbol, side, amount
                )
            else:
                order = self.exchange.create_limit_order(
                    self.symbol, side, amount, price
                )
            
            logging.info(f"Ordine {side} eseguito: {order}")
            return order
        except Exception as e:
            logging.error(f"Errore nel piazzamento dell'ordine: {e}")
            return None
    
    def close_position(self, position_info):
        """Chiude una posizione aperta"""
        try:
            side = 'sell' if position_info['direction'] == 'long' else 'buy'
            amount = position_info['amount']
            
            order = self.exchange.create_market_order(
                self.symbol, side, amount
            )
            
            logging.info(f"Posizione chiusa: {order}")
            return order
        except Exception as e:
            logging.error(f"Errore nella chiusura della posizione: {e}")
            return None
    
    def set_stop_loss_take_profit(self, position_type, entry_price, tp, sl, amount):
        """Imposta Stop Loss e Take Profit
        
        Nota: Supporto Bitget tramite trigger ccxt (ordini di tipo market con triggerPrice)
        """
        try:
            # Take Profit
            tp_side = 'sell' if position_type == 'long' else 'buy'
            self.exchange.create_order(
                symbol=self.symbol,
                type='market',
                side=tp_side,
                amount=amount,
                price=None,
                params={'triggerPrice': tp, 'reduceOnly': True}
            )
            
            # Stop Loss
            sl_side = 'sell' if position_type == 'long' else 'buy'
            self.exchange.create_order(
                symbol=self.symbol,
                type='market',
                side=sl_side,
                amount=amount,
                price=None,
                params={'triggerPrice': sl, 'reduceOnly': True}
            )
            
            logging.info(f"TP: {tp}, SL: {sl}")
        except Exception as e:
            logging.warning(f"Errore nel setup TP/SL: {e}")
    
    def get_open_position(self):
        """Ottiene le posizioni aperte"""
        try:
            positions = self.exchange.fetch_positions([self.symbol])
            for pos in positions:
                if pos['contracts'] > 0:
                    return {
                        'symbol': pos['symbol'],
                        'direction': 'long' if pos['side'] == 'long' else 'short',
                        'amount': pos['contracts'],
                        'entry_price': pos['average'],
                        'current_price': pos['last'],
                        'unrealized_pnl': pos['unrealizedPnl']
                    }
            return None
        except Exception as e:
            logging.error(f"Errore nel fetch delle posizioni: {e}")
            return None
    
    def run_live(self, check_interval=60):
        """Esegue il trading in real-time
        
        Args:
            check_interval: Secondi tra ogni check
        """
        logging.info("Bot di trading avviato")
        print("🤖 Bot di trading LIVE avviato...")
        
        while True:
            try:
                # Ottieni dati attuali
                df = self.data_manager.fetch_ohlcv_live(self.symbol, '1m', limit=100)
                daily_df = self.data_manager.get_daily_candles(self.symbol, limit=30)
                
                if df is None:
                    time.sleep(check_interval)
                    continue
                
                # Calcola indicatori e segnali
                df = self.strategy.calculate_indicators(df)
                daily_trend = self.strategy.check_daily_trend(daily_df)
                df = self.strategy.generate_signals(df, daily_trend)
                
                latest_signal = df.iloc[-1]['signal']
                current_price = df.iloc[-1]['close']
                
                # Controlla posizione aperta
                open_pos = self.get_open_position()
                balance = self.get_balance()
                
                # Logica di trading
                if open_pos is None and latest_signal != 0:
                    # Apri nuova posizione
                    if balance > 0 and self.daily_loss < balance * config.MAX_DAILY_LOSS:
                        position_size = balance * config.RISK_PER_TRADE
                        
                        side = 'buy' if latest_signal == 1 else 'sell'
                        order = self.place_order(side, position_size)
                        
                        if order:
                            tp_sl = self.strategy.calculate_take_profit_stop_loss(
                                current_price, latest_signal
                            )
                            self.set_stop_loss_take_profit(
                                'long' if latest_signal == 1 else 'short',
                                current_price,
                                tp_sl['tp'],
                                tp_sl['sl'],
                                position_size
                            )
                            
                            print(f"📈 Posizione aperta: {side.upper()} a {current_price:.4f}")
                            logging.info(f"Posizione aperta: {side} a {current_price}")
                
                elif open_pos is not None and latest_signal != 0:
                    # Chiudi posizione se segnale opposto
                    if (open_pos['direction'] == 'long' and latest_signal == -1) or \
                       (open_pos['direction'] == 'short' and latest_signal == 1):
                        self.close_position(open_pos)
                        self.daily_loss += abs(open_pos['unrealized_pnl'])
                        print(f"❌ Posizione chiusa. PnL: {open_pos['unrealized_pnl']:.2f} USDT")
                        logging.info(f"Posizione chiusa. PnL: {open_pos['unrealized_pnl']}")
                
                # Log stato
                timestamp = datetime.now().strftime('%H:%M:%S')
                status = f"[{timestamp}] Trend: {daily_trend} | Signal: {latest_signal} | Price: {current_price:.4f}"
                print(status)
                
                time.sleep(check_interval)
            
            except KeyboardInterrupt:
                print("\n⛔ Bot fermato dall'utente")
                logging.info("Bot fermato")
                break
            except Exception as e:
                logging.error(f"Errore nel loop di trading: {e}")
                time.sleep(check_interval)

if __name__ == "__main__":
    import traceback
    try:
        trader = LiveTrader()
        trader.run_live()
    except Exception as e:
        print(f"Failed to start bot: {e}")
        traceback.print_exc()
