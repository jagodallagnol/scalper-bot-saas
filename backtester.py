import pandas as pd
import numpy as np
from data_manager import DataManager
from strategy import ScalperStrategy
import config

class Backtester:
    def __init__(self, initial_balance=config.INITIAL_BALANCE):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity = initial_balance
        self.trades = []
        self.data_manager = DataManager()
        self.strategy = ScalperStrategy()
        
    def run_backtest(self, df, daily_df=None):
        """Esegue il backtest sulla serie storica
        
        Args:
            df: DataFrame con OHLCV data
            daily_df: DataFrame con candle giornalieri per il filtro trend
        """
        # Calcola indicatori
        df = self.strategy.calculate_indicators(df)
        
        # Determina il trend giornaliero iniziale
        daily_trend = self.strategy.check_daily_trend(daily_df) if daily_df is not None else 'neutral'
        
        # Genera segnali
        df = self.strategy.generate_signals(df, daily_trend)
        
        position = None
        trade_num = 0
        
        for idx in range(len(df)):
            current_row = df.iloc[idx]
            signal = current_row['signal']
            price = current_row['close']
            
            # Aggiorna il trend ogni ora (ogni 60 candle da 1 minuto)
            if idx % 60 == 0 and daily_df is not None:
                daily_trend = self.strategy.check_daily_trend(daily_df)
            
            # Chiudi posizione aperta se segnale opposto
            if position is not None:
                pnl = self._calculate_pnl(position, price)
                
                # Controlla Take Profit e Stop Loss
                if position['type'] == 'long':
                    if price >= position['tp'] or price <= position['sl']:
                        self._close_position(position, price, idx)
                        position = None
                elif position['type'] == 'short':
                    if price <= position['tp'] or price >= position['sl']:
                        self._close_position(position, price, idx)
                        position = None
                
                # Controlla segnale opposto
                if position is not None and signal != 0 and signal != position['signal']:
                    self._close_position(position, price, idx)
                    position = None
            
            # Apri nuova posizione se segnale e nessuna posizione aperta
            if position is None and signal != 0:
                # Calcola dimensione della posizione basata su risk management
                position_size = self._calculate_position_size(price)
                
                tp_sl = self.strategy.calculate_take_profit_stop_loss(price, signal)
                
                position = {
                    'type': 'long' if signal == 1 else 'short',
                    'entry_price': price,
                    'entry_idx': idx,
                    'entry_time': current_row.name,
                    'size': position_size,
                    'signal': signal,
                    'tp': tp_sl['tp'],
                    'sl': tp_sl['sl'],
                    'trade_num': trade_num
                }
                trade_num += 1
        
        # Chiudi posizione aperta se rimane al termine
        if position is not None:
            last_price = df.iloc[-1]['close']
            self._close_position(position, last_price, len(df) - 1)
        
        return self._generate_report(df)
    
    def _calculate_position_size(self, price):
        """Calcola la dimensione della posizione basata sul rischio"""
        risk_amount = self.balance * config.RISK_PER_TRADE
        position_size = min(risk_amount / price, self.balance / price * 0.1)
        return position_size
    
    def _calculate_pnl(self, position, current_price):
        """Calcola il PnL non realizzato"""
        if position['type'] == 'long':
            pnl = (current_price - position['entry_price']) * position['size']
        else:
            pnl = (position['entry_price'] - current_price) * position['size']
        return pnl
    
    def _close_position(self, position, exit_price, idx):
        """Chiude una posizione e registra il trade"""
        pnl = self._calculate_pnl(position, exit_price)
        pnl_percent = (pnl / (position['entry_price'] * position['size'])) * 100
        
        self.balance += pnl
        self.equity = self.balance
        
        self.trades.append({
            'trade_num': position['trade_num'],
            'type': position['type'],
            'entry_price': position['entry_price'],
            'entry_time': position['entry_time'],
            'exit_price': exit_price,
            'size': position['size'],
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'duration_bars': idx - position['entry_idx']
        })
    
    def _generate_report(self, df):
        """Genera il report del backtest"""
        trades_df = pd.DataFrame(self.trades)
        
        if len(trades_df) == 0:
            print("Nessun trade eseguito")
            return None
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        avg_pnl = trades_df['pnl'].mean()
        
        report = {
            'initial_balance': self.initial_balance,
            'final_balance': self.balance,
            'total_return': ((self.balance - self.initial_balance) / self.initial_balance) * 100,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'max_win': trades_df['pnl'].max(),
            'max_loss': trades_df['pnl'].min(),
            'profit_factor': abs(trades_df[trades_df['pnl'] > 0]['pnl'].sum() / 
                                trades_df[trades_df['pnl'] < 0]['pnl'].sum()) 
                            if losing_trades > 0 else float('inf'),
            'trades': trades_df
        }
        
        return report
    
    def print_report(self, report):
        """Stampa il report in modo leggibile"""
        if report is None:
            return
        
        print("\n" + "="*60)
        print("BACKTEST REPORT".center(60))
        print("="*60)
        print(f"\nIniziale Balance: ${report['initial_balance']:.2f}")
        print(f"Final Balance:    ${report['final_balance']:.2f}")
        print(f"Total Return:     {report['total_return']:.2f}%")
        
        print(f"\nTotal Trades:     {report['total_trades']}")
        print(f"Winning Trades:   {report['winning_trades']}")
        print(f"Losing Trades:    {report['losing_trades']}")
        print(f"Win Rate:         {report['win_rate']:.2f}%")
        
        print(f"\nTotal PnL:        ${report['total_pnl']:.2f}")
        print(f"Avg PnL:          ${report['avg_pnl']:.2f}")
        print(f"Max Win:          ${report['max_win']:.2f}")
        print(f"Max Loss:         ${report['max_loss']:.2f}")
        print(f"Profit Factor:    {report['profit_factor']:.2f}")
        print("="*60 + "\n")
