@echo off
REM SecureDoc - Final Setup and Launch Script
REM This script ensures everything is ready and guides you through getting an API key

echo.
echo ========================================
echo   🚀 SECUREDOC - FINAL LAUNCH
echo ========================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv310\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating Python 3.10 environment...
call venv310\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if .env file exists and has API key
if not exist ".env" (
    echo ❌ .env file not found!
    echo Creating .env file...
    copy .env.example .env >nul 2>&1
)

REM Check API key
for /f "tokens=2 delims==" %%a in ('findstr "OPENAI_API_KEY" .env') do set API_KEY=%%a
if "%API_KEY%"=="" (
    echo ❌ No OpenAI API key found in .env file
    goto :GET_API_KEY
)
if "%API_KEY%"=="sk-" (
    echo ❌ OpenAI API key is empty in .env file
    goto :GET_API_KEY
)
if "%API_KEY%"=="sk-demo-key-for-testing-purposes-only" (
    echo ❌ Demo API key detected - you need a real one
    goto :GET_API_KEY
)

REM API key looks valid, continue
echo ✅ OpenAI API key detected
goto :LAUNCH_APP

:GET_API_KEY
echo.
echo ========================================
echo   🔑 GET YOUR OPENAI API KEY
echo ========================================
echo.
echo To use SecureDoc, you need an OpenAI API key:
echo.
echo 1. 🌐 Open your browser and go to:
echo    https://platform.openai.com/api-keys
echo.
echo 2. 🔐 Sign in or create a free account
echo    (New accounts get $5-$18 in free credits!)
echo.
echo 3. ➕ Click "Create new secret key"
echo.
echo 4. 📋 Copy the API key (starts with "sk-")
echo.
echo 5. 📝 Open the .env file in this folder
echo.
echo 6. ✏️  Replace this line:
echo    OPENAI_API_KEY=sk-
echo.
echo    With your actual key:
echo    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
echo.
echo 7. 💾 Save the file and close it
echo.
echo 8. ▶️  Run this script again
echo.
echo ========================================
echo.
echo Press any key when you have your API key ready...
pause >nul
goto :LAUNCH_APP

:LAUNCH_APP
echo.
echo ========================================
echo   🚀 STARTING SECUREDOC
echo ========================================
echo.
echo 🔍 Checking dependencies...
pip install -q -r requirements.txt 2>nul

echo.
echo ✅ Environment ready!
echo 🌐 Opening SecureDoc at: http://localhost:8501
echo.
echo 📖 Instructions:
echo 1. Upload a PDF file using the uploader
echo 2. Configure settings in the left sidebar (optional)
echo 3. Ask questions about your PDF content
echo 4. View answers with source references
echo.
echo Press Ctrl+C in this window to stop the server
echo.

REM Start the Streamlit app
streamlit run app.py --server.headless true --server.port 8501

echo.
echo Server stopped. Press any key to exit...
pause >nul