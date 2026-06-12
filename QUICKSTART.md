# 🚀 GETTING STARTED GUIDE - Forex Trading Bot

## ⚡ Quick Setup (5 minutes)

### Step 1: Run Setup Script
**Windows:**
```powershell
cd forex_bot
setup.bat
```

**Linux/Mac:**
```bash
cd forex_bot
chmod +x setup.sh
./setup.sh
```

### Step 2: Get Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy your key

### Step 3: Configure API Key
1. Open `.env` file in the project folder
2. Replace: `GEMINI_API_KEY=your_gemini_api_key_here`
3. With: `GEMINI_API_KEY=your_actual_key_pasted_here`
4. Save file

### Step 4: Run the App
```powershell
.\run.bat
```

### Optional: Run the Mobile-Friendly Web App
```powershell
.\run_web.bat
```

For online mobile access, deploy `streamlit_app.py` from your GitHub repo on Streamlit Community Cloud and add `GEMINI_API_KEY` in the app secrets.

---

## 📊 How to Use

### 1️⃣ Select Forex Pair
- Dropdown menu with 8 major pairs
- XAUUSD, EURUSD, GBPUSD, etc.

### 2️⃣ Select Timeframe
- Available: 1m, 5m, 15m, 30m, 1h, 4h, 1D, 1W
- Choose based on your trading style

### 3️⃣ Upload Chart Image
- Click **"📁 Browse Chart Image"**
- Select chart from TradingView or your broker
- Supported: JPG, PNG, GIF, BMP, WebP (max 10MB)
- See preview before analyzing

### 4️⃣ Click "🚀 Analyze Chart"
- Progress bar shows analysis stages:
  - Analyzing with Gemini Pro...
  - Parsing results...
  - Analyzing image features...
  - Saving to database...

### 5️⃣ Review Results
Results tab shows:
```
PREDICTED DIRECTION: UP / DOWN / CONSOLIDATION
CONFIDENCE: XX%

SUPPORT LEVELS: 1.0850, 1.0820, 1.0790
RESISTANCE LEVELS: 1.0950, 1.0980, 1.1020

[Detailed AI Analysis]
- Market Structure
- Support/Resistance Analysis
- Supply/Demand Zones
- BOS/CHoC Detection
- Candle Pattern Analysis
- Trend Bias
- Price Targets
```

### 6️⃣ Check History
- **History Tab**: All past analyses
- **Pattern DB Tab**: Pattern statistics
- Click row to reload analysis

---

## 🎯 Analysis Includes

### Market Structure
- Trend direction (Uptrend/Downtrend/Ranging)
- Higher Highs/Lows or Lower Highs/Lows
- Structure breaks and changes

### Support & Resistance
- Exact price levels
- Strength assessment
- Moving averages

### Supply & Demand Zones
- Unmitigated zones
- Liquidity pools
- Rejection areas

### Candlestick Patterns
- Engulfing
- Pin bars
- Doji
- Hammer
- Wick analysis

### Trend & Momentum
- Bias direction
- Strength assessment
- Divergence signals

### Predictions
- Next few hours movement
- Price targets
- Entry/Exit levels
- Probability %

---

## ❓ Troubleshooting

### "GEMINI_API_KEY not found"
✅ Solution:
1. Verify `.env` file exists in project folder
2. Check API key is filled in (not the example text)
3. Save the file
4. Restart the app

### App won't start
✅ Solution:
1. Run: `.\run.bat` on Windows, or `.\venv\Scripts\python.exe main.py`
2. Check error in terminal
3. Verify all dependencies in the virtual environment: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Check Python version: `python --version` (need 3.8+)

### Image upload fails
✅ Solution:
1. Image must be < 10MB
2. Use: JPG, PNG, GIF, BMP, or WebP format
3. Try a different image
4. Clear project cache and retry

### Analysis takes too long
✅ Solution:
1. Gemini Pro analysis can take 10-30 seconds
2. Check internet connection
3. First time setup may be slower
4. Complex charts take longer to analyze

### No database results
✅ Solution:
1. First time - database is empty, run analysis first
2. History saved after each analysis
3. Check `data/forex_analysis.db` exists
4. Try running an analysis and refresh

---

## 💡 Tips & Tricks

### Best Results
- Use clear, zoomed-in charts
- Include pair name and timeframe label
- High resolution images work better
- Avoid cluttered indicators

### Trading Integration
- Copy analysis to your trading notes
- Set alerts at predicted levels
- Verify with your own analysis
- Always use stop losses

### Database
- All analyses stored in `data/forex_analysis.db`
- Can export for backtesting
- Patterns tracked for statistics
- Price history available

---

## ⚠️ IMPORTANT DISCLAIMERS

🚨 **This tool is for EDUCATIONAL purposes only**

- ❌ NOT financial advice
- ❌ Do your own research
- ❌ AI predictions can be wrong
- ❌ Use proper risk management
- ❌ Trade at your own risk
- ❌ Forex trading involves significant losses

✅ Best practices:
- Always use stop losses
- Risk only what you can afford to lose
- Verify AI analysis with your own analysis
- Don't trade on AI prediction alone
- Keep detailed trade records

---

## 📱 File Locations

- **Config**: `config.py` - Pairs, timeframes, API settings
- **Database**: `data/forex_analysis.db` - All analysis history
- **Logs**: `logs/` - Application logs
- **API Key**: `.env` - Your Gemini key (keep secret!)

---

## 🆘 Need Help?

1. Check `logs/` folder for error messages
2. Verify `.env` configuration
3. Test API key at: makersuite.google.com/app/apikey
4. Check internet connection
5. Review README.md for detailed docs

---

## 🎓 Next Steps

✅ App is ready to use!

1. Test with a sample chart
2. Review the analysis
3. Compare with TradingView analysis
4. Build your trading strategy
5. Practice paper trading first

**Happy Trading! 📈**
