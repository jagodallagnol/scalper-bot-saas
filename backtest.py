#!/usr/bin/env python3
"""
Main script per backtest della strategia scalper
Uso: python backtest.py
"""

from backtester import Backtester
from data_manager import DataManager
import pandas as pd

def main():
    print("🔍 Avvio backtest strategia scalper XRP...")
    
    # Carica dati
    data_manager = DataManager()
    df = data_manager.load_local_data('XRPUSD_1m_Binance.csv')
    
    if df is None:
        print("❌ Errore nel caricamento dei dati. Controlla il file CSV")
        return
    
    # Limita ai dati recenti per testing (ultimi 5000 candle = ~3.5 giorni)
    if len(df) > 5000:
        df = df.iloc[-5000:].copy()
    
    print(f"📊 Dati caricati: {len(df)} candle")
    print(f"Periodo: {df.index.min()} a {df.index.max()}")
    
    # Prova a caricare i dati giornalieri localmente
    # Se non disponibili, verranno ignorati nel backtest
    daily_df = None
    try:
        daily_df = pd.read_csv('data/daily_data.csv', index_col=0, parse_dates=True)
        print(f"📈 Dati giornalieri caricati")
    except:
        print("⚠️  Dati giornalieri non disponibili - filtro trend disabilitato")
    
    # Esegui backtest
    backtester = Backtester(initial_balance=1000)
    report = backtester.run_backtest(df, daily_df)
    
    # Stampa report
    backtester.print_report(report)
    
    # Salva report dettagliato
    if report is not None:
        report['trades'].to_csv('backtest_results.csv', index=False)
        print("✅ Risultati salvati in backtest_results.csv")

if __name__ == '__main__':
    main()
