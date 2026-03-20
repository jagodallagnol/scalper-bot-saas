import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import config

class ScalperStrategy:
    def __init__(self):
        self.ma_fast = config.MA_FAST
        self.ma_slow = config.MA_SLOW
        self.rsi_period = config.RSI_PERIOD
        self.rsi_overbought = config.RSI_OVERBOUGHT
        self.rsi_oversold = config.RSI_OVERSOLD
        self.daily_ma = config.DAILY_MA_PERIOD
        
    def calculate_indicators(self, df):
        """Calcola gli indicatori tecnici"""
        # Moving Averages
        df['ema_fast'] = EMAIndicator(close=df['close'], window=self.ma_fast).ema_indicator()
        df['ema_slow'] = EMAIndicator(close=df['close'], window=self.ma_slow).ema_indicator()
        
        # RSI
        df['rsi'] = RSIIndicator(close=df['close'], window=self.rsi_period).rsi()
        
        # Volume Moving Average
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        
        return df
    
    def check_daily_trend(self, daily_df):
        """Controlla il trend giornaliero (filtro)
        Returns: 'up', 'down', 'neutral'
        """
        if daily_df is None or len(daily_df) < self.daily_ma:
            return 'neutral'
        
        daily_df['ma_daily'] = daily_df['close'].rolling(window=self.daily_ma).mean()
        current_price = daily_df['close'].iloc[-1]
        current_ma = daily_df['ma_daily'].iloc[-1]
        
        if current_price > current_ma * 1.002:  # 0.2% sopra
            return 'up'
        elif current_price < current_ma * 0.998:  # 0.2% sotto
            return 'down'
        else:
            return 'neutral'
    
    def generate_signals(self, df, daily_trend='neutral'):
        """Genera segnali di trading
        Returns: DataFrame con colonna 'signal' (-1 short, 0 nothing, 1 long)
        """
        df['signal'] = 0
        
        # Calcola il crossover delle medie
        df['ma_crossover'] = ((df['ema_fast'] > df['ema_slow']).astype(int) - 
                              (df['ema_fast'] < df['ema_slow']).astype(int))
        df['ma_crossover_prev'] = df['ma_crossover'].shift(1)
        
        # Golden Cross (passaggio da negativo a positivo)
        long_ma_cross = (df['ma_crossover'] > 0) & (df['ma_crossover_prev'] <= 0)
        
        # Death Cross (passaggio da positivo a negativo)
        short_ma_cross = (df['ma_crossover'] < 0) & (df['ma_crossover_prev'] >= 0)
        
        # Condizioni aggiuntive
        long_condition = (
            long_ma_cross &  # Golden cross
            (df['rsi'] < self.rsi_overbought) &  # RSI non overbought
            (df['volume'] > df['volume_ma'] * 1.3)  # Volume elevato
        )
        
        short_condition = (
            short_ma_cross &  # Death cross
            (df['rsi'] > self.rsi_oversold) &  # RSI non oversold
            (df['volume'] > df['volume_ma'] * 1.3)  # Volume elevato
        )
        
        # Applica i segnali
        df.loc[long_condition, 'signal'] = 1
        df.loc[short_condition, 'signal'] = -1
        
        # Applica il filtro del trend giornaliero
        if daily_trend == 'up':
            # SHORT solo con RSI molto basso
            df.loc[(df['signal'] == -1) & (df['rsi'] >= 35), 'signal'] = 0
        elif daily_trend == 'down':
            # LONG solo con RSI molto alto
            df.loc[(df['signal'] == 1) & (df['rsi'] <= 65), 'signal'] = 0
        
        return df
    
    def calculate_take_profit_stop_loss(self, entry_price, signal, atr=None):
        """Calcola Take Profit e Stop Loss
        
        Args:
            entry_price: Prezzo di entrata
            signal: 1 per long, -1 per short
            atr: Average True Range (opzionale per dinamico)
        
        Returns:
            dict con tp e sl
        """
        if atr is None:
            atr = entry_price * 0.005  # 0.5% come default
        
        if signal == 1:  # LONG
            tp = entry_price + atr * 2  # 2 ATR per TP
            sl = entry_price - atr  # 1 ATR per SL
        else:  # SHORT
            tp = entry_price - atr * 2
            sl = entry_price + atr
        
        return {'tp': tp, 'sl': sl, 'entry': entry_price}
