Write-Host "Installing Python dependencies..." -ForegroundColor Green
Write-Host ""

# Try to install pip first
python -m ensurepip --upgrade

# Install dependencies
python -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Now you can run: python app.py" -ForegroundColor Yellow

