"""
Quick Start Guide for Forex Trading Bot
"""

import os
import sys

# Reconfigure stdout to UTF-8 to support emoji display on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def print_header(text):
    print("\n" + "="*50)
    print(f" {text}")
    print("="*50)

def check_gemini_key():
    """Check if Gemini API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return False
    return True

def get_gemini_key():
    """Guide user to get Gemini API key"""
    print_header("GETTING YOUR GEMINI PRO API KEY")
    print("""
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Open .env file in the project
6. Replace 'your_gemini_api_key_here' with your actual key
7. Save the file
    """)

def verify_installation():
    """Verify all dependencies are installed"""
    print_header("VERIFYING INSTALLATION")
    
    dependencies = [
        ("PyQt6", "PyQt6"),
        ("google.genai", "google-genai"),
        ("PIL", "Pillow"),
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("requests", "requests"),
        ("dotenv", "python-dotenv"),
        ("sqlalchemy", "SQLAlchemy")
    ]
    
    all_installed = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} not installed")
            all_installed = False
            
    return all_installed

def main():
    print_header("FOREX TRADING BOT - QUICK START")
    
    print("""
Welcome to the Forex Trading Bot!

This guide will help you get started.
    """)
    
    # Check dependencies
    print("\nStep 1: Checking dependencies...")
    if not verify_installation():
        print("\n⚠️  Some dependencies are missing!")
        print("Run: pip install -r requirements-desktop.txt")
        return
    
    # Check API Key
    print("\nStep 2: Checking Gemini API Key...")
    if not check_gemini_key():
        print("❌ Gemini API key not configured")
        get_gemini_key()
        return
    
    print("✅ Gemini API key configured")
    
    # Ready to run
    print_header("READY TO START")
    print("""
Everything is set up! You can now run the app:

    python main.py

The Forex Trading Bot will:
1. Open a desktop application window
2. Let you upload forex chart images
3. Analyze charts using AI
4. Predict market movements
5. Store analysis history

IMPORTANT REMINDERS:
⚠️  This tool is for educational purposes
⚠️  Not financial advice - always do your own research
⚠️  Use proper risk management when trading
⚠️  Past performance doesn't guarantee future results

Features:
📊 Chart upload and analysis
🤖 AI-powered predictions
📈 Technical pattern recognition
💾 Analysis database
🎯 Support/Resistance detection
    """)

if __name__ == '__main__':
    main()
