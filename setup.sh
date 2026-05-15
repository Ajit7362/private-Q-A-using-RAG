#!/bin/bash
# SecureDoc - Setup Script for Linux/Mac

echo "========================================"
echo "  SecureDoc - Complete Setup"
echo "========================================"
echo ""

echo "[1/4] Checking Python 3.10..."
if ! command -v python3.10 &> /dev/null; then
    echo "Error: Python 3.10 not found!"
    echo "Install Python 3.10 using:"
    echo "  - macOS: brew install python@3.10"
    echo "  - Ubuntu: sudo apt-get install python3.10"
    exit 1
fi
python3.10 --version
echo "✅ Python 3.10 found"

echo ""
echo "[2/4] Creating virtual environment..."
if [ ! -d "venv310" ]; then
    python3.10 -m venv venv310
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi
echo "✅ Virtual environment ready"

echo ""
echo "[3/4] Installing dependencies..."
source venv310/bin/activate
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

echo ""
echo "[4/4] Configuring OpenAI API..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠️  Created .env file - Edit it with your OpenAI API key!"
        echo ""
        echo "To get your API key:"
        echo "1. Visit https://platform.openai.com/api-keys"
        echo "2. Create a new API key"
        echo "3. Edit .env and replace sk-your-api-key-here with your key"
        echo ""
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "========================================"
echo "  ✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Run: source venv310/bin/activate"
echo "3. Run: streamlit run app.py"
echo "4. Open your browser to http://localhost:8501"
echo ""
