@echo off
REM Tbot Web App Runner

if not exist venv (
    echo Virtual environment not found. Setting up first...
    call setup.bat
)

echo Starting Tbot Web App...
venv\Scripts\python.exe -m streamlit run streamlit_app.py
