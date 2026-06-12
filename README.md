# Forex Trading Bot - AI Chart Analyzer

A Python desktop application that uses Google Gemini Pro AI to analyze forex charts and predict market movements.

## Features

✨ **Core Features:**
- 📊 Upload forex chart images
- 🤖 AI-powered analysis using Google Gemini Pro
- 📈 Technical pattern recognition
- 🎯 Market movement predictions
- 💾 Analysis history database
- 🔍 Support/Resistance detection
- 📍 Supply/Demand zone identification
- 🕯️ Candlestick pattern analysis

## Supported Analysis

The bot analyzes:
- **Market Structure** - Trend direction, Higher Highs/Lows
- **Support & Resistance** - Key price levels
- **Supply & Demand Zones** - Liquidity pools and rejection areas
- **Break of Structure (BOS)** - Pattern changes
- **Candlestick Patterns** - Engulfing, Pinbar, Doji, Hammer
- **Trend Bias & Momentum** - Strength and direction
- **Price Predictions** - Next few hours movement with targets

## Supported Pairs

- XAUUSD (Gold)
- EURUSD
- GBPUSD
- USDJPY
- USDCHF
- AUDUSD
- NZDUSD
- USDCAD

## Timeframes

1m, 5m, 15m, 30m, 1h, 4h, 1D, 1W

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini Pro API Key (Free tier available)

### Step 1: Clone/Download
```bash
git clone <your-repository-url>
cd forex_bot
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup API Key
1. Get your free Gemini Pro API key from: https://makersuite.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Step 5: Run Application
```powershell
.\run.bat
```

Or run with the project virtual environment directly:
```powershell
.\venv\Scripts\python.exe main.py
```

### Run the Web App Locally
For the mobile-friendly browser version:
```powershell
.\run_web.bat
```

Or run with the project virtual environment directly:
```powershell
.\venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal.

## Deploy Online From GitHub

The easiest way to use this from your phone is Streamlit Community Cloud:

1. Push this project to GitHub.
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Click **Create app**.
4. Select your repository and branch.
5. Set the main file path to:
   ```text
   streamlit_app.py
   ```
6. Add this secret in the app settings:
   ```toml
   GEMINI_API_KEY = "your_real_gemini_key_here"
   ```
7. Deploy the app and open the Streamlit URL on your mobile browser.

Do not commit your `.env` file or real API key to GitHub.

## Usage

1. **Select Forex Pair** - Choose from the dropdown (EURUSD, GBPUSD, etc.)
2. **Select Timeframe** - Choose analysis timeframe (1h, 4h, 1D, etc.)
3. **Upload Chart Image** - Click "Browse Chart Image" and select your chart
4. **Analyze** - Click "🚀 Analyze Chart"
5. **View Results** - See prediction, support/resistance levels, and detailed analysis
6. **History** - Check past analyses in the History tab

## Output

The bot provides:
- ✅ **Predicted Direction** - UP, DOWN, or CONSOLIDATION
- 📊 **Confidence Level** - Percentage certainty (0-100%)
- 🎯 **Price Targets** - Expected price levels
- 📍 **Support Levels** - Identified support areas
- 📈 **Resistance Levels** - Identified resistance areas
- 🔍 **Pattern Analysis** - Identified candlestick patterns
- 💡 **Detailed Reasoning** - Full technical analysis

## Database

All analyses are stored locally in SQLite:
- `data/forex_analysis.db` - Contains analysis history
- Can be queried for pattern statistics and backtesting

## File Structure

```
forex_bot/
├── main.py                    # Entry point
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
├── README.md                  # This file
├── ui/
│   └── main_window.py         # PyQt6 GUI
├── analysis/
│   ├── gemini_analyzer.py     # Gemini Pro integration
│   └── technical_analyzer.py  # Technical analysis
├── database/
│   └── db_manager.py          # SQLite database
└── utils/
    └── logger.py              # Logging utility
```

## API Keys

### Google Gemini Pro (Required)
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Add to `.env` file as `GEMINI_API_KEY`
4. Free tier includes generous limits

### TradingView (Optional)
- For real-time data integration (future feature)
- Add to `.env` if available

## Limitations

- Chart analysis depends on image quality
- AI predictions are not guaranteed; use with caution
- For trading, always use proper risk management
- Not financial advice - trade at your own risk

## Troubleshooting

**"GEMINI_API_KEY not found"**
- Make sure `.env` file exists in the project directory
- Check API key is correct in `.env`
- Restart the application

**Image upload fails**
- Ensure image is < 10MB
- Supported formats: JPG, PNG, GIF, BMP, WebP
- Try a different chart image

**Slow analysis**
- First run may take longer
- Gemini Pro takes time for complex analysis
- Check internet connection

## Future Enhancements

- 🔄 Real-time price tracking
- 📱 Mobile app version
- 🤖 Machine learning pattern recognition
- 📊 TradingView integration
- ⏰ Scheduled alerts
- 📈 Backtesting engine
- 💼 Portfolio tracking

## Disclaimer

⚠️ **DISCLAIMER**
- This tool is for educational purposes
- Not financial advice
- Always do your own research
- Use proper risk management
- Forex trading involves significant risk
- Past performance ≠ future results

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Verify API key is active
3. Ensure all dependencies are installed

## License

MIT License - Feel free to modify and distribute

---

**Happy Trading! 🚀📈**
