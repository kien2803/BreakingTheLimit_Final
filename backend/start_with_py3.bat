@echo off
echo Starting Backend Server with py -3...
echo.

REM Check if py -3 works
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: py -3 not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
py -3 -m pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    py -3 -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
)

REM Run server
echo.
echo Starting server...
py -3 app.py

pause

