"""
Advanced Scalper Strategy con 16+ indicatori tecnici
Per scalping su timeframe 1m
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, SMAIndicator, ADXIndicator, TRIXIndicator, MACD
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, AccDistIndexIndicator
import config

class AdvancedScalperStrategy:
    """Strategia di scalping avanzata con 16+ indicatori"""
    
    def __init__(self):
        # EMA Parameters
        self.ema_fast = 5
        self.ema_medium = 13
        self.ema_slow = 50
        
        # RSI Parameters
        self.rsi_period = 14
        self.rsi_overbought = 70
        self.rsi_oversold = 30
        
        # KDJ (Stochastic)
        self.kdj_period = 9
        self.kdj_smooth = 3
        
        # Bollinger Bands
        self.bb_period = 20
        self.bb_std = 2
        
        # MACD
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        
        # ATR
        self.atr_period = 14
        
        # Volatility
        self.volatility_period = 20
        
        # Momentum
        self.momentum_period = 10
        
        # Pivot Points
        self.pivot_period = 20
        
        # OBV parameters
        self.obv_ma_period = 20
        
    def calculate_all_indicators(self, df):
        """Calcola tutti gli indicatori tecnici"""
        
        # ============ MOVING AVERAGES ============
        df['ema_fast'] = EMAIndicator(close=df['close'], window=self.ema_fast).ema_indicator()
        df['ema_medium'] = EMAIndicator(close=df['close'], window=self.ema_medium).ema_indicator()
        df['ema_slow'] = EMAIndicator(close=df['close'], window=self.ema_slow).ema_indicator()
        df['sma_50'] = SMAIndicator(close=df['close'], window=50).sma_indicator()
        
        # ============ RSI (Overbought/Oversold) ============
        df['rsi'] = RSIIndicator(close=df['close'], window=self.rsi_period).rsi()
        
        # ============ STOCHASTIC OSCILLATOR (KDJ) ============
        stoch = StochasticOscillator(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=self.kdj_period,
            smooth_window=self.kdj_smooth
        )
        df['kdj_k'] = stoch.stoch()
        df['kdj_d'] = stoch.stoch_signal()
        df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
        
        # ============ BOLLINGER BANDS ============
        bb = BollingerBands(
            close=df['close'],
            window=self.bb_period,
            window_dev=self.bb_std
        )
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # ============ MACD ============
        macd = MACD(close=df['close'], window_fast=self.macd_fast, 
                    window_slow=self.macd_slow, window_sign=self.macd_signal)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        
        # ============ ATR (Volatility) ============
        df['atr'] = AverageTrueRange(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=self.atr_period
        ).average_true_range()
        
        # ============ VOLATILITY (Historical & Current) ============
        df['volatility_hist'] = df['close'].pct_change().rolling(window=self.volatility_period).std() * 100
        df['volatility_current'] = df['close'].pct_change().rolling(window=5).std() * 100
        
        # ============ VOLUME INDICATORS ============
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # On-Balance Volume (OBV)
        df['obv'] = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume']).on_balance_volume()
        df['obv_ma'] = df['obv'].rolling(window=self.obv_ma_period).mean()
        df['obv_signal'] = (df['obv'] - df['obv_ma']).fillna(0)
        
        # Accumulation/Distribution Line (ADL)
        df['adl'] = AccDistIndexIndicator(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            volume=df['volume']
        ).acc_dist_index()
        df['adl_ma'] = df['adl'].rolling(window=self.obv_ma_period).mean()
        
        # ============ MOMENTUM ============
        df['momentum'] = df['close'].diff(self.momentum_period)
        df['momentum_ma'] = df['momentum'].rolling(window=5).mean()
        df['momentum_signal'] = np.where(df['momentum'] > df['momentum_ma'], 1, -1)
        
        # ============ PIVOT POINTS ============
        self._calculate_pivot_points(df)
        
        # ============ SAR (Parabolic SAR) ============
        self._calculate_sar(df)
        
        # ============ FIBONACCI EXTENSIONS ============
        self._calculate_fibonacci_levels(df)
        
        # ============ TREND STRENGTH INDEX (TSI) ============
        self._calculate_tsi(df)
        
        # ============ ADX (Trend Strength) ============
        adx = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['adx'] = adx.adx()
        df['di_plus'] = adx.adx_pos()
        df['di_minus'] = adx.adx_neg()
        
        # ============ TRIX (Triple Exponential Moving Average) ============
        df['trix'] = TRIXIndicator(close=df['close'], window=15).trix()
        
        # ============ FEAR & GREED INDEX (Basato su RSI e Volume) ============
        self._calculate_fear_greed(df)
        
        return df
    
    def _calculate_pivot_points(self, df):
        """Calcola i Pivot Points (S3, S2, S1, P, R1, R2, R3)"""
        df['pivot'] = (df['high'].rolling(self.pivot_period).max() + 
                       df['low'].rolling(self.pivot_period).min() + 
                       df['close']) / 3
        
        df['resistance_1'] = (2 * df['pivot']) - df['low'].rolling(self.pivot_period).min()
        df['support_1'] = (2 * df['pivot']) - df['high'].rolling(self.pivot_period).max()
        
        df['resistance_2'] = df['pivot'] + (df['high'].rolling(self.pivot_period).max() - 
                                             df['low'].rolling(self.pivot_period).min())
        df['support_2'] = df['pivot'] - (df['high'].rolling(self.pivot_period).max() - 
                                          df['low'].rolling(self.pivot_period).min())
        
        df['resistance_3'] = df['resistance_2'] + (df['high'].rolling(self.pivot_period).max() - 
                                                    df['low'].rolling(self.pivot_period).min())
        df['support_3'] = df['support_2'] - (df['high'].rolling(self.pivot_period).max() - 
                                              df['low'].rolling(self.pivot_period).min())
    
    def _calculate_sar(self, df):
        """Calcola il Parabolic SAR"""
        length = len(df)
        sar = [0] * length
        af = 0.02
        max_af = 0.2
        
        # Inizializzazione
        is_long = True
        hp = df['high'].iloc[0]
        lp = df['low'].iloc[0]
        sar[0] = df['low'].iloc[0]
        
        for i in range(1, length):
            if is_long:
                sar[i] = sar[i-1] + af * (hp - sar[i-1])
                sar[i] = min(sar[i], df['low'].iloc[i-1:i+1].min())
                
                if df['high'].iloc[i] > hp:
                    hp = df['high'].iloc[i]
                    af = min(af + 0.02, max_af)
                
                if df['low'].iloc[i] < sar[i]:
                    is_long = False
                    sar[i] = hp
                    lp = df['low'].iloc[i]
                    af = 0.02
            else:
                sar[i] = sar[i-1] - af * (sar[i-1] - lp)
                sar[i] = max(sar[i], df['high'].iloc[i-1:i+1].max())
                
                if df['low'].iloc[i] < lp:
                    lp = df['low'].iloc[i]
                    af = min(af + 0.02, max_af)
                
                if df['high'].iloc[i] > sar[i]:
                    is_long = True
                    sar[i] = lp
                    hp = df['high'].iloc[i]
                    af = 0.02
        
        df['sar'] = sar
        df['sar_signal'] = np.where(df['close'] > df['sar'], 1, -1)
    
    def _calculate_fibonacci_levels(self, df):
        """Calcola i livelli di Fibonacci (retracement e extension)"""
        # Ultimi 50 candle
        window = min(50, len(df))
        high = df['high'].tail(window).max()
        low = df['low'].tail(window).min()
        diff = high - low
        
        # Fibonacci Ratios
        df['fib_0'] = low
        df['fib_23.6'] = high - (diff * 0.236)
        df['fib_38.2'] = high - (diff * 0.382)
        df['fib_50'] = high - (diff * 0.5)
        df['fib_61.8'] = high - (diff * 0.618)
        df['fib_100'] = high
        
        # Extensions
        df['fib_ext_138.2'] = low - (diff * 0.382)
        df['fib_ext_161.8'] = low - (diff * 0.618)
        df['fib_ext_200'] = low - diff
    
    def _calculate_tsi(self, df):
        """Calcola il Trend Strength Index (TSI)"""
        # TSI basato su momentum
        momentum = df['close'].diff()
        
        # Prima EMA
        ema1 = momentum.ewm(span=25, adjust=False).mean()
        # Seconda EMA
        ema2 = ema1.ewm(span=13, adjust=False).mean()
        
        # EMA del valore assoluto
        abs_ema1 = np.abs(momentum).ewm(span=25, adjust=False).mean()
        abs_ema2 = abs_ema1.ewm(span=13, adjust=False).mean()
        
        df['tsi'] = (ema2 / abs_ema2 * 100).fillna(0)
        df['tsi_signal'] = df['tsi'].ewm(span=7, adjust=False).mean()
    
    def _calculate_fear_greed(self, df):
        """Calcola un Fear & Greed Index semplificato"""
        # Basato su: RSI, Volume, Momentum
        rsi_score = (df['rsi'] - 30) / 40  # 0-1 score
        
        # Volume score
        volume_score = np.minimum(df['volume_ratio'], 2) / 2  # Cap a 1
        
        # Momentum score
        momentum_score = (df['momentum'] / df['momentum'].abs().rolling(10).max()).fillna(0)
        momentum_score = (momentum_score + 1) / 2  # Normalizza a 0-1
        
        # Media ponderata
        df['fear_greed'] = (rsi_score * 0.35 + volume_score * 0.35 + momentum_score * 0.3) * 100
        
        # Classificazione
        df['fear_greed_level'] = pd.cut(df['fear_greed'], 
                                         bins=[0, 25, 50, 75, 100],
                                         labels=['Fear', 'Neutral', 'Greed', 'Euphoria'],
                                         include_lowest=True)
    
    def generate_signals(self, df):
        """
        Genera segnali di trading basati su tutti gli indicatori.
        Ritorna -1 (Short), 0 (Hold), 1 (Long)
        """
        signals = pd.Series(0, index=df.index)
        scores = pd.DataFrame(index=df.index)
        
        # ============ SCORING SYSTEM ============
        # Ogni indicatore contribuisce a un score da -1 a 1
        
        # 1. EMA Alignment (0.15 weight)
        ema_score = np.where(
            (df['ema_fast'] > df['ema_medium']) & (df['ema_medium'] > df['ema_slow']), 1,
            np.where(
                (df['ema_fast'] < df['ema_medium']) & (df['ema_medium'] < df['ema_slow']), -1,
                0
            )
        )
        scores['ema_score'] = ema_score * 0.15
        
        # 2. RSI (0.12 weight)
        rsi_score = np.where(
            df['rsi'] > self.rsi_overbought, -1,
            np.where(
                df['rsi'] < self.rsi_oversold, 1,
                np.where(df['rsi'] > 60, -0.5, np.where(df['rsi'] < 40, 0.5, 0))
            )
        )
        scores['rsi_score'] = rsi_score * 0.12
        
        # 3. KDJ (0.12 weight)
        kdj_score = np.where(
            df['kdj_k'] > 80, -1,
            np.where(
                df['kdj_k'] < 20, 1,
                np.where(
                    df['kdj_k'] > df['kdj_d'], 0.5,
                    np.where(df['kdj_k'] < df['kdj_d'], -0.5, 0)
                )
            )
        )
        scores['kdj_score'] = kdj_score * 0.12
        
        # 4. Bollinger Bands (0.12 weight)
        bb_score = np.where(
            df['close'] > df['bb_upper'], -1,
            np.where(
                df['close'] < df['bb_lower'], 1,
                np.where(df['bb_position'] > 0.8, -0.5, np.where(df['bb_position'] < 0.2, 0.5, 0))
            )
        )
        scores['bb_score'] = bb_score * 0.12
        
        # 5. MACD (0.12 weight)
        macd_score = np.where(
            df['macd'] > df['macd_signal'], 1,
            np.where(
                df['macd'] < df['macd_signal'], -1,
                np.where(df['macd_diff'] > 0, 0.5, -0.5)
            )
        )
        scores['macd_score'] = macd_score * 0.12
        
        # 6. Volume & OBV (0.12 weight)
        obv_score = np.where(
            df['obv'] > df['obv_ma'], 1,
            np.where(
                df['obv'] < df['obv_ma'], -1,
                0
            )
        )
        volume_score = np.where(df['volume_ratio'] > 1.3, 0.5, np.where(df['volume_ratio'] < 0.7, -0.5, 0))
        scores['volume_score'] = (obv_score * 0.7 + volume_score * 0.3) * 0.12
        
        # 7. ADL (0.08 weight)
        adl_score = np.where(
            df['adl'] > df['adl_ma'], 1,
            np.where(
                df['adl'] < df['adl_ma'], -1,
                0
            )
        )
        scores['adl_score'] = adl_score * 0.08
        
        # 8. Momentum (0.08 weight)
        momentum_score = np.where(
            df['momentum'] > df['momentum_ma'], 1,
            np.where(
                df['momentum'] < df['momentum_ma'], -1,
                0
            )
        )
        scores['momentum_score'] = momentum_score * 0.08
        
        # 9. SAR (0.05 weight)
        scores['sar_score'] = df['sar_signal'] * 0.05
        
        # 10. ADX (0.05 weight) - Solo su trend forti
        adx_score = np.where(
            df['adx'] > 25,
            np.where(df['di_plus'] > df['di_minus'], 1, -1),
            0
        )
        scores['adx_score'] = adx_score * 0.05
        
        # 11. TSI (0.03 weight)
        tsi_score = np.where(
            df['tsi'] > df['tsi_signal'], 1,
            np.where(
                df['tsi'] < df['tsi_signal'], -1,
                0
            )
        )
        scores['tsi_score'] = tsi_score * 0.03
        
        # 12. Fear & Greed (0.03 weight)
        fg_score = (df['fear_greed'] - 50) / 50  # Normalizza a -1 a 1
        scores['fg_score'] = fg_score * 0.03
        
        # Somma tutti gli score
        total_score = scores.sum(axis=1)
        df['total_score'] = total_score
        df['score_components'] = scores
        
        # ============ SIGNAL GENERATION ============
        # Soglie di segnale
        long_threshold = 0.35
        short_threshold = -0.35
        
        signals = np.where(
            total_score > long_threshold, 1,
            np.where(
                total_score < short_threshold, -1,
                0
            )
        )
        
        df['signal'] = signals
        df['signal_strength'] = total_score.abs()
        
        return df
    
    def calculate_dynamic_tp_sl(self, entry_price, signal, df_current, lookback=50):
        """
        Calcola Take Profit e Stop Loss dinamici basati su:
        - ATR
        - Fibonacci Levels
        - Pivot Points
        """
        if len(df_current) < 5:
            # Fallback: base su ATR medio
            atr = df_current['atr'].iloc[-1] if 'atr' in df_current else entry_price * 0.005
            if signal == 1:
                return {
                    'tp': entry_price + (atr * 2.5),
                    'sl': entry_price - (atr * 1)
                }
            else:
                return {
                    'tp': entry_price - (atr * 2.5),
                    'sl': entry_price + (atr * 1)
                }
        
        recent_df = df_current.tail(lookback)
        current_atr = df_current['atr'].iloc[-1]
        
        if signal == 1:  # LONG
            # TP basato su: ATR + Fibonacci extension
            tp_atr = entry_price + (current_atr * 2.5)
            tp_fib = recent_df['fib_ext_161.8'].iloc[-1]
            tp = max(tp_atr, tp_fib) if tp_fib > entry_price else tp_atr
            
            # SL basato su: ATR + Support
            sl_atr = entry_price - (current_atr * 1)
            sl_support = recent_df['support_1'].iloc[-1]
            sl = min(sl_atr, sl_support) if sl_support < entry_price else sl_atr
        else:  # SHORT
            # TP basato su: ATR + Fibonacci extension
            tp_atr = entry_price - (current_atr * 2.5)
            tp_fib = recent_df['fib_ext_161.8'].iloc[-1]
            tp = min(tp_atr, tp_fib) if tp_fib < entry_price else tp_atr
            
            # SL basato su: ATR + Resistance
            sl_atr = entry_price + (current_atr * 1)
            sl_resistance = recent_df['resistance_1'].iloc[-1]
            sl = max(sl_atr, sl_resistance) if sl_resistance > entry_price else sl_atr
        
        return {
            'tp': tp,
            'sl': sl,
            'entry': entry_price,
            'atr': current_atr
        }
    
    def get_signal_explanation(self, df, idx):
        """Ritorna una spiegazione del segnale generato"""
        row = df.iloc[idx]
        components = row.get('score_components', {})
        
        explanation = {
            'price': row['close'],
            'signal': row['signal'],
            'strength': row['signal_strength'],
            'components': {
                'EMA': components.get('ema_score', 0) / 0.15 if 'ema_score' in components else 0,
                'RSI': components.get('rsi_score', 0) / 0.12 if 'rsi_score' in components else 0,
                'KDJ': components.get('kdj_score', 0) / 0.12 if 'kdj_score' in components else 0,
                'BB': components.get('bb_score', 0) / 0.12 if 'bb_score' in components else 0,
                'MACD': components.get('macd_score', 0) / 0.12 if 'macd_score' in components else 0,
                'Volume/OBV': components.get('volume_score', 0) / 0.12 if 'volume_score' in components else 0,
                'ADL': components.get('adl_score', 0) / 0.08 if 'adl_score' in components else 0,
                'Momentum': components.get('momentum_score', 0) / 0.08 if 'momentum_score' in components else 0,
            },
            'volatility': row.get('volatility_current', 0),
            'fear_greed': row.get('fear_greed_level', 'N/A'),
        }
        
        return explanation
