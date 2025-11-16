Write-Host "========================================" -ForegroundColor Green
Write-Host "Starting Backend Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Set-Location $PSScriptRoot

# Activate venv
& "$PSScriptRoot\venv\bin\Activate.ps1"

# Run server
python app.py

