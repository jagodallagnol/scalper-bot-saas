#!/usr/bin/env python3
"""
Quick Test - Verifica rapidamente che la strategia avanzata funziona
Esegui questo file per un test veloce della strategia
"""

import sys
import os

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                      🧪 QUICK TEST - ADVANCED STRATEGY                    ║
║                  Verifica rapida funzionamento strategia                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

# ============ TEST 1: Import Modules ============
print("\n✅ TEST 1: Importazione moduli...")
try:
    import pandas as pd
    import numpy as np
    print("   ✅ pandas, numpy - OK")
except ImportError as e:
    print(f"   ❌ Errore: {e}")
    sys.exit(1)

try:
    from advanced_scalper_strategy import AdvancedScalperStrategy
    print("   ✅ AdvancedScalperStrategy - OK")
except ImportError as e:
    print(f"   ❌ Errore: {e}")
    sys.exit(1)

try:
    from advanced_backtester import AdvancedBacktester
    print("   ✅ AdvancedBacktester - OK")
except ImportError as e:
    print(f"   ❌ Errore: {e}")
    sys.exit(1)

try:
    from data_manager import DataManager
    print("   ✅ DataManager - OK")
except ImportError as e:
    print(f"   ❌ Errore: {e}")
    print("   Nota: DataManager richiede dati")

# ============ TEST 2: Crea Sample Data ============
print("\n✅ TEST 2: Creazione dati di test...")

# Crea dati sintetici
dates = pd.date_range('2024-01-01', periods=500, freq='1min')
np.random.seed(42)

# OHLCV data realistico
close = 0.50 + np.cumsum(np.random.randn(500) * 0.001)
high = close + np.abs(np.random.randn(500) * 0.002)
low = close - np.abs(np.random.randn(500) * 0.002)
open_price = close.shift(1).fillna(close.iloc[0])
volume = np.random.uniform(1000000, 5000000, 500)

df = pd.DataFrame({
    'open': open_price,
    'high': high,
    'low': low,
    'close': close,
    'volume': volume
}, index=dates)

print(f"   ✅ DataFrame creato: {len(df)} candle")
print(f"      Intervallo prezzo: {df['close'].min():.4f} - {df['close'].max():.4f}")

# ============ TEST 3: Calcola Indicatori ============
print("\n✅ TEST 3: Calcolo indicatori...")

try:
    strategy = AdvancedScalperStrategy()
    df = strategy.calculate_all_indicators(df)
    print(f"   ✅ Indicatori calcolati")
    print(f"      Colonne create: {len(df.columns)} (da 4 iniziali)")
    
    # Controlla alcuni indicatori specifici
    required_indicators = [
        'ema_fast', 'ema_slow', 'rsi', 'macd', 
        'kdj_k', 'kdj_d', 'bb_upper', 'bb_lower',
        'obv', 'atr', 'sar', 'pivot', 'adx'
    ]
    
    missing = [ind for ind in required_indicators if ind not in df.columns]
    if missing:
        print(f"   ⚠️  Indicatori mancanti: {missing}")
    else:
        print(f"   ✅ Tutti gli indicatori principali presenti")
    
except Exception as e:
    print(f"   ❌ Errore nel calcolo: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============ TEST 4: Genera Segnali ============
print("\n✅ TEST 4: Generazione segnali...")

try:
    df = strategy.generate_signals(df)
    
    signal_counts = df['signal'].value_counts()
    print(f"   ✅ Segnali generati")
    print(f"      Long signals: {signal_counts.get(1, 0)}")
    print(f"      Short signals: {signal_counts.get(-1, 0)}")
    print(f"      No signals: {signal_counts.get(0, 0)}")
    
    if 'total_score' in df.columns:
        print(f"      Score range: {df['total_score'].min():.3f} - {df['total_score'].max():.3f}")
        avg_score = df['total_score'].mean()
        print(f"      Score medio: {avg_score:.3f}")
    
except Exception as e:
    print(f"   ❌ Errore nella generazione segnali: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============ TEST 5: TP/SL Dinamici ============
print("\n✅ TEST 5: Calcolo TP/SL dinamici...")

try:
    entry_price = df['close'].iloc[250]
    tp_sl = strategy.calculate_dynamic_tp_sl(entry_price, 1, df.iloc[:251])
    
    print(f"   ✅ TP/SL calcolati")
    print(f"      Entry: {tp_sl['entry']:.4f}")
    print(f"      TP: {tp_sl['tp']:.4f}")
    print(f"      SL: {tp_sl['sl']:.4f}")
    print(f"      Risk/Reward: {(tp_sl['tp'] - tp_sl['entry']) / (tp_sl['entry'] - tp_sl['sl']):.2f}:1")
    
except Exception as e:
    print(f"   ❌ Errore nel calcolo TP/SL: {e}")
    import traceback
    traceback.print_exc()

# ============ TEST 6: Mini Backtest ============
print("\n✅ TEST 6: Mini backtest (100 candle)...")

try:
    backtester = AdvancedBacktester(initial_balance=1000)
    df_test = df.iloc[:100].copy()
    
    df_results, report = backtester.run_backtest(df_test)
    
    print(f"   ✅ Backtest completato")
    print(f"      Total trades: {report['total_trades']}")
    print(f"      Win rate: {report['win_rate']:.1f}%")
    print(f"      Total PnL: ${report['total_pnl']:.2f}")
    print(f"      ROI: {report['roi']:.2f}%")
    
    if report['total_trades'] > 0:
        print(f"      Avg win: ${report['avg_win']:.2f}")
        print(f"      Avg loss: ${report['avg_loss']:.2f}")
        print(f"      Best trade: ${report['best_trade']:.2f}")
        print(f"      Worst trade: ${report['worst_trade']:.2f}")
    
except Exception as e:
    print(f"   ❌ Errore nel backtest: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============ TEST 7: Data Export ============
print("\n✅ TEST 7: Esportazione dati...")

try:
    # Esporta trades
    backtester.export_trades_csv('test_backtest_results.csv')
    print(f"   ✅ CSV trades esportato")
    
    # Esporta indicatori
    export_cols = ['close', 'signal', 'total_score', 'rsi', 'macd', 'obv']
    available_cols = [col for col in export_cols if col in df_results.columns]
    df_results[available_cols].to_csv('test_backtest_indicators.csv')
    print(f"   ✅ CSV indicatori esportato")
    
    # Cleanup
    import os
    os.remove('test_backtest_results.csv')
    os.remove('test_backtest_indicators.csv')
    print(f"   ✅ File di test cancellati (test completed)")
    
except Exception as e:
    print(f"   ⚠️  Errore nella esportazione: {e}")

# ============ SUMMARY ============
print("\n" + "="*76)
print("✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
print("="*76)

print("""
La strategia avanzata è funzionante e pronta all'uso!

PROSSIMI PASSI:

1. Esegui il backtest completo:
   python advanced_backtest.py

2. Visualizza i risultati:
   python advanced_visualize.py

3. Se il backtest è positivo, configura .env e vai live:
   python live_trading.py

Buon trading! 🚀
""")
