@echo off
echo Installing Python dependencies...
echo.

REM Try to install pip first
python -m ensurepip --upgrade

REM Install dependencies
python -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests

echo.
echo Installation complete!
echo.
pause

