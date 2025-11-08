#!/bin/bash
# Script to run the Ship Route Generator application

echo "🚢 Starting Ship Route Generator..."
echo ""

# Check if streamlit is available
if ! command -v streamlit &> /dev/null && ! python3 -m streamlit --version &> /dev/null
then
    echo "❌ Streamlit is not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

# Run the application
python3 -m streamlit run app.py
