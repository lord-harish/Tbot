@echo off
REM Forex Trading Bot Windows Runner Script

if not exist venv (
    echo Virtual environment not found. Setting up first...
    call setup.bat
)

echo Starting Forex Trading Bot...
venv\Scripts\python.exe main.py
