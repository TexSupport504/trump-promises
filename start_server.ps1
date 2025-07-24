# Trump Promises Tracker Launcher
Write-Host "Starting Trump Promises Tracker..." -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Change to the project directory
Set-Location "E:\OneDrive\Documents\GitHub\trump-promises"

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Start the server
Write-Host "Starting web server..." -ForegroundColor Yellow
python run_server.py

Read-Host "Press Enter to exit"
