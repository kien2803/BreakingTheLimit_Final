@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd /d %~dp0

REM Activate venv and run
call venv\bin\activate.bat
python app.py

pause

