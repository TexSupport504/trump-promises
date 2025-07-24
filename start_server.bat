@echo off
echo Starting Trump Promises Tracker...
echo ====================================

REM Change to the project directory
cd /d "E:\OneDrive\Documents\GitHub\trump-promises"

REM Activate virtual environment and run server
call .venv\Scripts\activate.bat
python run_server.py

pause
