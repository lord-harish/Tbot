#!/bin/bash
# Forex Trading Bot Setup Script for Linux/Mac

echo "============================================"
echo "Forex Trading Bot - Setup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Installing dependencies..."
pip install -r requirements-desktop.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 4: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Gemini API key!"
    echo "Get it from: https://makersuite.google.com/app/apikey"
else
    echo ".env file already exists"
fi

echo ""
echo "============================================"
echo "✅ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GEMINI_API_KEY"
echo "2. Run: python main.py"
echo ""
