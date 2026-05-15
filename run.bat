@echo off
REM SecureDoc - PDF Q&A Application
REM Created with Python 3.10

echo ========================================
echo   SecureDoc - PDF Q&A with OpenAI
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv310\Scripts\activate.bat" (
    echo Creating Python 3.10 virtual environment...
    py -3.10 -m venv venv310
    if errorlevel 1 (
        echo Error: Could not create virtual environment
        echo Make sure Python 3.10 is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv310\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Could not activate virtual environment
    pause
    exit /b 1
)

REM Install requirements if needed
echo Checking dependencies...
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Environment ready! Starting SecureDoc...
echo.
echo 🌐 Opening: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Start the Streamlit app
streamlit run app.py --logger.level=info

pause