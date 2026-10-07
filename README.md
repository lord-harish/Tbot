# Tbot - Forex Chart Analysis AI

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Pro-4285F4?style=flat-square&logo=google)](https://makersuite.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A Python desktop and web application that uses **Google Gemini AI** to analyze forex charts and predict market movement scenarios.

### 🚀 **[Try the Live App Now](https://lord-harish-tbot.streamlit.app)** | 📖 **[View on GitHub](https://github.com/lord-harish/Tbot)**

</div>

---

## ✨ Core Features

- 📊 **Upload forex chart images** - Support for all formats
- 🤖 **AI-powered analysis** using Google Gemini Pro
- 📈 **Technical pattern recognition** - Candlesticks, trends, structures
- 🎯 **Market movement predictions** - UP, DOWN, or CONSOLIDATION
- 💾 **Analysis history database** - Track all your analyses
- 🔍 **Support/Resistance detection** - Key price levels
- 📍 **Supply/Demand zones** - Liquidity identification
- 🕯️ **Candlestick patterns** - Engulfing, Pinbar, Doji, Hammer

---

## 📊 Supported Analysis

The bot analyzes:

| Analysis Type | Details |
|---|---|
| **Market Structure** | Trend direction, Higher Highs/Lows |
| **Support & Resistance** | Key price levels |
| **Supply & Demand Zones** | Liquidity pools and rejection areas |
| **Break of Structure (BOS)** | Pattern changes |
| **Candlestick Patterns** | Engulfing, Pinbar, Doji, Hammer |
| **Trend Bias & Momentum** | Strength and direction |
| **Price Predictions** | Next few hours movement with targets |

---

## 💱 Supported Pairs & Timeframes

### Pairs
```
XAUUSD (Gold) | EURUSD | GBPUSD | USDJPY | USDCHF | AUDUSD | NZDUSD | USDCAD
```

### Timeframes
```
1m | 5m | 15m | 30m | 1h | 4h | 1D | 1W
```

---

## 🎯 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini Pro API Key (Free tier available)

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/lord-harish/Tbot.git
cd forex_bot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements-desktop.txt

# 4. Get API key from: https://makersuite.google.com/app/apikey

# 5. Create .env file
Copy .env.example to .env
Add: GEMINI_API_KEY=your_key_here

# 6. Run the app
.\run.bat
```

---

## 🌐 Deploy Online (Easiest Way)

Use **Streamlit Community Cloud** for instant deployment:

1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Create app → Select your repo
5. Main file: `streamlit_app.py`
6. Add secret: `GEMINI_API_KEY = "your_key"`
7. Deploy! 🎉

**Live at:** https://lord-harish-tbot.streamlit.app

---

## 📱 Usage Guide

1. **Select Forex Pair** - EURUSD, GBPUSD, etc.
2. **Select Timeframe** - 1h, 4h, 1D, etc.
3. **Upload Chart Image** - PNG, JPG, GIF, BMP, WebP
4. **Click Analyze** - 🚀 Let AI work its magic
5. **View Results** - Prediction, targets, analysis
6. **Check History** - All past analyses saved

---

## 📤 Output & Results

The bot provides:

```
✅ Predicted Direction     → UP | DOWN | CONSOLIDATION
📊 Confidence Level        → 0-100%
🎯 Price Targets           → Entry, Take Profit, Stop Loss
📍 Support Levels          → Identified areas
📈 Resistance Levels       → Identified areas
🔍 Pattern Analysis        → Candlestick patterns found
💡 Detailed Reasoning      → Full technical analysis
```

---

## 🗂️ Project Structure

```
forex_bot/
├── main.py                    # Desktop entry point
├── streamlit_app.py           # Web entry point
├── config.py                  # Configuration
├── requirements.txt           # Web dependencies
├── requirements-desktop.txt   # Desktop dependencies
├── .env.example               # Environment template
│
├── ui/
│   └── main_window.py         # PyQt6 GUI (desktop)
│
├── analysis/
│   ├── gemini_analyzer.py     # Gemini Pro integration
│   └── technical_analyzer.py  # Technical analysis logic
│
├── database/
│   └── db_manager.py          # SQLite database manager
│
└── utils/
    └── logger.py              # Logging utility
```

---

## 🔑 API Configuration

### Google Gemini Pro (Required)
- **Get key:** https://makersuite.google.com/app/apikey
- **Free tier:** Generous limits
- **Add to .env:** `GEMINI_API_KEY=your_key`

### TradingView (Optional)
- For future real-time data integration

---

## ⚠️ Important Notes

- **Not Financial Advice** - Use at your own risk
- **Always use risk management** - Never risk more than you can afford
- **Chart quality matters** - Clear charts = better analysis
- **Do your own research** - AI is a tool, not a guarantee
- **Past performance ≠ Future results**

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"GEMINI_API_KEY not found"** | Check `.env` file exists, verify API key is correct |
| **Image upload fails** | Ensure image < 10MB, supported format (JPG, PNG, GIF, BMP, WebP) |
| **Slow analysis** | First run is slower, check internet connection |
| **App won't start** | Verify all dependencies installed: `pip install -r requirements-desktop.txt` |

---

## 🚀 Future Enhancements

- 🔄 Real-time price tracking
- 📱 Mobile app version
- 🤖 Machine learning pattern recognition
- 📊 TradingView integration
- ⏰ Scheduled alerts
- 📈 Backtesting engine
- 💼 Portfolio tracking
- 🌍 Multi-language support

---

## 📞 Support & Issues

- Check `logs/` directory for errors
- Verify API key is active and valid
- Ensure all dependencies are installed
- [Create an Issue](https://github.com/lord-harish/Tbot/issues) for bugs

---

## 📄 License

MIT License - Feel free to use, modify, and distribute

---

<div align="center">

### 🎯 Ready to Analyze? 

### **[Launch Tbot Now](https://lord-harish-tbot.streamlit.app)** 🚀

### Made with ❤️ by [lord-harish](https://github.com/lord-harish)

</div>
