"""
Advanced Configuration File for Scalper Strategy
Contiene tutti i parametri configurabili per la strategia avanzata
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============ BITGET API CONFIGURATION ============
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSWORD = os.getenv('BITGET_PASSWORD')

# ============ TRADING CONFIGURATION ============
SYMBOL = os.getenv('SYMBOL', 'XRPUSDT')
TIMEFRAME = '1m'  # 1 minute candles
LEVERAGE = int(os.getenv('LEVERAGE', 5))
MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', 0.1))
RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.02))  # 2% per trade
MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 0.05))  # 5% max daily loss

# ============ MODE ============
TRADING_MODE = os.getenv('TRADING_MODE', 'backtest')  # 'backtest' or 'live'

# ============ BACKTEST CONFIGURATION ============
BACKTEST_START_DATE = '2024-01-01'
BACKTEST_END_DATE = '2024-12-31'
INITIAL_BALANCE = 1000  # USDT

# ============ ADVANCED STRATEGY PARAMETERS ============

# --- EMA (Exponential Moving Average) ---
EMA_FAST = 5
EMA_MEDIUM = 13
EMA_SLOW = 50
SMA_PERIOD = 50

# --- RSI (Relative Strength Index) ---
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# --- KDJ / STOCHASTIC ---
KDJ_PERIOD = 9
KDJ_SMOOTH = 3
KDJ_OVERBOUGHT = 80
KDJ_OVERSOLD = 20

# --- BOLLINGER BANDS ---
BB_PERIOD = 20
BB_STD_DEV = 2

# --- MACD (Moving Average Convergence Divergence) ---
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# --- ATR (Average True Range) ---
ATR_PERIOD = 14

# --- VOLATILITY ---
VOLATILITY_PERIOD = 20
CURRENT_VOLATILITY_PERIOD = 5

# --- MOMENTUM ---
MOMENTUM_PERIOD = 10

# --- SAR (Parabolic SAR) ---
SAR_AF_START = 0.02  # Acceleration Factor initial
SAR_AF_MAX = 0.2     # Acceleration Factor maximum

# --- PIVOT POINTS ---
PIVOT_PERIOD = 20

# --- FIBONACCI ---
FIB_LOOKBACK = 50

# --- ADX (Average Directional Index) ---
ADX_PERIOD = 14
ADX_TREND_THRESHOLD = 25  # Solo trade su trend forti

# --- TRIX (Triple Exponential Moving Average) ---
TRIX_PERIOD = 15

# --- VOLUME INDICATORS ---
VOLUME_MA_PERIOD = 20
VOLUME_RATIO_THRESHOLD = 1.3  # Volume deve essere > media * questo valore

# --- OBV (On-Balance Volume) ---
OBV_MA_PERIOD = 20

# --- ADL (Accumulation/Distribution Line) ---
ADL_MA_PERIOD = 20

# ============ SIGNAL GENERATION THRESHOLDS ============

# Soglie di score per i segnali
LONG_SIGNAL_THRESHOLD = 0.35
SHORT_SIGNAL_THRESHOLD = -0.35
MIN_SIGNAL_STRENGTH = 0.35

# ============ INDICATOR WEIGHTS (pesi nel sistema di scoring) ============
# Questi devono sommare a 1.0

WEIGHT_EMA = 0.12
WEIGHT_RSI = 0.12
WEIGHT_KDJ = 0.12
WEIGHT_BB = 0.12
WEIGHT_MACD = 0.10
WEIGHT_VOLUME = 0.10
WEIGHT_ADL = 0.08
WEIGHT_MOMENTUM = 0.08
WEIGHT_SAR = 0.05
WEIGHT_ADX = 0.05
WEIGHT_TSI = 0.03
WEIGHT_FEAR_GREED = 0.03

# Verifica che i pesi sommino a 1
TOTAL_WEIGHT = (WEIGHT_EMA + WEIGHT_RSI + WEIGHT_KDJ + WEIGHT_BB + 
                WEIGHT_MACD + WEIGHT_VOLUME + WEIGHT_ADL + WEIGHT_MOMENTUM + 
                WEIGHT_SAR + WEIGHT_ADX + WEIGHT_TSI + WEIGHT_FEAR_GREED)

assert 0.99 <= TOTAL_WEIGHT <= 1.01, f"Pesi non normalizzati: {TOTAL_WEIGHT}"

# ============ DYNAMIC TP/SL CONFIGURATION ============

# Moltiplicatori ATR per Take Profit e Stop Loss
TP_ATR_MULTIPLIER = 2.5  # TP a 2.5x ATR
SL_ATR_MULTIPLIER = 1.0  # SL a 1x ATR

# Use Fibonacci per TP/SL
USE_FIBONACCI_TP = True
USE_PIVOT_SL = True

# ============ FEAR & GREED INDEX ============

# Pesi per il calcolo del Fear & Greed
FG_RSI_WEIGHT = 0.35
FG_VOLUME_WEIGHT = 0.35
FG_MOMENTUM_WEIGHT = 0.30

# ============ DAILY TREND FILTER ============

DAILY_MA_PERIOD = 50
DAILY_TREND_THRESHOLD = 0.002  # 0.2%

# ============ LOGGING ============

LOG_FILE = 'trading.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# ============ DATABASE / CSV OUTPUT ============

RESULTS_DIR = '.'
TRADES_CSV = 'advanced_backtest_results.csv'
INDICATORS_CSV = 'advanced_backtest_indicators.csv'

# ============ BACKTEST OUTPUT ============

EXPORT_CHARTS = True
CHART_DPI = 100
CHART_STYLE = 'seaborn'  # 'seaborn', 'ggplot', 'bmh'

# ============ ADVANCED FEATURES ============

# Optimization
OPTIMIZATION_ENABLED = False
OPTIMIZATION_METHOD = 'bayesian'  # 'grid', 'random', 'bayesian'
OPTIMIZATION_JOBS = 4

# Use GPU (se disponibile)
USE_GPU = False

# Multi-timeframe analysis (usa dati da timeframe superiori come filtro)
USE_MULTI_TIMEFRAME = True
SECONDARY_TIMEFRAME = '5m'

# ============ SAFETY PARAMETERS ============

# Max trades per day
MAX_TRADES_PER_DAY = 100

# Min time between trades (secondi)
MIN_TIME_BETWEEN_TRADES = 0

# Max consecutive losses before stopping
MAX_CONSECUTIVE_LOSSES = 5

# Disable trading during (ore UTC)
DISABLE_TRADING_HOURS = []  # Es: [0, 1, 2] per disabilitare 00:00-02:59

# ============ PRINT CONFIGURATION ============

VERBOSE = True  # Stampa messaggi dettagliati
PRINT_SIGNAL_COMPONENTS = True  # Stampa i componenti del score
PRINT_TRADE_DETAILS = True  # Stampa dettagli di ogni trade
