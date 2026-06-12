@echo off
REM Forex Trading Bot Setup Script for Windows

echo ============================================
echo Forex Trading Bot - Setup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements-desktop.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 4: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your Gemini API key!
    echo Get it from: https://makersuite.google.com/app/apikey
) else (
    echo .env file already exists
)

echo.
echo ============================================
echo ✅ Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run: run.bat
echo.
pause
