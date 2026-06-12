#!/usr/bin/env python3
"""
Forex Trading Bot - AI-Powered Chart Analysis
Analyzes forex charts using Google Gemini Pro and predicts market movements
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import run_app
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main entry point"""
    try:
        logger.info("Starting Forex Trading Bot...")
        run_app()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()
