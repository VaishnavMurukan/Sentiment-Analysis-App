@echo off
REM Quick deployment preparation script

echo ====================================
echo Sentiment Analysis - Deploy Prep
echo ====================================
echo.

echo [1/4] Installing gunicorn...
pip install gunicorn

echo.
echo [2/4] Building frontend...
cd frontend
call npm run build
cd ..

echo.
echo [3/4] Files ready for deployment!
echo.
echo Next steps:
echo 1. Push to GitHub: git push origin main
echo 2. Deploy backend to Render.com
echo 3. Deploy frontend to Vercel.com
echo.
echo See DEPLOYMENT_GUIDE.md for details!
echo ====================================

pause
