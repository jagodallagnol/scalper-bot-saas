#!/usr/bin/env python3
"""
Script per ottimizzare i parametri della strategia
Testa diverse combinazioni di MA_FAST, MA_SLOW, RSI_PERIOD
"""

from backtester import Backtester
from data_manager import DataManager
from strategy import ScalperStrategy
import pandas as pd
import config

def optimize_parameters():
    """Testa diverse combinazioni di parametri"""
    
    # Carica dati una sola volta
    data_manager = DataManager()
    df = data_manager.load_local_data('XRPUSD_1m_Binance.csv')
    
    if df is None:
        print("❌ Errore nel caricamento dei dati")
        return
    
    # Limita ai dati recenti
    if len(df) > 5000:
        df = df.iloc[-5000:].copy()
    
    print(f"📊 Dati: {len(df)} candle\n")
    
    # Parametri da testare
    ma_fast_values = [3, 5, 7, 9]
    ma_slow_values = [15, 20, 25, 30]
    rsi_period_values = [10, 14, 20]
    
    results = []
    total_tests = len(ma_fast_values) * len(ma_slow_values) * len(rsi_period_values)
    test_num = 0
    
    print(f"🔄 Testing {total_tests} combinazioni di parametri...\n")
    
    for ma_fast in ma_fast_values:
        for ma_slow in ma_slow_values:
            if ma_fast >= ma_slow:  # Skip invalid combinations
                continue
            
            for rsi_period in rsi_period_values:
                test_num += 1
                
                # Aggiorna i parametri della strategia
                strategy = ScalperStrategy()
                strategy.ma_fast = ma_fast
                strategy.ma_slow = ma_slow
                strategy.rsi_period = rsi_period
                
                # Esegui backtest
                backtester = Backtester(initial_balance=1000)
                
                # Calcola indicatori con parametri personalizzati
                df_test = df.copy()
                df_test = strategy.calculate_indicators(df_test)
                df_test = strategy.generate_signals(df_test, 'neutral')
                
                # Runna il backtest
                report = backtester.run_backtest(df_test, None)
                
                if report is not None:
                    results.append({
                        'MA_FAST': ma_fast,
                        'MA_SLOW': ma_slow,
                        'RSI_PERIOD': rsi_period,
                        'Total_Return_%': report['total_return'],
                        'Win_Rate_%': report['win_rate'],
                        'Total_Trades': report['total_trades'],
                        'Profit_Factor': report['profit_factor'],
                        'Final_Balance': report['final_balance']
                    })
                    
                    status = f"[{test_num}/{total_tests}] MA({ma_fast},{ma_slow}) RSI({rsi_period}): " \
                            f"Return {report['total_return']:.2f}% | Win {report['win_rate']:.1f}% | PF {report['profit_factor']:.2f}"
                    print(status)
    
    # Salva e mostra i risultati migliori
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Profit_Factor', ascending=False)
    
    print("\n" + "="*100)
    print("TOP 10 MIGLIORI PARAMETRI (ordinati per Profit Factor)".center(100))
    print("="*100)
    print(results_df.head(10).to_string(index=False))
    print("="*100)
    
    # Salva il report completo
    results_df.to_csv('optimization_results.csv', index=False)
    print(f"\n✅ Risultati completi salvati in optimization_results.csv")
    
    # Raccomandazione
    best = results_df.iloc[0]
    print(f"\n🎯 PARAMETRI CONSIGLIATI:")
    print(f"   MA_FAST = {int(best['MA_FAST'])}")
    print(f"   MA_SLOW = {int(best['MA_SLOW'])}")
    print(f"   RSI_PERIOD = {int(best['RSI_PERIOD'])}")
    print(f"   Profit Factor: {best['Profit_Factor']:.2f}")
    print(f"   Win Rate: {best['Win_Rate_%']:.2f}%")

if __name__ == '__main__':
    optimize_parameters()
