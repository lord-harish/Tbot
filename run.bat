@echo off
REM Tbot Windows Runner Script

if not exist venv (
    echo Virtual environment not found. Setting up first...
    call setup.bat
)

echo Starting Tbot...
venv\Scripts\python.exe main.py
