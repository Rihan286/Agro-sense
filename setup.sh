#!/bin/bash

# AgroSense Setup Script
echo "🌱 Setting up AgroSense - AI Plant Disease Detector"
echo "=================================================="

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Create backend virtual environment
echo ""
echo "Creating virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate  # For Unix/Mac
# On Windows use: venv\Scripts\activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
echo ""
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file. Please update with your API keys."
else
    echo "⚠️  .env file already exists"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your API keys"
echo "2. Start backend: cd backend && python app.py"
echo "3. Open frontend: Open frontend/index.html in browser"
echo ""
echo "Or run frontend with Python server:"
echo "cd frontend && python -m http.server 8000"
echo ""
echo "Happy farming! 🌾"
