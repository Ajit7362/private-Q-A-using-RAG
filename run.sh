#!/bin/bash
# SecureDoc - Launcher for Linux/Mac

echo "========================================"
echo "  SecureDoc - PDF Q&A with OpenAI"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv310" ]; then
    echo "Virtual environment not found. Running setup..."
    bash setup.sh
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

# Activate virtual environment
source venv310/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Could not activate virtual environment"
    exit 1
fi

echo "Checking dependencies..."
pip install -q --upgrade pip setuptools wheel 2>/dev/null
pip install -q -r requirements.txt 2>/dev/null

echo ""
echo "✅ Environment ready! Starting SecureDoc..."
echo ""
echo "🌐 Opening: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Streamlit app
streamlit run app.py
