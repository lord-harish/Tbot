import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QFileDialog, QTextEdit, QTabWidget,
    QTableWidget, QTableWidgetItem, QProgressBar, QMessageBox,
    QScrollArea, QFrame, QSplitter
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from datetime import datetime

import config
from analysis.gemini_analyzer import GeminiAnalyzer
from analysis.technical_analyzer import TechnicalAnalyzer
from analysis.economic_calendar import EconomicCalendar
from database.db_manager import DatabaseManager
from utils.logger import get_logger

logger = get_logger(__name__)

class AnalysisWorker(QThread):
    """Worker thread for running analysis without blocking UI"""
    analysis_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)
    
    def __init__(self, image_path, pair, timeframe, gemini_analyzer, tech_analyzer, calendar, db_manager):
        super().__init__()
        self.image_path = image_path
        self.pair = pair
        self.timeframe = timeframe
        self.gemini_analyzer = gemini_analyzer
        self.tech_analyzer = tech_analyzer
        self.calendar = calendar
        self.db_manager = db_manager
    
    def run(self):
        try:
            self.progress_update.emit("Analyzing image features...")
            image_features = self.tech_analyzer.analyze_image_features(self.image_path)

            self.progress_update.emit("Checking related economic calendar events...")
            calendar_context = self.calendar.get_events_for_pair(self.pair)

            self.progress_update.emit("Running higher-level Gemini forecast...")

            # Get Gemini analysis
            analysis_result = self.gemini_analyzer.analyze_chart(
                self.image_path,
                self.pair,
                self.timeframe,
                calendar_context=calendar_context,
                image_features=image_features
            )

            if not analysis_result:
                raise RuntimeError("Failed to analyze chart")

            self.progress_update.emit("Parsing analysis results...")
            parsed_analysis = self.gemini_analyzer.parse_analysis_response(analysis_result['raw_analysis'])
            
            # Combine results
            complete_analysis = {
                'pair': self.pair,
                'timeframe': self.timeframe,
                'timestamp': datetime.now().isoformat(),
                'gemini_analysis': analysis_result,
                'parsed_analysis': parsed_analysis,
                'image_features': image_features,
                'calendar_context': calendar_context
            }
            
            # Save to database
            self.progress_update.emit("Saving analysis to database...")
            self.db_manager.save_analysis(
                pair=self.pair,
                timeframe=self.timeframe,
                image_path=self.image_path,
                analysis_result=str(analysis_result),
                prediction=parsed_analysis.get('direction', 'UNKNOWN'),
                confidence=parsed_analysis.get('confidence', 0),
                patterns=[],
                support_levels=parsed_analysis.get('support_levels', []),
                resistance_levels=parsed_analysis.get('resistance_levels', [])
            )
            
            self.progress_update.emit("Analysis complete!")
            self.analysis_complete.emit(complete_analysis)
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            self.error_occurred.emit(f"Analysis error: {str(e)}")


class ForexBotMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize components
        try:
            self.db_manager = DatabaseManager(config.DB_PATH)
            
            if not config.GEMINI_API_KEY:
                QMessageBox.critical(
                    self, 
                    "Missing API Key",
                    "GEMINI_API_KEY not found in environment variables.\n\n"
                    "Please:\n"
                    "1. Create a .env file in the project directory\n"
                    "2. Add: GEMINI_API_KEY=your_api_key_here\n"
                    "3. Restart the application"
                )
                self.close()
                return
            
            self.gemini_analyzer = GeminiAnalyzer(config.GEMINI_API_KEY)
            self.tech_analyzer = TechnicalAnalyzer()
            self.economic_calendar = EconomicCalendar()
            
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", f"Failed to initialize: {str(e)}")
            self.close()
            return
        
        self.analysis_worker = None
        self.current_analysis = None
        self.current_image_path = None
        
        self.init_ui()
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(100, 100, config.APP_WIDTH, config.APP_HEIGHT)
    
    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel: Input and controls
        left_panel = self.create_left_panel()
        
        # Right panel: Results
        right_panel = self.create_right_panel()
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
    
    def create_left_panel(self):
        """Create left input panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("Forex Chart Analyzer")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Pair Selection
        layout.addWidget(QLabel("Select Forex Pair:"))
        self.pair_combo = QComboBox()
        self.pair_combo.addItems(config.FOREX_PAIRS)
        layout.addWidget(self.pair_combo)
        
        # Timeframe Selection
        layout.addWidget(QLabel("Select Timeframe:"))
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(config.TIMEFRAMES)
        layout.addWidget(self.timeframe_combo)
        
        # Image Upload
        layout.addWidget(QLabel("Chart Image:"))
        
        upload_btn_layout = QHBoxLayout()
        self.upload_btn = QPushButton("📁 Browse Chart Image")
        self.upload_btn.clicked.connect(self.upload_image)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        upload_btn_layout.addWidget(self.upload_btn)
        layout.addLayout(upload_btn_layout)
        
        # Image preview
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(150)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")
        layout.addWidget(self.image_label)
        
        layout.addWidget(QLabel("File path:"))
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("color: #666; font-style: italic;")
        self.file_path_label.setWordWrap(True)
        layout.addWidget(self.file_path_label)
        
        # Analyze Button
        layout.addSpacing(20)
        self.analyze_btn = QPushButton("🚀 Analyze Chart")
        self.analyze_btn.clicked.connect(self.analyze_chart)
        self.analyze_btn.setMinimumHeight(50)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        layout.addWidget(self.analyze_btn)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status Label
        self.status_label = QLabel("Ready to analyze")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create right results panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Tabs for different views
        self.tabs = QTabWidget()
        
        # Tab 1: Analysis Results
        self.analysis_tab = QTextEdit()
        self.analysis_tab.setReadOnly(True)
        self.tabs.addTab(self.analysis_tab, "📊 Analysis")
        
        # Tab 2: History
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Time", "Pair", "Timeframe", "Prediction", "Confidence"])
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.itemClicked.connect(self.load_history_item)
        self.tabs.addTab(self.history_table, "📈 History")
        
        # Tab 3: Pattern Database
        self.pattern_table = QTableWidget()
        self.pattern_table.setColumnCount(4)
        self.pattern_table.setHorizontalHeaderLabels(["Pattern", "Pair", "Timeframe", "Success Rate"])
        self.tabs.addTab(self.pattern_table, "🎯 Pattern DB")
        
        layout.addWidget(self.tabs)
        
        # Load History Button
        load_btn_layout = QHBoxLayout()
        load_history_btn = QPushButton("🔄 Refresh History")
        load_history_btn.clicked.connect(self.refresh_history)
        load_btn_layout.addWidget(load_history_btn)
        load_btn_layout.addStretch()
        layout.addLayout(load_btn_layout)
        
        return panel
    
    def upload_image(self):
        """Handle image upload"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Forex Chart Image",
            "",
            "Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.webp);;All Files (*)"
        )
        
        if file_path:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > config.MAX_IMAGE_SIZE:
                QMessageBox.warning(
                    self,
                    "File Too Large",
                    f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds limit ({config.MAX_IMAGE_SIZE / 1024 / 1024:.2f}MB)"
                )
                return
            
            self.current_image_path = file_path
            self.file_path_label.setText(file_path)
            
            # Show preview
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaledToHeight(150, Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
            
            logger.info(f"Image selected: {file_path}")
    
    def analyze_chart(self):
        """Start chart analysis"""
        if not self.current_image_path:
            QMessageBox.warning(self, "No Image", "Please select a chart image first")
            return
        
        if not os.path.exists(self.current_image_path):
            QMessageBox.warning(self, "File Not Found", "Selected image file not found")
            return
        
        pair = self.pair_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        
        # Disable buttons and show progress
        self.analyze_btn.setEnabled(False)
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.status_label.setText("Analyzing...")
        self.status_label.setStyleSheet("color: #ffc107; font-weight: bold;")
        
        # Start worker thread
        self.analysis_worker = AnalysisWorker(
            self.current_image_path,
            pair,
            timeframe,
            self.gemini_analyzer,
            self.tech_analyzer,
            self.economic_calendar,
            self.db_manager
        )
        
        self.analysis_worker.analysis_complete.connect(self.on_analysis_complete)
        self.analysis_worker.error_occurred.connect(self.on_analysis_error)
        self.analysis_worker.progress_update.connect(self.on_progress_update)
        
        self.analysis_worker.start()
    
    def on_progress_update(self, message):
        """Update progress"""
        self.status_label.setText(message)
        self.progress_bar.setValue(min(self.progress_bar.value() + 20, 100))
    
    def on_analysis_complete(self, analysis_data):
        """Handle analysis completion"""
        self.current_analysis = analysis_data
        
        # Display results
        gemini_text = analysis_data['gemini_analysis']['raw_analysis']
        parsed = analysis_data['parsed_analysis']
        calendar_context = analysis_data.get('calendar_context', {})
        calendar_events = calendar_context.get('events', [])
        calendar_lines = []
        for event in calendar_events[:8]:
            event_time = event.get('time_utc')
            if hasattr(event_time, 'astimezone'):
                event_time = EconomicCalendar.format_event_time(event_time)
            calendar_lines.append(
                f"- {event_time} | {event.get('currency', 'N/A')} | "
                f"{event.get('impact', 'Unknown').upper()} | {event.get('title', 'Untitled event')}"
            )
        calendar_text = '\n'.join(calendar_lines) if calendar_lines else calendar_context.get(
            'summary',
            'No calendar events available.'
        )
        
        results_text = f"""
FOREX TRADING ANALYSIS
{'='*60}

PAIR: {analysis_data['pair']}
TIMEFRAME: {analysis_data['timeframe']}
TIME: {analysis_data['timestamp']}

PREDICTED DIRECTION: {parsed.get('direction', 'UNKNOWN')}
CONFIDENCE: {parsed.get('confidence', 0)}%
BIAS: {parsed.get('bias', 'WAIT')}
TRADE QUALITY: {parsed.get('trade_quality_score', 0)}/100
VOLATILITY RISK: {parsed.get('volatility_risk', 'UNKNOWN')}
PRIMARY TARGET: {parsed.get('primary_target', 'N/A')}
INVALIDATION: {parsed.get('invalidation_level', 'N/A')}

SUPPORT LEVELS: {', '.join(parsed.get('support_levels', ['N/A']))}
RESISTANCE LEVELS: {', '.join(parsed.get('resistance_levels', ['N/A']))}

{'='*60}
RELATED ECONOMIC CALENDAR:
{'='*60}

{calendar_text}

{'='*60}
DETAILED ANALYSIS:
{'='*60}

{gemini_text}
        """
        
        self.analysis_tab.setText(results_text)
        
        # Update status
        self.status_label.setText(f"✅ Analysis Complete - Prediction: {parsed.get('direction', 'UNKNOWN')}")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        
        # Re-enable buttons
        self.analyze_btn.setEnabled(True)
        self.upload_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Refresh history
        self.refresh_history()
        
        logger.info(f"Analysis complete for {analysis_data['pair']} {analysis_data['timeframe']}")
    
    def on_analysis_error(self, error_message):
        """Handle analysis error"""
        QMessageBox.critical(self, "Analysis Error", error_message)
        
        self.status_label.setText("❌ Analysis Failed")
        self.status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        
        self.analyze_btn.setEnabled(True)
        self.upload_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        logger.error(error_message)
    
    def refresh_history(self):
        """Refresh analysis history table"""
        try:
            history = self.db_manager.get_analysis_history(limit=50)
            
            self.history_table.setRowCount(0)
            for row_idx, item in enumerate(history):
                self.history_table.insertRow(row_idx)
                
                timestamp = item.get('timestamp', '')
                pair = item.get('pair', '')
                timeframe = item.get('timeframe', '')
                prediction = item.get('prediction', 'N/A')
                confidence = item.get('confidence', 0)
                
                self.history_table.setItem(row_idx, 0, QTableWidgetItem(str(timestamp)[:19]))
                self.history_table.setItem(row_idx, 1, QTableWidgetItem(pair))
                self.history_table.setItem(row_idx, 2, QTableWidgetItem(timeframe))
                self.history_table.setItem(row_idx, 3, QTableWidgetItem(prediction))
                self.history_table.setItem(row_idx, 4, QTableWidgetItem(f"{confidence}%"))
            
            # Resize columns
            self.history_table.resizeColumnsToContents()
            
        except Exception as e:
            logger.error(f"Error refreshing history: {e}")
    
    def load_history_item(self, item):
        """Load selected history item"""
        row = item.row()
        pair = self.history_table.item(row, 1).text()
        timeframe = self.history_table.item(row, 2).text()
        
        self.pair_combo.setCurrentText(pair)
        self.timeframe_combo.setCurrentText(timeframe)


def run_app():
    """Run the application"""
    app = None
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(sys.argv)
        window = ForexBotMainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application error: {e}")
        if app:
            QMessageBox.critical(None, "Application Error", str(e))


if __name__ == '__main__':
    run_app()
