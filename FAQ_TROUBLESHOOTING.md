# ❓ FAQ & Troubleshooting Guide

## Frequently Asked Questions

### Q: Do I need to pay for Gemini Pro?
**A:** No! Google Gemini Pro has a **free tier** with generous limits:
- Free: 60 requests per minute
- This is enough for all your analysis needs
- Premium available if needed

### Q: What if my Gemini API key doesn't work?
**A:** 
1. Verify key at: https://makersuite.google.com/app/apikey
2. Make sure it's currently active (not revoked)
3. Check `.env` file has correct key (no extra spaces)
4. Restart the application
5. Test in quickstart.py: `.\venv\Scripts\python.exe quickstart.py`

### Q: Why is analysis taking so long?
**A:** Gemini Pro takes time for complex analysis:
- First analysis: ~20-30 seconds
- Subsequent: ~10-15 seconds
- Depends on image complexity
- Internet connection speed matters
- This is normal!

### Q: Can I use images from any source?
**A:** Yes, as long as:
- ✅ TradingView charts
- ✅ MT4/MT5 screenshots
- ✅ Other broker platforms
- ✅ Any clear forex chart
- ❌ Must include pair name and timeframe

### Q: Will this predict the market correctly?
**A:** No! Important limitations:
- AI can be wrong
- Not guaranteed results
- Market is complex and unpredictable
- Use as tool, not guarantee
- Always do your own research
- Combine with multiple analysis methods

### Q: How do I export my analysis history?
**A:** 
1. Database file: `data/forex_analysis.db`
2. Can open with SQLite browser
3. Export to CSV from there
4. Or write a Python script to export

### Q: Can I use this for real trading?
**A:** 
- ✅ Can assist in trading decisions
- ✅ Combine with your analysis
- ✅ Use for pattern recognition
- ❌ Don't trade on prediction alone
- ❌ Always use stop losses
- ❌ Risk management is YOUR responsibility

### Q: What's the maximum file size?
**A:** 10MB (can be changed in config.py)
- Most screenshots: 1-5MB
- Should be fine

### Q: Can I run multiple analyses at once?
**A:** Each analysis runs in separate thread:
- Can start new analysis while one is running
- UI stays responsive
- Results appear as they complete
- Database saves all of them

### Q: Where is my data stored?
**A:** All local:
- Database: `data/forex_analysis.db`
- Images: Referenced, not copied
- Logs: `logs/` folder
- No cloud storage

### Q: How do I add more currency pairs?
**A:**
1. Edit `config.py`
2. Add pair to `FOREX_PAIRS` list
3. Restart app
Done!

---

## Troubleshooting Guide

### ❌ Problem: "GEMINI_API_KEY not found" Error

**Cause:** API key not configured

**Solutions:**
1. ✅ Create `.env` file in project folder
2. ✅ Add: `GEMINI_API_KEY=your_key_here`
3. ✅ Get key from: makersuite.google.com/app/apikey
4. ✅ Save file and restart app

**Check:**
```bash
# Verify .env exists
dir .env  # Windows
ls -la .env  # Linux/Mac

# Verify content
type .env  # Windows
cat .env  # Linux/Mac
```

---

### ❌ Problem: App Won't Start

**Cause:** Missing dependencies

**Solutions:**
1. ✅ Run setup script: `setup.bat` or `setup.sh`
2. ✅ Or manually install:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. ✅ Check Python version:
```bash
python --version
# Should be 3.8 or higher
```

4. ✅ Try running directly:
```powershell
.\venv\Scripts\python.exe main.py
```

5. ✅ Check error log:
```bash
cat logs/*.log  # See error details
```

---

### ❌ Problem: "Image File Not Found" Error

**Cause:** File path invalid or file deleted

**Solutions:**
1. ✅ Reselect image: Click "Browse Chart Image"
2. ✅ Verify file still exists
3. ✅ Ensure full write access to folder
4. ✅ Try with different image

---

### ❌ Problem: "File Too Large" Warning

**Cause:** Image exceeds 10MB limit

**Solutions:**
1. ✅ Compress image before uploading
2. ✅ Crop unnecessary parts
3. ✅ Convert to JPG format (smaller)
4. ✅ Increase limit in config.py if needed

---

### ❌ Problem: Slow Image Upload

**Cause:** Large file or slow connection

