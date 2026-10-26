@echo off
echo ============================================================
echo   Maze Game - DAA Mini-Project (DFS vs BFS Pathfinding)
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/2] Checking and installing dependencies...
python -m pip install -r requirements.txt --quiet

echo [2/2] Launching Maze Game...
python main.py

pause
