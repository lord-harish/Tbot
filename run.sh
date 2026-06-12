#!/bin/bash
# Forex Trading Bot Linux/Mac Runner Script

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Setting up first..."
    chmod +x setup.sh
    ./setup.sh
fi

echo "Starting Forex Trading Bot..."
./venv/bin/python main.py
