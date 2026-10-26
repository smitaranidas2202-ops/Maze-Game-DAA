#!/usr/bin/env bash
# Runner script for macOS & Linux

echo "============================================================"
echo "  Maze Game - DAA Mini-Project (DFS vs BFS Pathfinding)"
echo "============================================================"
echo ""

# Find python3 or python
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "[ERROR] Python 3 was not found on your system."
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo "[1/2] Installing requirements..."
$PYTHON_CMD -m pip install -r requirements.txt --quiet 2>/dev/null || true

echo "[2/2] Launching Maze Game..."
$PYTHON_CMD main.py
