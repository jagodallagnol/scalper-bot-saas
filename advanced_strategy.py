import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, MomentumIndicator, KDJIndicator, MACDIndicator
from ta.trend import EMAIndicator, MACD, AroonIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, AccumulationDistributionIndicator
import config

class AdvancedScalperStrategy:
    """Strategia scalper avanzata con 15+ indicatori tecnici"""
    
    def __init__(self):
        self.ma_fast = config.MA_FAST
        self.ma_slow = config.MA_SLOW
        self.rsi_period = config.RSI_PERIOD
        
    def calculate_all_indicators(self, df):
        """Calcola tutti gli indicatori tecnici"""
        
        # 1. MEDIE MOBILI (EMA)
        df['ema_fast'] = EMAIndicator(close=df['close'], window=self.ma_fast).ema_indicator()
        df['ema_slow'] = EMAIndicator(close=df['close'], window=self.ma_slow).ema_indicator()
        df['ema_50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
        df['ema_200'] = EMAIndicator(close=df['close'], window=200).ema_indicator()
        
        # 2. RSI (Relative Strength Index)
        df['rsi'] = RSIIndicator(close=df['close'], window=self.rsi_period).rsi()
        
        # 3. MOMENTUM
        df['momentum'] = MomentumIndicator(close=df['close'], window=10).momentum()
        df['momentum_pct'] = df['momentum'].pct_change() * 100
        
        # 4. BOLLINGER BANDS
        bb = BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_high'] = bb.bollinger_hband()
        df['bb_low'] = bb.bollinger_lband()
        df['bb_mid'] = bb.bollinger_mavg()
        df['bb_width'] = (df['bb_high'] - df['bb_low']) / df['bb_mid']  # Volatilità
        df['bb_position'] = (df['close'] - df['bb_low']) / (df['bb_high'] - df['bb_low'])
        
        # 5. MACD (Moving Average Convergence Divergence)
        macd = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        df['macd_crossover'] = ((df['macd'] > df['macd_signal']).astype(int) - 
                               (df['macd'] < df['macd_signal']).astype(int))
        
        # 6. KDJ (Stochastic K-D-J)
        kdj = KDJIndicator(high=df['high'], low=df['low'], close=df['close'], window=9, signal=3)
        df['kdj_k'] = kdj.kdj_k()
        df['kdj_d'] = kdj.kdj_d()
        df['kdj_j'] = kdj.kdj_j()
        
        # 7. ATR (Average True Range) - Volatilità
        atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['atr'] = atr.average_true_range()
        df['atr_pct'] = (df['atr'] / df['close']) * 100
        
        # 8. VOLUME INDICATORS
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        df['volume_trend'] = df['volume'].rolling(window=5).mean() > df['volume'].rolling(window=20).mean()
        
        # OBV (On-Balance Volume)
        obv = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume'])
        df['obv'] = obv.on_balance_volume()
        df['obv_ema'] = EMAIndicator(close=df['obv'], window=20).ema_indicator()
        df['obv_momentum'] = df['obv'] - df['obv_ema']
        
        # ADL (Accumulation/Distribution Line)
        adl = AccumulationDistributionIndicator(high=df['high'], low=df['low'], 
                                               close=df['close'], volume=df['volume'])
        df['adl'] = adl.accumulation_distribution()
        df['adl_ema'] = EMAIndicator(close=df['adl'], window=20).ema_indicator()
        
        # 9. VOLATILITÀ STORICA vs ATTUALE
        df['volatility_hist'] = df['close'].pct_change().rolling(window=20).std() * 100
        df['volatility_current'] = df['close'].pct_change().rolling(window=5).std() * 100
        df['volatility_expansion'] = df['volatility_current'] > df['volatility_hist']
        
        # 10. FORCE INDEX (Indice di Forza Trend)
        df['force_index'] = (df['close'].diff() * df['volume']).rolling(window=13).mean()
        df['force_index_ema'] = EMAIndicator(close=df['force_index'], window=13).ema_indicator()
        
        # 11. PIVOT POINTS (Punti Pivot Standard)
        df['pivot'] = (df['high'] + df['low'] + df['close']) / 3
        df['resistance1'] = (2 * df['pivot']) - df['low']
        df['support1'] = (2 * df['pivot']) - df['high']
        df['resistance2'] = df['pivot'] + (df['high'] - df['low'])
        df['support2'] = df['pivot'] - (df['high'] - df['low'])
        
        # 12. SAR (Parabolic SAR) - Implementazione semplificata
        df['sar'] = self._calculate_sar(df)
        
        # 13. FIBONACCI EXTENSION
        df['fib_ext_123'] = self._calculate_fibonacci_extension(df)
        
        # 14. TREND STRENGTH INDEX
        df['trend_strength'] = self._calculate_trend_strength(df)
        
        # 15. PRICE ACTION - Candle Patterns
        df['bullish_candle'] = (df['close'] > df['open']).astype(int)
        df['candle_body'] = abs(df['close'] - df['open'])
        df['candle_wick_ratio'] = df['candle_body'] / (df['high'] - df['low'])
        
        return df
    
    def _calculate_sar(self, df, iaf=0.02, maf=0.2):
        """Parabolic SAR semplificato"""
        sar = df['close'].copy()
        length = len(df)
        
        for i in range(2, length):
            if i < 5:
                sar.iloc[i] = df['close'].iloc[:i].min()
            else:
                sar.iloc[i] = sar.iloc[i-1]
        
        return sar
    
    def _calculate_fibonacci_extension(self, df, period=20):
        """Calcola i livelli Fibonacci Extension"""
        if len(df) < period:
            return df['close']
        
        recent_high = df['high'].iloc[-period:].max()
        recent_low = df['low'].iloc[-period:].min()
        range_val = recent_high - recent_low
        
        fib_ext = df['close'] + (range_val * 1.618)
        return fib_ext
    
    def _calculate_trend_strength(self, df, period=14):
        """Calcola la forza del trend usando ADX-like logic"""
        df_copy = df.copy()
        
        # Uptrend se EMA veloce > lenta
        uptrend = (df_copy['ema_fast'] > df_copy['ema_slow']).astype(int)
        
        # Strength basata su RSI e Momentum
        rsi_strength = df_copy['rsi'] / 100
        momentum_strength = np.abs(df_copy['momentum']) / df_copy['close']
        
        trend_strength = uptrend * (rsi_strength + momentum_strength) / 2
        trend_strength = trend_strength.rolling(window=period).mean()
        
        return trend_strength
    
    def generate_advanced_signals(self, df, daily_trend='neutral'):
        """Genera segnali usando tutti gli indicatori
        
        Returns: DataFrame con colonna 'signal_score' da -100 a 100
        """
        df['signal_score'] = 0
        df['signal_strength'] = 0
        df['signal_reasons'] = ''
        
        # SEGNALI LONG
        long_scores = pd.Series(0.0, index=df.index)
        
        # 1. EMA Crossover (Golden Cross)
        long_scores += np.where(df['ema_fast'] > df['ema_slow'], 15, 0)
        
        # 2. RSI non overbought + momentum positivo
        long_scores += np.where((df['rsi'] < 70) & (df['momentum'] > 0), 15, 0)
        
        # 3. Bollinger Bands - prezzo sotto la banda media
        long_scores += np.where(df['close'] > df['bb_mid'], 10, 0)
        
        # 4. MACD crossover
        long_scores += np.where(df['macd'] > df['macd_signal'], 15, 0)
        
        # 5. KDJ - K > D e non overbought
        long_scores += np.where((df['kdj_k'] > df['kdj_d']) & (df['kdj_k'] < 80), 10, 0)
        
        # 6. Volume elevato
        long_scores += np.where(df['volume_ratio'] > 1.3, 10, 0)
        
        # 7. OBV crescente
        long_scores += np.where(df['obv_momentum'] > 0, 10, 0)
        
        # 8. Force Index positivo
        long_scores += np.where(df['force_index'] > df['force_index_ema'], 10, 0)
        
        # 9. Price Action - candle positiva
        long_scores += np.where(df['bullish_candle'] == 1, 5, 0)
        
        # 10. Trend Strength
        long_scores += np.where(df['trend_strength'] > 0.5, 10, 0)
        
        # SEGNALI SHORT
        short_scores = pd.Series(0.0, index=df.index)
        
        # 1. EMA Crossover (Death Cross)
        short_scores += np.where(df['ema_fast'] < df['ema_slow'], 15, 0)
        
        # 2. RSI non oversold + momentum negativo
        short_scores += np.where((df['rsi'] > 30) & (df['momentum'] < 0), 15, 0)
        
        # 3. Bollinger Bands - prezzo sopra la banda media
        short_scores += np.where(df['close'] < df['bb_mid'], 10, 0)
        
        # 4. MACD crossover
        short_scores += np.where(df['macd'] < df['macd_signal'], 15, 0)
        
        # 5. KDJ - K < D e non oversold
        short_scores += np.where((df['kdj_k'] < df['kdj_d']) & (df['kdj_k'] > 20), 10, 0)
        
        # 6. Volume elevato
        short_scores += np.where(df['volume_ratio'] > 1.3, 10, 0)
        
        # 7. OBV decrescente
        short_scores += np.where(df['obv_momentum'] < 0, 10, 0)
        
        # 8. Force Index negativo
        short_scores += np.where(df['force_index'] < df['force_index_ema'], 10, 0)
        
        # 9. Price Action - candle negativa
        short_scores += np.where(df['bullish_candle'] == 0, 5, 0)
        
        # 10. Trend Strength
        short_scores += np.where(df['trend_strength'] < 0.3, 10, 0)
        
        # Applica filtro trend giornaliero
        if daily_trend == 'up':
            short_scores = np.where(df['rsi'] < 25, short_scores, 0)  # SHORT solo molto strong
        elif daily_trend == 'down':
            long_scores = np.where(df['rsi'] > 75, long_scores, 0)  # LONG solo molto strong
        
        # Calcola segnale finale
        df['signal_score'] = long_scores - short_scores
        
        # Segnali binari (solo se score > 50)
        df['signal'] = 0
        df.loc[df['signal_score'] > 50, 'signal'] = 1
        df.loc[df['signal_score'] < -50, 'signal'] = -1
        
        # Signal strength 0-100
        df['signal_strength'] = np.abs(df['signal_score']).clip(0, 100)
        
        return df
    
    def calculate_dynamic_tp_sl(self, entry_price, signal, df_row):
        """Calcola TP/SL dinamici basati su volatilità e Fibonacci
        
        Args:
            entry_price: Prezzo di entrata
            signal: 1 per long, -1 per short
            df_row: Riga del DataFrame con gli indicatori
        
        Returns:
            dict con tp e sl
        """
        atr = df_row['atr']
        fib_ext = df_row['fib_ext_123']
        volatility = df_row['volatility_current']
        
        # Usa ATR + Fibonacci per calcolare livelli dinamici
        if signal == 1:  # LONG
            tp_atr = entry_price + (atr * 2.5)  # Più aggressivo con ATR
            tp_fib = fib_ext * 1.005  # 0.5% dalla Fib extension
            tp = max(tp_atr, tp_fib)
            
            sl = entry_price - atr  # Stop Loss conservativo
            
        else:  # SHORT
            tp_atr = entry_price - (atr * 2.5)
            tp_fib = fib_ext * 0.995
            tp = min(tp_atr, tp_fib)
            
            sl = entry_price + atr
        
        return {
            'tp': tp,
            'sl': sl,
            'entry': entry_price,
            'atr': atr
        }
    
    def get_signal_description(self, df_row):
        """Ritorna descrizione testuale del segnale"""
        reasons = []
        
        if df_row['ema_fast'] > df_row['ema_slow']:
            reasons.append("EMA↑")
        if df_row['rsi'] > 60:
            reasons.append("RSI↑")
        if df_row['macd'] > df_row['macd_signal']:
            reasons.append("MACD↑")
        if df_row['kdj_k'] > df_row['kdj_d']:
            reasons.append("KDJ↑")
        if df_row['obv_momentum'] > 0:
            reasons.append("OBV↑")
        if df_row['force_index'] > df_row['force_index_ema']:
            reasons.append("FI↑")
        if df_row['volume_ratio'] > 1.3:
            reasons.append("VOL↑")
        
        return " | ".join(reasons) if reasons else "No signal"
