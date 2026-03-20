"""
Advanced Backtester - Esegue backtest con la strategia avanzata
"""

import pandas as pd
import numpy as np
from advanced_scalper_strategy import AdvancedScalperStrategy
from data_manager import DataManager
import config
from datetime import datetime

class AdvancedBacktester:
    """Backtester per la strategia avanzata con tutti gli indicatori"""
    
    def __init__(self, initial_balance=config.INITIAL_BALANCE):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity = initial_balance
        self.trades = []
        self.data_manager = DataManager()
        self.strategy = AdvancedScalperStrategy()
        
    def run_backtest(self, df, min_signal_strength=0.35):
        """
        Esegue il backtest sulla serie storica.
        
        Args:
            df: DataFrame con OHLCV data
            min_signal_strength: Forza minima del segnale (0-1)
        
        Returns:
            DataFrame e report con statistiche
        """
        print("Calcolo indicatori avanzati...")
        df = self.strategy.calculate_all_indicators(df)
        
        print("Generazione segnali...")
        df = self.strategy.generate_signals(df)
        
        position = None
        trade_num = 0
        
        print("Esecuzione backtest...")
        for idx in range(len(df)):
            current_row = df.iloc[idx]
            signal = current_row['signal']
            signal_strength = current_row['signal_strength']
            price = current_row['close']
            timestamp = current_row.name
            
            # Chiudi posizione aperta se segnale opposto o se SL/TP hit
            if position is not None:
                # Check SL/TP
                if position['type'] == 'long':
                    if price >= position['tp']:
                        self._close_position(position, price, idx, 'TP', df.iloc[idx])
                        position = None
                    elif price <= position['sl']:
                        self._close_position(position, price, idx, 'SL', df.iloc[idx])
                        position = None
                elif position['type'] == 'short':
                    if price <= position['tp']:
                        self._close_position(position, price, idx, 'TP', df.iloc[idx])
                        position = None
                    elif price >= position['sl']:
                        self._close_position(position, price, idx, 'SL', df.iloc[idx])
                        position = None
                
                # Check opposto segnale
                if position is not None and signal != 0 and signal != position['signal']:
                    self._close_position(position, price, idx, 'Opposite Signal', df.iloc[idx])
                    position = None
            
            # Apri nuova posizione se segnale sufficientemente forte
            if position is None and signal != 0 and signal_strength >= min_signal_strength:
                # Calcola TP e SL
                tp_sl = self.strategy.calculate_dynamic_tp_sl(price, signal, df.iloc[:idx+1])
                
                # Calcola dimensione posizione
                position_size = self._calculate_position_size(price, tp_sl)
                
                position = {
                    'type': 'long' if signal == 1 else 'short',
                    'entry_price': price,
                    'entry_idx': idx,
                    'entry_time': timestamp,
                    'size': position_size,
                    'signal': signal,
                    'tp': tp_sl['tp'],
                    'sl': tp_sl['sl'],
                    'trade_num': trade_num,
                    'signal_strength': signal_strength,
                    'atr': tp_sl.get('atr', 0)
                }
                trade_num += 1
        
        # Chiudi posizione aperta al fine del backtest
        if position is not None:
            last_price = df.iloc[-1]['close']
            self._close_position(position, last_price, len(df) - 1, 'Backtest End', df.iloc[-1])
        
        return df, self._generate_report()
    
    def _calculate_position_size(self, price, tp_sl):
        """Calcola la dimensione della posizione basata sul rischio"""
        if tp_sl['tp'] == tp_sl['entry'] or tp_sl['sl'] == tp_sl['entry']:
            return 0.01  # Fallback minimo
        
        risk_amount = self.balance * config.RISK_PER_TRADE
        
        # Calcola il rischio in USDT
        if abs(price - tp_sl['sl']) > 0:
            position_size = risk_amount / abs(price - tp_sl['sl'])
        else:
            position_size = 0.01
        
        # Limita la posizione
        position_size = min(
            position_size,
            self.balance / price * 0.1  # Max 10% del balance
        )
        
        return max(position_size, 0.001)  # Min 0.001
    
    def _close_position(self, position, close_price, close_idx, close_reason, row):
        """Chiude una posizione e registra il trade"""
        if position['type'] == 'long':
            pnl = (close_price - position['entry_price']) * position['size']
            roi = ((close_price - position['entry_price']) / position['entry_price']) * 100
        else:
            pnl = (position['entry_price'] - close_price) * position['size']
            roi = ((position['entry_price'] - close_price) / position['entry_price']) * 100
        
        # Aggiorna il balance
        self.balance += pnl
        
        # Registra il trade
        trade = {
            'trade_num': position['trade_num'],
            'type': position['type'],
            'entry_price': position['entry_price'],
            'close_price': close_price,
            'entry_time': position['entry_time'],
            'close_time': row.name,
            'size': position['size'],
            'pnl': pnl,
            'roi': roi,
            'close_reason': close_reason,
            'bars': close_idx - position['entry_idx'],
            'signal_strength': position.get('signal_strength', 0),
            'atr': position.get('atr', 0),
            'indicators': {
                'rsi': row.get('rsi', 0),
                'macd': row.get('macd', 0),
                'obv': row.get('obv', 0),
                'adx': row.get('adx', 0),
                'volatility': row.get('volatility_current', 0),
            }
        }
        
        self.trades.append(trade)
    
    def _generate_report(self):
        """Genera un report completo del backtest"""
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'roi': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'max_drawdown': 0,
                'profit_factor': 0,
                'trades': []
            }
        
        df_trades = pd.DataFrame(self.trades)
        
        winning = df_trades[df_trades['pnl'] > 0]
        losing = df_trades[df_trades['pnl'] < 0]
        
        total_pnl = df_trades['pnl'].sum()
        total_roi = df_trades['roi'].sum()
        
        report = {
            'total_trades': len(df_trades),
            'winning_trades': len(winning),
            'losing_trades': len(losing),
            'win_rate': (len(winning) / len(df_trades) * 100) if len(df_trades) > 0 else 0,
            'total_pnl': total_pnl,
            'roi': (total_pnl / self.initial_balance) * 100,
            'avg_win': winning['pnl'].mean() if len(winning) > 0 else 0,
            'avg_loss': losing['pnl'].mean() if len(losing) > 0 else 0,
            'max_drawdown': self._calculate_max_drawdown(),
            'profit_factor': (winning['pnl'].sum() / abs(losing['pnl'].sum())) if len(losing) > 0 else 0,
            'best_trade': df_trades['pnl'].max(),
            'worst_trade': df_trades['pnl'].min(),
            'avg_bars_held': df_trades['bars'].mean(),
            'trades': self.trades,
            'final_balance': self.balance
        }
        
        return report
    
    def _calculate_max_drawdown(self):
        """Calcola il massimo drawdown"""
        if not self.trades:
            return 0
        
        cumulative = self.initial_balance
        peak = cumulative
        max_dd = 0
        
        for trade in self.trades:
            cumulative += trade['pnl']
            if cumulative < peak:
                dd = (peak - cumulative) / peak * 100
                max_dd = max(max_dd, dd)
            else:
                peak = cumulative
        
        return max_dd
    
    def print_report(self, report):
        """Stampa il report in formato leggibile"""
        print("\n" + "="*60)
        print("BACKTEST REPORT - ADVANCED SCALPER STRATEGY")
        print("="*60)
        print(f"\n📊 STATISTICHE GENERALI:")
        print(f"   Total Trades: {report['total_trades']}")
        print(f"   Winning Trades: {report['winning_trades']}")
        print(f"   Losing Trades: {report['losing_trades']}")
        print(f"   Win Rate: {report['win_rate']:.2f}%")
        
        print(f"\n💰 PROFITTI/PERDITE:")
        print(f"   Total PnL: ${report['total_pnl']:.2f}")
        print(f"   ROI: {report['roi']:.2f}%")
        print(f"   Initial Balance: ${self.initial_balance:.2f}")
        print(f"   Final Balance: ${report['final_balance']:.2f}")
        
        print(f"\n📈 METRICHE DI PERFORMANCE:")
        print(f"   Average Win: ${report['avg_win']:.2f}")
        print(f"   Average Loss: ${report['avg_loss']:.2f}")
        print(f"   Max Drawdown: {report['max_drawdown']:.2f}%")
        print(f"   Profit Factor: {report['profit_factor']:.2f}")
        print(f"   Best Trade: ${report['best_trade']:.2f}")
        print(f"   Worst Trade: ${report['worst_trade']:.2f}")
        print(f"   Avg Bars Held: {report['avg_bars_held']:.1f}")
        
        print("\n" + "="*60)
    
    def export_trades_csv(self, filename='advanced_backtest_results.csv'):
        """Esporta i trades in CSV"""
        if not self.trades:
            print("Nessun trade da esportare")
            return
        
        df = pd.DataFrame(self.trades)
        df.to_csv(filename, index=False)
        print(f"✅ Trades esportati in {filename}")