**Solutions:**
1. ✅ Try smaller image
2. ✅ Check internet connection
3. ✅ Restart app
4. ✅ Try different image

---

### ❌ Problem: Analysis Fails with API Error

**Cause:** API issue or key invalid

**Solutions:**
1. ✅ Check internet connection
2. ✅ Verify API key is active
3. ✅ Try different chart
4. ✅ Wait a minute and retry
5. ✅ Check Gemini status page

---

### ❌ Problem: No Analysis Results Showing

**Cause:** Analysis completed but UI not updating

**Solutions:**
1. ✅ Click "Refresh History" button
2. ✅ Check Results tab
3. ✅ Check logs for errors
4. ✅ Try new analysis

---

### ❌ Problem: Database Errors

**Cause:** Corrupted or locked database

**Solutions:**
1. ✅ Delete `data/forex_analysis.db`
2. ✅ App will recreate on next run
3. ✅ This clears old analyses (fresh start)

---

### ❌ Problem: PyQt6 Import Error

**Cause:** PyQt6 not installed correctly

**Solutions:**
```bash
# Uninstall and reinstall
pip uninstall PyQt6 -y
pip install PyQt6==6.7.0
```

---

### ❌ Problem: "Connection Timeout" to Gemini

**Cause:** Internet connection or Gemini server issue

**Solutions:**
1. ✅ Check internet connection
2. ✅ Try again in a minute
3. ✅ Check if Gemini API is down
4. ✅ Try with different image

---

### ❌ Problem: Can't Find Logs

**Cause:** Logs folder not visible

**Solutions:**
```bash
# Windows - Show hidden files
# In File Explorer: View > Hidden items (check box)

# Or navigate to folder
cd forex_bot\logs

# Linux/Mac
ls -la logs/
```

---

## Performance Tips

### Speed Up Analysis
1. ✅ Use cropped chart images (smaller)
2. ✅ Use JPG format (smaller than PNG)
3. ✅ Clear old data occasionally
4. ✅ Use faster internet

### Keep Database Clean
```bash
# Backup database first
# Then delete old analysis
# Or query specific pairs only
```

### Free Up Disk Space
1. ✅ Delete old log files
2. ✅ Compress old database
3. ✅ Remove unused images

---

## Advanced Troubleshooting

### Enable Debug Logging
Edit `utils/logger.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG
    # ... rest of config
)
```

### Check API Response
Add to `gemini_analyzer.py`:
```python
print("Response:", response.text)  # See raw response
```

### Verify Database
```bash
# Use SQLite browser
# Download: https://sqlitebrowser.org/

# Or use command line
sqlite3 data/forex_analysis.db
# Then: SELECT * FROM analysis_history LIMIT 5;
```

---

## Getting Help

**If you're still stuck:**

1. ✅ Check the logs: `logs/` folder
2. ✅ Review README.md
3. ✅ Check QUICKSTART.md
4. ✅ Review ARCHITECTURE.md
5. ✅ Test API key: makersuite.google.com/app/apikey

**Common Issues Checklist:**
- [ ] API key added to `.env`?
- [ ] `.env` file saved?
- [ ] All dependencies installed?
- [ ] Python 3.8+ installed?
- [ ] Internet connection active?
- [ ] Image file valid?
- [ ] File < 10MB?
- [ ] App restarted after changes?

---

## Known Limitations

### Analysis Accuracy
- Depends on image quality
- Depends on indicator clarity
- AI can miss patterns
- Should verify manually

### Timeframe Limitations
- Very small timeframes (1m) may be noisy
- Very large timeframes (1W) fewer signals
- Best: 4h and 1D for most analysis

### Pair Limitations
- Works best with major pairs
- Minor pairs supported but less data
- Exotic pairs may have less accuracy

### Technical Limitations
- Max image: 10MB
- GUI limited to ~1400x900
- Analysis queue: one at a time (improved in future)
- Database: local only (not cloud)

---

## Future Improvements

Planned features:
- [ ] Faster analysis (parallel processing)
- [ ] Better pattern recognition
- [ ] Real-time price tracking
- [ ] Trading alerts
- [ ] Export functionality
- [ ] Mobile app
- [ ] Cloud backup
- [ ] Advanced statistics

---

Still having issues? Check:
1. Logs folder: `logs/`
2. Config file: `config.py`
3. Environment: `.env`
4. README: Full documentation
5. ARCHITECTURE: Technical details

**Good luck! 🚀**
