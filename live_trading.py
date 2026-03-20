#!/usr/bin/env python3
"""
Main script per il trading live
Uso: python live_trading.py
"""

import sys
from live_trader import LiveTrader
from data_manager import DataManager
import config

def main():
    if config.BINANCE_API_KEY == 'your_api_key_here':
        print("❌ ERRORE: Configura le API keys nel file .env")
        print("1. Copia .env.example a .env")
        print("2. Inserisci le tue API keys da Binance")
        return
    
    print("🚀 Avvio trading live XRP SCALPER")
    print(f"Simbolo: {config.SYMBOL}")
    print(f"Leva: {config.LEVERAGE}x")
    print(f"Rischio per trade: {config.RISK_PER_TRADE * 100}%")
    print(f"Max loss giornaliero: {config.MAX_DAILY_LOSS * 100}%")
    print("\n⚠️  ATTENZIONE: Questo è trading reale con denaro vero!")
    print("Premi Ctrl+C per fermare il bot in qualsiasi momento\n")
    
    input("Premi INVIO per continuare...")
    
    trader = LiveTrader()
    balance = trader.get_balance()
    
    if balance is None:
        print("❌ Errore nel collegamento con Binance. Controlla le API keys")
        return
    
    print(f"\n💰 Balance: {balance:.2f} USDT")
    print("Bot avviato. Monitoraggio in corso...\n")
    
    trader.run_live(check_interval=60)

if __name__ == '__main__':
    main()
