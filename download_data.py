#!/usr/bin/env python3
"""
Script per scaricare e cachare i dati da Binance
Uso: python download_data.py
"""

from data_manager import DataManager
from datetime import datetime, timedelta

def download_1m_data():
    """Scarica i dati 1 minuto degli ultimi 7 giorni"""
    data_manager = DataManager()
    
    print("📥 Scaricamento dati 1 minuto XRP/USDT...")
    df = data_manager.fetch_ohlcv_live('XRPUSDT', '1m', limit=10080)  # 7 giorni * 1440 minuti
    
    if df is not None:
        data_manager.save_data_cache(df, 'xrp_1m_latest.csv')
        print(f"✅ Salvato: {len(df)} candle")
    else:
        print("❌ Errore nel download")

def download_daily_data():
    """Scarica i dati giornalieri degli ultimi 6 mesi"""
    data_manager = DataManager()
    
    print("📥 Scaricamento dati giornalieri XRP/USDT...")
    df = data_manager.fetch_ohlcv_live('XRPUSDT', '1d', limit=180)
    
    if df is not None:
        data_manager.save_data_cache(df, 'xrp_daily.csv')
        print(f"✅ Salvato: {len(df)} candle")
    else:
        print("❌ Errore nel download")

if __name__ == '__main__':
    download_1m_data()
    download_daily_data()
    print("\n✨ Download completato!")
