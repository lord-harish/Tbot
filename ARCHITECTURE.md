# 🏗️ Forex Trading Bot - Architecture & Technical Details

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PyQt6 GUI (main_window.py)               │
│                   (1,300+ lines of UI)                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Input Panel          │      Results Panel            │  │
│  │ ─────────────────────┼─────────────────────────────  │  │
│  │ • Pair selector      │ • Analysis Results Tab         │  │
│  │ • Timeframe selector │ • History Table Tab            │  │
│  │ • Image upload       │ • Pattern DB Tab               │  │
│  │ • Analyze button     │ • Real-time updates            │  │
│  │ • Progress bar       │                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│                    AnalysisWorker (Thread)                  │
│                   (Runs analysis without                    │
│                    blocking UI)                             │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │   Gemini    │   │ Technical   │   │  Database   │
   │  Analyzer   │   │  Analyzer   │   │  Manager    │
   │             │   │             │   │             │
   │ • Upload    │   │ • Detect    │   │ • Save      │
   │   image     │   │   patterns  │   │   analysis  │
   │ • Send to   │   │ • Calculate │   │ • Store     │
   │   Gemini    │   │   S/R       │   │   history   │
   │ • Parse     │   │ • Supply/   │   │ • Query     │
   │   response  │   │   Demand    │   │   data      │
   │ • Extract   │   │   zones     │   │             │
   │   direction │   │             │   │             │
   │   & targets │   │             │   │             │
   └─────────────┘   └─────────────┘   └─────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                    ┌──────────────────┐
                    │  SQLite Database │
                    │ (forex_analysis) │
                    │                  │
                    │ • analysis_      │
                    │   history        │
                    │ • pattern_db     │
                    │ • price_tracking │
                    └──────────────────┘
```

## Data Flow

```
User Action: Upload Chart
                │
                ▼
    Extract Pair & Timeframe
                │
                ▼
    Validate Image (< 10MB)
                │
                ▼
    Display Preview & Path
                │
                ▼
    Click "Analyze Chart"
                │
                ▼
    Create AnalysisWorker Thread
                │
    ┌───────────┼────────────┐
    ▼           ▼            ▼
  UI Running  Worker Thread Running
              (Non-blocking)
                │
    ┌───────────┼────────────────────┐
    ▼           ▼                    ▼
Step 1:     Step 2:              Step 3:
Upload      Parse                Analyze
Image to    Response             Image
Gemini      from                 Features
            Gemini
    │           │                    │
    └───────────┴────────────────────┘
                │
                ▼
    Combine All Results
                │
                ▼
    Save to Database
                │
                ▼
    Emit Signal to UI
                │
                ▼
    Display Results
    Update History
    Refresh UI
