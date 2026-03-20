"""
Visualizzazione avanzata dei risultati con i 16+ indicatori
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import warnings

warnings.filterwarnings('ignore')

def plot_advanced_indicators(df, start_idx=0, end_idx=None, title="Advanced Scalper Strategy"):
    """
    Plotta tutti gli indicatori su multiple righe.
    Questo è un visualizzatore completo.
    """
    if end_idx is None:
        end_idx = min(start_idx + 500, len(df))  # Max 500 candle
    
    df_plot = df.iloc[start_idx:end_idx].copy()
    dates = range(len(df_plot))
    
    # Crea la figura con subplots
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(8, 1, hspace=0.3)
    
    # ============ PRICE & MOVING AVERAGES ============
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(dates, df_plot['close'], label='Close', color='black', linewidth=1.5, alpha=0.7)
    ax1.plot(dates, df_plot['ema_fast'], label='EMA5', color='green', alpha=0.7)
    ax1.plot(dates, df_plot['ema_medium'], label='EMA13', color='orange', alpha=0.7)
    ax1.plot(dates, df_plot['ema_slow'], label='EMA50', color='red', alpha=0.7)
    
    # Colora i segnali
    long_signals = df_plot[df_plot['signal'] == 1]
    short_signals = df_plot[df_plot['signal'] == -1]
    
    if len(long_signals) > 0:
        ax1.scatter(long_signals.index - start_idx, long_signals['close'], 
                   color='green', marker='^', s=100, label='Long Signal', zorder=5)
    if len(short_signals) > 0:
        ax1.scatter(short_signals.index - start_idx, short_signals['close'], 
                   color='red', marker='v', s=100, label='Short Signal', zorder=5)
    
    ax1.set_title(f'{title} - Price & Moving Averages', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # ============ BOLLINGER BANDS ============
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(dates, df_plot['close'], label='Close', color='black', linewidth=1)
    ax2.fill_between(dates, df_plot['bb_upper'], df_plot['bb_lower'], alpha=0.2, color='blue')
    ax2.plot(dates, df_plot['bb_upper'], color='blue', linestyle='--', alpha=0.5, label='BB Upper')
    ax2.plot(dates, df_plot['bb_middle'], color='blue', alpha=0.7, label='BB Middle')
    ax2.plot(dates, df_plot['bb_lower'], color='blue', linestyle='--', alpha=0.5, label='BB Lower')
    ax2.set_title('Bollinger Bands', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # ============ RSI & KDJ ============
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.plot(dates, df_plot['rsi'], label='RSI(14)', color='purple', linewidth=1.5)
    ax3.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
    ax3.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
    ax3.fill_between(dates, 30, 70, alpha=0.1, color='gray')
    ax3.set_ylim(0, 100)
    ax3.set_title('RSI(14) & KDJ Levels', fontsize=10, fontweight='bold')
    ax3.legend(loc='upper left', fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # ============ KDJ Lines ============
    if 'kdj_k' in df_plot.columns:
        ax3_2 = ax3.twinx()
        ax3_2.plot(dates, df_plot['kdj_k'], label='KDJ_K', color='cyan', linewidth=1, alpha=0.7)
        ax3_2.plot(dates, df_plot['kdj_d'], label='KDJ_D', color='magenta', linewidth=1, alpha=0.7)
        ax3_2.set_ylim(0, 100)
        ax3_2.legend(loc='upper right', fontsize=8)
    
    # ============ MACD ============
    ax4 = fig.add_subplot(gs[3, 0])
    colors = ['green' if df_plot['macd_diff'].iloc[i] > 0 else 'red' 
              for i in range(len(df_plot))]
    ax4.bar(dates, df_plot['macd_diff'], label='MACD Histogram', color=colors, alpha=0.6)
    ax4.plot(dates, df_plot['macd'], label='MACD', color='blue', linewidth=1.5)
    ax4.plot(dates, df_plot['macd_signal'], label='Signal', color='red', linewidth=1.5)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax4.set_title('MACD', fontsize=10, fontweight='bold')
    ax4.legend(loc='upper left', fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    # ============ VOLUME & OBV ============
    ax5 = fig.add_subplot(gs[4, 0])
    colors = ['green' if df_plot['close'].iloc[i] > df_plot['open'].iloc[i] else 'red' 
              for i in range(len(df_plot))]
    ax5.bar(dates, df_plot['volume'], label='Volume', color=colors, alpha=0.5)
    ax5.plot(dates, df_plot['volume_ma'], label='Volume MA(20)', color='orange', linewidth=1.5)
    ax5.set_title('Volume Analysis', fontsize=10, fontweight='bold')
    ax5.legend(loc='upper left', fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # OBV su asse secondario
    ax5_2 = ax5.twinx()
    ax5_2.plot(dates, df_plot['obv'], label='OBV', color='purple', alpha=0.7, linewidth=1)
    ax5_2.plot(dates, df_plot['obv_ma'], label='OBV MA', color='darkviolet', alpha=0.7, linewidth=1.5)
    ax5_2.legend(loc='upper right', fontsize=8)
    
    # ============ MOMENTUM & ADL ============
    ax6 = fig.add_subplot(gs[5, 0])
    ax6.plot(dates, df_plot['momentum'], label='Momentum', color='blue', linewidth=1)
    ax6.plot(dates, df_plot['momentum_ma'], label='Momentum MA', color='orange', linewidth=1.5)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax6.set_title('Momentum & ADL', fontsize=10, fontweight='bold')
    ax6.legend(loc='upper left', fontsize=8)
    ax6.grid(True, alpha=0.3)
    
    # ADL su asse secondario
    if 'adl' in df_plot.columns:
        ax6_2 = ax6.twinx()
        ax6_2.plot(dates, df_plot['adl'], label='ADL', color='purple', alpha=0.7, linewidth=1)
        ax6_2.legend(loc='upper right', fontsize=8)
    
    # ============ ATR & VOLATILITY ============
    ax7 = fig.add_subplot(gs[6, 0])
    ax7.plot(dates, df_plot['atr'], label='ATR(14)', color='green', linewidth=1.5)
    ax7.fill_between(dates, 0, df_plot['atr'], alpha=0.2, color='green')
    ax7.set_title('ATR & Volatility', fontsize=10, fontweight='bold')
    ax7.legend(loc='upper left', fontsize=8)
    ax7.grid(True, alpha=0.3)
    
    # Volatility su asse secondario
    if 'volatility_current' in df_plot.columns:
        ax7_2 = ax7.twinx()
        ax7_2.plot(dates, df_plot['volatility_current'], 
                  label='Volatility (Current)', color='red', alpha=0.7, linewidth=1.5)
        if 'volatility_hist' in df_plot.columns:
            ax7_2.plot(dates, df_plot['volatility_hist'], 
                      label='Volatility (Historical)', color='orange', alpha=0.7, linewidth=1)
        ax7_2.legend(loc='upper right', fontsize=8)
    
    # ============ SIGNAL STRENGTH & FEAR/GREED ============
    ax8 = fig.add_subplot(gs[7, 0])
    colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' 
              for x in df_plot['total_score']]
    ax8.bar(dates, df_plot['total_score'], label='Signal Score', color=colors, alpha=0.6)
    ax8.axhline(y=0.35, color='green', linestyle='--', alpha=0.5, label='Long Threshold (0.35)')
    ax8.axhline(y=-0.35, color='red', linestyle='--', alpha=0.5, label='Short Threshold (-0.35)')
    ax8.set_title('Overall Signal Strength & Fear/Greed', fontsize=10, fontweight='bold')
    ax8.legend(loc='upper left', fontsize=8)
    ax8.grid(True, alpha=0.3)
    
    # Fear & Greed su asse secondario
    if 'fear_greed' in df_plot.columns:
        ax8_2 = ax8.twinx()
        ax8_2.plot(dates, df_plot['fear_greed'], 
                  label='Fear & Greed Index', color='purple', alpha=0.7, linewidth=1.5)
        ax8_2.fill_between(dates, 0, 100, alpha=0.05, color='purple')
        ax8_2.set_ylim(0, 100)
        ax8_2.legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    
    # Salva la figura
    plt.savefig('advanced_strategy_analysis.png', dpi=100, bbox_inches='tight')
    print("✅ Grafico salvato in 'advanced_strategy_analysis.png'")
    
    plt.show()

def plot_pivot_points(df, start_idx=0, end_idx=None):
    """Plotta i Pivot Points e i Fibonacci Levels"""
    if end_idx is None:
        end_idx = min(start_idx + 200, len(df))
    
    df_plot = df.iloc[start_idx:end_idx].copy()
    dates = range(len(df_plot))
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Price
    ax.plot(dates, df_plot['close'], label='Close', color='black', linewidth=2)
    
    # Pivot Points
    if 'pivot' in df_plot.columns:
        ax.plot(dates, df_plot['pivot'], label='Pivot', color='blue', linewidth=1.5, linestyle='-')
        ax.plot(dates, df_plot['support_1'], label='S1', color='green', linewidth=1, linestyle='--')
        ax.plot(dates, df_plot['resistance_1'], label='R1', color='red', linewidth=1, linestyle='--')
        ax.plot(dates, df_plot['support_2'], label='S2', color='darkgreen', linewidth=1, linestyle=':')
        ax.plot(dates, df_plot['resistance_2'], label='R2', color='darkred', linewidth=1, linestyle=':')
    
    # Fibonacci Levels
    if 'fib_61.8' in df_plot.columns:
        ax.plot(dates, df_plot['fib_61.8'], label='Fib 61.8%', color='purple', 
               linewidth=1, linestyle='-', alpha=0.7)
        ax.plot(dates, df_plot['fib_38.2'], label='Fib 38.2%', color='orange', 
               linewidth=1, linestyle='-', alpha=0.7)
    
    ax.set_title('Pivot Points & Fibonacci Levels', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pivot_fibonacci_analysis.png', dpi=100, bbox_inches='tight')
    print("✅ Grafico Pivot Points salvato in 'pivot_fibonacci_analysis.png'")
    
    plt.show()

def plot_trades(df, trades_list, start_idx=0, end_idx=None):
    """Plotta i trades effettuati"""
    if end_idx is None:
        end_idx = min(start_idx + 500, len(df))
    
    df_plot = df.iloc[start_idx:end_idx].copy()
    dates = range(len(df_plot))
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Price
    ax.plot(dates, df_plot['close'], label='Close', color='black', linewidth=1)
    
    # Plot trades che rientrano nella finestra
    for trade in trades_list:
        entry_idx = trade['entry_idx']
        close_idx = trade['entry_time']
        
        if entry_idx >= start_idx and entry_idx < end_idx:
            rel_idx = entry_idx - start_idx
            color = 'green' if trade['type'] == 'long' else 'red'
            marker = '^' if trade['type'] == 'long' else 'v'
            
            # Entry
            ax.scatter(rel_idx, trade['entry_price'], color=color, marker=marker, s=200, zorder=5)
            
            # Exit (se visibile)
            if isinstance(close_idx, int) and close_idx < end_idx:
                ax.scatter(close_idx - start_idx, trade['close_price'], 
                          color=color, marker='s', s=100, alpha=0.5, zorder=5)
                
                # Linea tra entry e exit
                ax.plot([rel_idx, close_idx - start_idx], 
                       [trade['entry_price'], trade['close_price']], 
                       color=color, alpha=0.3, linewidth=1)
    
    ax.set_title('Trades Execution', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('trades_execution.png', dpi=100, bbox_inches='tight')
    print("✅ Grafico Trades salvato in 'trades_execution.png'")
    
    plt.show()

def main():
    """Carica e visualizza i risultati del backtest"""
    print("📊 Visualizzazione Risultati Advanced Strategy")
    print("="*60)
    
    # Carica i dati
    try:
        df = pd.read_csv('advanced_backtest_indicators.csv', index_col=0, parse_dates=True)
        print(f"✅ Caricati {len(df)} candle")
    except FileNotFoundError:
        print("❌ File 'advanced_backtest_indicators.csv' non trovato")
        print("   Esegui prima 'python advanced_backtest.py'")
        return
    
    # Carica i trades
    try:
        trades = pd.read_csv('advanced_backtest_results.csv')
        print(f"✅ Caricati {len(trades)} trades")
    except FileNotFoundError:
        trades = []
        print("⚠️  File 'advanced_backtest_results.csv' non trovato")
    
    # Scelta visualizzazione
    print("\n📈 Opzioni di visualizzazione:")
    print("1. Tutti gli indicatori (completo)")
    print("2. Pivot Points & Fibonacci")
    print("3. Esecuzione Trades")
    print("4. Tutte le visualizzazioni")
    
    choice = input("\nScelta (1-4): ").strip()
    
    if choice in ['1', '4']:
        plot_advanced_indicators(df, start_idx=0, end_idx=min(500, len(df)))
    
    if choice in ['2', '4']:
        plot_pivot_points(df, start_idx=0, end_idx=min(200, len(df)))
    
    if choice in ['3', '4'] and len(trades) > 0:
        plot_trades(df, trades.to_dict('records'))
    
    print("\n✅ Visualizzazione completata!")

if __name__ == "__main__":
    main()
