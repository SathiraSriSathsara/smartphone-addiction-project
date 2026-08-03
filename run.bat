@echo off
title Smartphone Addiction Project Launcher

cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo ==========================================
echo Starting Smartphone Addiction Project...
echo ==========================================

REM Start FastAPI server
start "API Server" cmd /k "call .venv\Scripts\activate.bat && uvicorn api.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Web Server
start "Web Server" cmd /k "call .venv\Scripts\activate.bat && python -m http.server 5500 --directory web"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:5500

echo.
echo API  : http://127.0.0.1:8000
echo Web  : http://localhost:5500
echo Docs : http://127.0.0.1:8000/docs
echo.
echo Both servers are running.
pause