import pandas as pd
import json
import os
from datetime import datetime, timedelta
import ccxt

class DataManager:
    def __init__(self, symbol='XRPUSDT'):
        self.symbol = symbol
        self.data_dir = 'data'
        self.exchange = ccxt.bitget()
        
    def load_local_data(self, filename):
        """Carica dati locali da file CSV"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            
            # Rinomina le colonne per standardizzarle
            column_mapping = {
                'Open time': 'time',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            }
            
            df.rename(columns=column_mapping, inplace=True)
            
            # Seleziona solo le colonne necessarie
            if 'time' in df.columns:
                df['time'] = pd.to_datetime(df['time'])
                df = df[['time', 'open', 'high', 'low', 'close', 'volume']].copy()
                df.set_index('time', inplace=True)
                return df
            else:
                print(f"Colonne non riconosciute in {filepath}")
                return None
        else:
            print(f"File {filepath} non trovato")
            return None
    
    def fetch_ohlcv_live(self, symbol, timeframe='1m', limit=300):
        """Scarica dati OHLCV live da Binance"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Errore nel fetch dei dati: {e}")
            return None
    
    def save_data_cache(self, df, filename):
        """Salva dati in cache per uso offline"""
        filepath = os.path.join(self.data_dir, filename)
        os.makedirs(self.data_dir, exist_ok=True)
        df.to_csv(filepath)
        print(f"Dati salvati in {filepath}")
    
    def get_daily_candles(self, symbol, limit=30):
        """Scarica i candle giornalieri per il filtro di trend"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Errore nel fetch dei candle giornalieri: {e}")
            return None