```

## Module Responsibilities

### 1. **main_window.py** (PyQt6 GUI)
- **Responsibilities:**
  - Render desktop application
  - Handle user interactions
  - Create worker threads
  - Display results
  - Update history/database views

- **Classes:**
  - `AnalysisWorker` - QThread subclass for async analysis
  - `ForexBotMainWindow` - Main application window

- **UI Panels:**
  - Left: Input controls and image upload
  - Right: Results tabs (Analysis, History, Pattern DB)

### 2. **gemini_analyzer.py** (AI Analysis)
- **Responsibilities:**
  - Communicate with Google Gemini Pro API
  - Send chart images for analysis
  - Parse AI responses
  - Extract structured data

- **Key Methods:**
  - `analyze_chart()` - Main analysis method
  - `parse_analysis_response()` - Extract direction, confidence, targets
  - `_extract_direction()` - Determine UP/DOWN/CONSOLIDATION
  - `_extract_confidence()` - Get confidence percentage
  - `_extract_targets()` - Extract price targets

### 3. **technical_analyzer.py** (Pattern Recognition)
- **Responsibilities:**
  - Perform technical analysis on chart images
  - Detect candlestick patterns
  - Calculate support/resistance
  - Identify supply/demand zones

- **Key Methods:**
  - `analyze_image_features()` - Edge/contour detection
  - `detect_candle_patterns()` - Pattern identification
  - `calculate_support_resistance()` - Level calculation
  - `detect_supply_demand_zones()` - Zone identification

- **Patterns Detected:**
  - Engulfing
  - Pin bars
  - Doji
  - Hammer

### 4. **db_manager.py** (Database)
- **Responsibilities:**
  - SQLite database operations
  - Store analysis results
  - Retrieve history
  - Track price data
  - Manage pattern database

- **Tables:**
  - `analysis_history` - All analyses
  - `pattern_database` - Pattern statistics
  - `price_tracking` - Price history

- **Key Methods:**
  - `save_analysis()` - Store analysis result
  - `get_analysis_history()` - Retrieve past analyses
  - `save_price_tracking()` - Log price data
  - `get_price_history()` - Get price data

### 5. **config.py** (Configuration)
- **Responsibilities:**
  - Define app settings
  - List supported pairs
  - List supported timeframes
  - Configure API keys
  - Set file size limits

- **Configurable:**
  - Forex pairs (8 major pairs)
  - Timeframes (8 timeframes from 1m to 1W)
  - Image size limit (10MB)
  - Supported formats (JPG, PNG, GIF, BMP, WebP)
  - Gemini model selection

### 6. **logger.py** (Logging)
- **Responsibilities:**
  - Log application events
  - Write to file and console
  - Track errors and issues

- **Log Levels:**
  - INFO - General information
  - ERROR - Errors and exceptions
  - DEBUG - Detailed debugging (optional)

## Analysis Workflow

### Input: Chart Image
```
Chart Image (.jpg, .png, etc.)
     │
     ▼
Validate Format & Size
     │
     ▼
Display Preview
     │
     ▼
Ready for Analysis
```

### Processing: Gemini Analysis
```
Chart → Gemini Pro API
          │
          ├─ Market Structure Analysis
          ├─ Support & Resistance
          ├─ Supply & Demand Zones
          ├─ Break of Structure (BOS)
          ├─ Change of Character (CHoC)
          ├─ Candlestick Patterns
          ├─ Trend Bias & Momentum
          └─ Price Predictions
               │
               ▼
        Gemini Response (Text)
               │
               ▼
        Parse & Extract:
        • Direction (UP/DOWN/CONSOLIDATION)
        • Confidence (%)
        • Support Levels
        • Resistance Levels
        • Price Targets
```

### Storage: Database
```
Parsed Results
     │
     ├─ Save to analysis_history
     ├─ Extract patterns
     ├─ Track price levels
     └─ Update pattern_database
          │
          ▼
        SQLite (forex_analysis.db)
```

### Output: Display Results
```
Complete Analysis
     │
     ├─ Direction & Confidence
     ├─ Support/Resistance Levels
     ├─ Full AI Analysis Text
     └─ Update History Table
          │
          ▼
        Display in GUI
```

## Threading Model

### Main Thread (UI)
- Handles user input
- Displays results
- Updates UI elements
- Never blocks

### Worker Thread (Analysis)
- Runs analysis in background
- Communicates via signals
- Doesn't freeze UI
- Emits `analysis_complete` signal when done

```
Main Thread (UI):
    User Input
         │
         ▼
    Create Worker
         │
         ├─ Worker starts on separate thread
         │       │
         │       ├─ Gemini Analysis
         │       ├─ Image Analysis
         │       ├─ Save Results
         │       │
         │       └─ Emit completion signal
         │
         ▼
    UI remains responsive
         │
    Receive signal
         │
         ▼
    Display Results
         │
         ▼
    Update History
```

## API Integration: Gemini Pro

### Request
```
Image (binary data)
   +
Analysis Prompt (detailed instructions)
   │
   ▼
Google Gemini API (genai.GenerativeModel)
```

### Response
```
Gemini Pro returns:
1. Detailed technical analysis
2. Support/Resistance identification
3. Pattern detection
4. Trend analysis
5. Price predictions
6. Entry/Exit suggestions
(In natural language text)
```

### Parsing
```
Raw Text Response
   │
   ├─ Extract "DIRECTION: UP/DOWN"
   ├─ Extract "CONFIDENCE: XX%"
   ├─ Extract support level prices
   ├─ Extract resistance level prices
   └─ Extract price targets
        │
        ▼
   Structured Data
