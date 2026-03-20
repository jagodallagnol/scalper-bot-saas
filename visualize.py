#!/usr/bin/env python3
"""
Script per visualizzare i risultati del backtest in modo grafico
Genera grafici dei trade, equity curve, e statistiche
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def visualize_backtest_results():
    """Visualizza i risultati del backtest"""
    
    try:
        trades_df = pd.read_csv('backtest_results.csv')
    except FileNotFoundError:
        print("❌ File backtest_results.csv non trovato")
        print("Esegui prima: python backtest.py")
        return
    
    if len(trades_df) == 0:
        print("❌ Nessun trade nel backtest_results.csv")
        return
    
    # Calcola statistiche
    trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
    winning_trades = trades_df[trades_df['pnl'] > 0]
    losing_trades = trades_df[trades_df['pnl'] < 0]
    
    # Crea figura con 4 subplot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('📊 Backtest Results - XRP Scalper Strategy', fontsize=16, fontweight='bold')
    
    # 1. Equity Curve
    ax1 = axes[0, 0]
    ax1.plot(range(len(trades_df)), 1000 + trades_df['cumulative_pnl'], linewidth=2, color='#1f77b4')
    ax1.axhline(y=1000, color='red', linestyle='--', alpha=0.5, label='Initial Balance')
    ax1.fill_between(range(len(trades_df)), 1000 + trades_df['cumulative_pnl'], 1000, alpha=0.3)
    ax1.set_title('Equity Curve', fontweight='bold')
    ax1.set_xlabel('Trade #')
    ax1.set_ylabel('Balance (USDT)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. PnL per Trade
    ax2 = axes[0, 1]
    colors = ['green' if x > 0 else 'red' for x in trades_df['pnl']]
    ax2.bar(range(len(trades_df)), trades_df['pnl'], color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax2.set_title('PnL per Trade', fontweight='bold')
    ax2.set_xlabel('Trade #')
    ax2.set_ylabel('PnL (USDT)')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Win vs Loss Distribution
    ax3 = axes[1, 0]
    if len(winning_trades) > 0 and len(losing_trades) > 0:
        bp = ax3.boxplot(
            [winning_trades['pnl'], losing_trades['pnl']],
            labels=['Winning Trades', 'Losing Trades'],
            patch_artist=True
        )
        bp['boxes'][0].set_facecolor('lightgreen')
        bp['boxes'][1].set_facecolor('lightcoral')
        ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax3.set_title('Win vs Loss Distribution', fontweight='bold')
        ax3.set_ylabel('PnL (USDT)')
        ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Trade Statistics
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    total_trades = len(trades_df)
    winning = len(winning_trades)
    losing = len(losing_trades)
    win_rate = (winning / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = trades_df['pnl'].sum()
    avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
    avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
    profit_factor = (winning_trades['pnl'].sum() / abs(losing_trades['pnl'].sum())) if len(losing_trades) > 0 else float('inf')
    
    max_win = trades_df['pnl'].max()
    max_loss = trades_df['pnl'].min()
    
    # Crea il testo delle statistiche
    stats_text = f"""
BACKTEST STATISTICS
{'='*40}

Total Trades:        {total_trades}
Winning Trades:      {winning} ({win_rate:.1f}%)
Losing Trades:       {losing} ({100-win_rate:.1f}%)

Total PnL:           ${total_pnl:.2f}
Avg Win:             ${avg_win:.2f}
Avg Loss:            ${avg_loss:.2f}
Max Win:             ${max_win:.2f}
Max Loss:            ${max_loss:.2f}

Profit Factor:       {profit_factor:.2f}
Risk/Reward Ratio:   {abs(avg_win/avg_loss) if avg_loss != 0 else 0:.2f}

ROI:                 {(total_pnl/1000*100):.2f}%
    """
    
    ax4.text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('backtest_visualization.png', dpi=150, bbox_inches='tight')
    print("✅ Grafico salvato: backtest_visualization.png")
    
    # Mostra il grafico
    plt.show()
    
    # Stampa statistiche di dettaglio
    print("\n" + "="*60)
    print("BACKTEST DETAILED STATISTICS".center(60))
    print("="*60)
    print(f"\nTrade Duration (bars):")
    print(f"  Min: {trades_df['duration_bars'].min()}")
    print(f"  Max: {trades_df['duration_bars'].max()}")
    print(f"  Avg: {trades_df['duration_bars'].mean():.1f}")
    
    print(f"\nBest Trade Type:")
    best_long = trades_df[trades_df['type'] == 'long']['pnl'].max()
    best_short = trades_df[trades_df['type'] == 'short']['pnl'].max()
    print(f"  Long:  ${best_long:.2f}")
    print(f"  Short: ${best_short:.2f}")
    
    long_win_rate = (len(trades_df[(trades_df['type'] == 'long') & (trades_df['pnl'] > 0)]) / 
                     len(trades_df[trades_df['type'] == 'long']) * 100) if len(trades_df[trades_df['type'] == 'long']) > 0 else 0
    short_win_rate = (len(trades_df[(trades_df['type'] == 'short') & (trades_df['pnl'] > 0)]) / 
                      len(trades_df[trades_df['type'] == 'short']) * 100) if len(trades_df[trades_df['type'] == 'short']) > 0 else 0
    
    print(f"\nWin Rate by Type:")
    print(f"  Long:  {long_win_rate:.1f}%")
    print(f"  Short: {short_win_rate:.1f}%")
    print("="*60)

if __name__ == '__main__':
    visualize_backtest_results()
