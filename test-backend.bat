@echo off
title Backend API Test
echo ========================================
echo   Backend API Health Check
echo ========================================
echo.
echo [1] Checking if backend is running...
curl -s http://localhost:8000/ 2>nul
if errorlevel 1 (
    echo FAIL - Backend not running! Start it first.
    pause
    exit /b 1
)
echo OK - Backend is alive
echo.

echo [2] Testing config endpoint...
curl -s http://localhost:8000/api/config
echo.
echo.

echo [3] Testing history endpoint...
curl -s http://localhost:8000/api/history
echo.
echo.

echo ========================================
echo Tests complete. If all returned JSON, backend is working.
echo If frontend still hangs, issue is in frontend code.
echo ========================================
pause
