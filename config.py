import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSWORD = os.getenv('BITGET_PASSWORD')

# Trading Configuration
SYMBOL = os.getenv('SYMBOL', 'XRPUSDT')
TIMEFRAME = '1m'  # 1 minute candles
LEVERAGE = int(os.getenv('LEVERAGE', 5))
MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', 0.1))
RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.02))  # 2% per trade
MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 0.05))  # 5% max daily loss

# Mode
TRADING_MODE = os.getenv('TRADING_MODE', 'backtest')  # 'backtest' or 'live'

# Backtest Configuration
BACKTEST_START_DATE = '2024-01-01'
BACKTEST_END_DATE = '2024-12-31'
INITIAL_BALANCE = 1000  # USDT

# Strategy Parameters
MA_FAST = 5
MA_SLOW = 20
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MIN_VOLUME_RATIO = 1.5  # Volume deve essere 1.5x la media

# Daily Trend Filter
DAILY_MA_PERIOD = 50
