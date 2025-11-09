#!/bin/bash
# FitTrack AI - Environment Setup Script
# Run this script to set up your environment with the Groq API key

echo "🚀 FitTrack AI - Environment Setup"
echo "=================================="
echo ""

# Load API key from config file if it exists
if [ -f ".env" ]; then
    source .env
    echo "✅ Loaded API key from .env file"
elif [ -f "api_key.txt" ]; then
    export GROQ_API_KEY=$(cat api_key.txt)
    echo "✅ Loaded API key from api_key.txt"
else
    # Fallback: Set default demo API key (REPLACE WITH YOUR OWN FOR PRODUCTION)
    export GROQ_API_KEY="your_groq_api_key_here"
    echo "⚠️  Using placeholder API key"
    echo "📝 To use your own key:"
    echo "   - Create .env file with: export GROQ_API_KEY='your_key'"
    echo "   - Or create api_key.txt with just the key"
    echo "   - Or export GROQ_API_KEY='your_key' before running"
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

# Verify API key is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY not set"
    exit 1
else
    echo "✅ GROQ_API_KEY configured"
fi

echo ""
echo "🎉 Setup complete! Now run:"
echo "   python app.py"
echo ""
echo "Or run everything in one command:"
echo "   source setup_env.sh && python app.py"
echo ""

