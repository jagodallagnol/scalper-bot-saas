"""
Script principale per il backtest con la strategia avanzata
Utilizza tutti gli indicatori tecnici avanzati
"""

import pandas as pd
from advanced_backtester import AdvancedBacktester
from data_manager import DataManager
import config

def main():
    print("🤖 ADVANCED SCALPER STRATEGY - BACKTEST")
    print("="*60)
    
    # Inizializza i manager
    data_manager = DataManager()
    backtester = AdvancedBacktester(initial_balance=config.INITIAL_BALANCE)
    
    # Carica i dati
    print("\n📥 Caricamento dati...")
    df_1m, df_daily = data_manager.load_data()
    
    if df_1m is None or len(df_1m) == 0:
        print("❌ Errore: Impossibile caricare i dati")
        return
    
    print(f"✅ Caricati {len(df_1m)} candle da 1 minuto")
    print(f"   Data range: {df_1m.index[0]} - {df_1m.index[-1]}")
    
    # Esegui il backtest
    print("\n🔄 Esecuzione backtest...")
    df_results, report = backtester.run_backtest(
        df_1m,
        min_signal_strength=0.35  # Soglia minima per il segnale
    )
    
    # Stampa il report
    backtester.print_report(report)
    
    # Esporta i risultati
    print("\n💾 Esportazione risultati...")
    backtester.export_trades_csv('advanced_backtest_results.csv')
    
    # Esporta i dati con indicatori e segnali
    output_columns = [
        'close', 'signal', 'total_score', 'signal_strength',
        'ema_fast', 'ema_slow', 'rsi', 'macd', 'macd_signal',
        'kdj_k', 'kdj_d', 'bb_upper', 'bb_lower', 'obv',
        'atr', 'volatility_current', 'adx', 'sar',
        'fear_greed', 'fear_greed_level'
    ]
    
    available_cols = [col for col in output_columns if col in df_results.columns]
    df_results[available_cols].to_csv('advanced_backtest_indicators.csv')
    print("✅ Indicatori esportati in advanced_backtest_indicators.csv")
    
    # Stampa alcuni dettagli sui segnali generati
    print("\n📋 DETTAGLI SEGNALI:")
    signal_counts = df_results['signal'].value_counts()
    print(f"   Long Signals: {signal_counts.get(1, 0)}")
    print(f"   Short Signals: {signal_counts.get(-1, 0)}")
    print(f"   No Signal: {signal_counts.get(0, 0)}")
    
    # Analisi Fear & Greed
    print("\n😨 FEAR & GREED ANALYSIS:")
    if 'fear_greed_level' in df_results.columns:
        fg_counts = df_results['fear_greed_level'].value_counts()
        for level, count in fg_counts.items():
            print(f"   {level}: {count} candle")
    
    # Volatilità media
    print("\n📊 VOLATILITÀ:")
    if 'volatility_current' in df_results.columns:
        avg_vol = df_results['volatility_current'].mean()
        max_vol = df_results['volatility_current'].max()
        print(f"   Media: {avg_vol:.2f}%")
        print(f"   Massima: {max_vol:.2f}%")
    
    print("\n" + "="*60)
    print("✅ Backtest completato!")

if __name__ == "__main__":
    main()
