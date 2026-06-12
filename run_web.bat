@echo off
REM Forex Trading Bot Web App Runner

if not exist venv (
    echo Virtual environment not found. Setting up first...
    call setup.bat
)

echo Starting Forex Trading Bot Web App...
venv\Scripts\python.exe -m streamlit run streamlit_app.py
