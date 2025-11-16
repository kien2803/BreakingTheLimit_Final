Write-Host "Starting Backend Server with py -3..." -ForegroundColor Green
Write-Host ""

# Check if py -3 works
try {
    $version = py -3 --version 2>&1
    Write-Host "Python found: $version" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: py -3 not found!" -ForegroundColor Red
    Write-Host "Please install Python from python.org" -ForegroundColor Yellow
    exit 1
}

# Check if Flask is installed
$flaskInstalled = py -3 -m pip show flask 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    py -3 -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
}

# Run server
Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
py -3 app.py

