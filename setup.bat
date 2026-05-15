@echo off
REM SecureDoc - Automatic Setup Script
REM This script sets up everything for SecureDoc

echo ========================================
echo   SecureDoc - Complete Setup
echo ========================================
echo.

echo [1/4] Checking Python 3.10...
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.10 not found!
    echo Please download and install Python 3.10 from https://www.python.org/downloads/
    echo Make sure to check "Add Python 3.10 to PATH" during installation
    pause
    exit /b 1
)
echo ✅ Python 3.10 found

echo.
echo [2/4] Creating virtual environment...
if not exist "venv310" (
    py -3.10 -m venv venv310
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo ✅ Virtual environment ready

echo.
echo [3/4] Installing dependencies...
call venv310\Scripts\activate.bat
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    echo Check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ Dependencies installed

echo.
echo [4/4] Configuring OpenAI API...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ⚠️  Created .env file - Edit it with your OpenAI API key!
        echo.
        echo To get your API key:
        echo 1. Visit https://platform.openai.com/api-keys
        echo 2. Create a new API key
        echo 3. Open .env file and replace sk-your-api-key-here with your key
        echo.
    )
) else (
    echo ✅ .env file already exists
)

echo.
echo ========================================
echo   ✅ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your OpenAI API key
echo 2. Run run.bat to start the application
echo 3. Open your browser to http://localhost:8501
echo.
pause
