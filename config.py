import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
TRADINGVIEW_API_KEY = os.getenv('TRADINGVIEW_API_KEY', '')

# Application Configuration
APP_TITLE = "Forex Trading Bot - AI Chart Analyzer"
APP_VERSION = "1.0.0"
APP_WIDTH = 1400
APP_HEIGHT = 900

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'forex_analysis.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Supported Forex Pairs
FOREX_PAIRS = [
    'XAUUSD',  # Gold
    'EURUSD',  # Euro/USD
    'GBPUSD',  # British Pound/USD
    'USDJPY',  # USD/Japanese Yen
    'USDCHF',  # USD/Swiss Franc
    'AUDUSD',  # Australian Dollar/USD
    'NZDUSD',  # New Zealand Dollar/USD
    'USDCAD',  # USD/Canadian Dollar
]

# Chart Timeframes
TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W']

# Analysis Settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']

# Gemini Model Configuration
# Use the current stable Flash model for chart-image analysis by default.
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

# Economic Calendar Configuration
ECONOMIC_CALENDAR_ENABLED = os.getenv('ECONOMIC_CALENDAR_ENABLED', 'true').lower() == 'true'
ECONOMIC_CALENDAR_URL = os.getenv(
    'ECONOMIC_CALENDAR_URL',
    'https://nfs.faireconomy.media/ff_calendar_thisweek.json'
)
ECONOMIC_CALENDAR_TIMEOUT = int(os.getenv('ECONOMIC_CALENDAR_TIMEOUT', '10'))
ECONOMIC_CALENDAR_LOOKBACK_HOURS = int(os.getenv('ECONOMIC_CALENDAR_LOOKBACK_HOURS', '12'))
ECONOMIC_CALENDAR_LOOKAHEAD_HOURS = int(os.getenv('ECONOMIC_CALENDAR_LOOKAHEAD_HOURS', '72'))
ECONOMIC_CALENDAR_MAX_EVENTS = int(os.getenv('ECONOMIC_CALENDAR_MAX_EVENTS', '12'))