```

## Database Schema

### analysis_history Table
```
Column              | Type      | Purpose
────────────────────┼───────────┼──────────────────────
id                  | PRIMARY   | Unique ID
timestamp           | DATETIME  | When analyzed
pair                | TEXT      | Currency pair
timeframe           | TEXT      | Timeframe (1h, 4h, etc)
image_path          | TEXT      | Path to chart image
analysis_result     | TEXT      | Full Gemini response
prediction          | TEXT      | UP/DOWN/CONSOLIDATION
confidence          | REAL      | Confidence %
patterns            | TEXT      | JSON of patterns found
support_levels      | TEXT      | JSON of support levels
resistance_levels   | TEXT      | JSON of resistance levels
```

### pattern_database Table
```
Column              | Type      | Purpose
────────────────────┼───────────┼──────────────────────
id                  | PRIMARY   | Unique ID
pattern_name        | TEXT      | Pattern type
pair                | TEXT      | Forex pair
timeframe           | TEXT      | Timeframe
description         | TEXT      | Pattern details
success_rate        | REAL      | Success percentage
occurrences         | INTEGER   | Times detected
creation_date       | DATETIME  | When added
```

### price_tracking Table
```
Column              | Type      | Purpose
────────────────────┼───────────┼──────────────────────
id                  | PRIMARY   | Unique ID
pair                | TEXT      | Forex pair
timestamp           | DATETIME  | When recorded
price               | REAL      | Price value
volume              | INTEGER   | Trading volume
source              | TEXT      | Data source (API/Manual)
```

## Error Handling

### Try-Catch Blocks
- Image validation
- API calls
- Database operations
- File I/O operations

### Error Messages
- User-friendly error dialogs
- Detailed logs in `logs/` folder
- Progress notifications
- Status updates

## Performance Considerations

### Optimization
- Async worker threads prevent UI freeze
- Image resizing for preview (faster display)
- Database indexing on frequently queried columns
- Batch database operations

### Limits
- Max image size: 10MB
- Max analysis history: 50 shown at once (pageable)
- Image formats: JPG, PNG, GIF, BMP, WebP

## Security

### API Key Protection
- Stored in `.env` file (not in code)
- `.gitignore` prevents accidental commits
- Loaded via `python-dotenv`
- Never logged or exposed

### Data Storage
- Local SQLite database (not cloud)
- Analysis stored locally
- No external data transmission (except to Gemini)
- User controls all data

## Future Enhancement Opportunities

1. **Real-time Data Integration**
   - Live price tracking
   - WebSocket connections
   - TradingView data feeds

2. **Machine Learning**
   - Pattern recognition improvement
   - Prediction accuracy enhancement
   - Historical backtesting

3. **Additional Features**
   - Multi-timeframe analysis
   - Pattern comparison
   - Trade alerts/notifications
   - Portfolio tracking

4. **Mobile Support**
   - Web interface
   - Mobile app
   - Cloud sync

5. **Advanced Analysis**
   - Volume profile
   - Order flow analysis
   - Market profile
   - Advanced statistics

---

## Configuration & Customization

### Add New Pairs
Edit `config.py`:
```python
FOREX_PAIRS = [
    'XAUUSD',
    'EURUSD',
    'YOUR_PAIR_HERE',  # Add here
]
```

### Change Timeframes
Edit `config.py`:
```python
TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W']
```

### Adjust Image Size Limit
Edit `config.py`:
```python
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # Change this value
```

### Modify Analysis Prompt
Edit `gemini_analyzer.py`:
```python
def _create_analysis_prompt(self, pair, timeframe):
    prompt = f"""
    Your custom analysis instructions here...
    """
```

---

This architecture provides:
✅ **Responsive UI** - Never freezes during analysis
✅ **Modular Design** - Easy to extend and modify
✅ **Secure** - API keys protected
✅ **Scalable** - Can handle multiple analyses
✅ **Maintainable** - Clean code structure
✅ **Reliable** - Error handling throughout
