@echo off
title Photo Solver - Start

echo ========================================
echo   Photo Solver App
echo ========================================
echo.

set "BASE=%~dp0"

echo [1/4] Installing backend dependencies...
cd /d "%BASE%backend"
pip install -r requirements.txt

echo.
echo [2/4] Installing frontend dependencies...
cd /d "%BASE%frontend"
call npm install

echo.
echo [3/4] Starting backend on port 8000...
start "PhotoSolver-Backend" cmd /k "cd /d %BASE%backend && python main.py"

echo [4/4] Starting frontend on port 5173...
start "PhotoSolver-Frontend" cmd /k "cd /d %BASE%frontend && npm run dev"

echo.
echo ========================================
echo   Done!
echo   Backend : http://localhost:8000
echo   Frontend: http://localhost:5173
echo.
echo   First time? Open Settings and add your API Key.
echo ========================================
echo.
pause
