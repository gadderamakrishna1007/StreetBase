@echo off
cls
echo.
echo ========================================
echo    🏠 AI Property Valuation Tool
echo ========================================
echo.
echo Starting your app...
echo.
echo The app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo ========================================
echo.

python -m streamlit run simple_app.py --server.port=8501 --server.headless=false

echo.
echo App stopped. Press any key to exit...
pause > nul