@echo off
echo ====================================
echo Starting Sentiment Analysis Web App
echo ====================================
echo.
echo Starting Backend Server...
start cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Both servers are starting!
echo ====================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo ====================================
echo.
echo Press any key to exit this window...
pause >nul
