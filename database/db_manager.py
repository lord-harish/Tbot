import sqlite3
from datetime import datetime
import json
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Analysis History Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    pair TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    image_path TEXT,
                    analysis_result TEXT,
                    prediction TEXT,
                    confidence REAL,
                    patterns TEXT,
                    support_levels TEXT,
                    resistance_levels TEXT
                )
            ''')
            
            # Pattern Database Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pattern_database (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_name TEXT NOT NULL,
                    pair TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    description TEXT,
                    success_rate REAL,
                    occurrences INTEGER DEFAULT 0,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Price Tracking Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pair TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    price REAL NOT NULL,
                    volume INTEGER,
                    source TEXT
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
            conn.close()
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def save_analysis(self, pair, timeframe, image_path, analysis_result, prediction, 
                     confidence, patterns, support_levels, resistance_levels):
        """Save analysis result to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_history 
                (pair, timeframe, image_path, analysis_result, prediction, confidence, patterns, support_levels, resistance_levels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (pair, timeframe, image_path, analysis_result, prediction, confidence, 
                  json.dumps(patterns), json.dumps(support_levels), json.dumps(resistance_levels)))
            
            conn.commit()
            analysis_id = cursor.lastrowid
            logger.info(f"Analysis saved with ID: {analysis_id}")
            conn.close()
            return analysis_id
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            return None
    
    def get_analysis_history(self, pair=None, limit=50):
        """Retrieve analysis history"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if pair:
                cursor.execute('''
                    SELECT * FROM analysis_history 
                    WHERE pair = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (pair, limit))
            else:
                cursor.execute('''
                    SELECT * FROM analysis_history 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error retrieving analysis history: {e}")
            return []
    
    def save_price_tracking(self, pair, price, volume=None, source='API'):
        """Save price tracking data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO price_tracking (pair, price, volume, source)
                VALUES (?, ?, ?, ?)
            ''', (pair, price, volume, source))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving price tracking: {e}")
    
    def get_price_history(self, pair, hours=24):
        """Get price history for a pair"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM price_tracking 
                WHERE pair = ? 
                AND timestamp > datetime('now', '-' || ? || ' hours')
                ORDER BY timestamp DESC
            ''', (pair, hours))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error retrieving price history: {e}")
            return []
