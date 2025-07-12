#!/bin/bash

echo "🚀 Setting up Family Search OCR Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Install pip first."
    exit 1
fi

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract not found. Installing..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt update
        sudo apt install -y tesseract-ocr tesseract-ocr-ita
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew não encontrado. Instale Homebrew primeiro."
            exit 1
        fi
        brew install tesseract tesseract-lang
    else
        echo "❌ Operating system not supported. Install Tesseract manually."
        exit 1
    fi
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Installing..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt update
        sudo apt install -y postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install postgresql
        brew services start postgresql
    else
        echo "❌ Operating system not supported. Install PostgreSQL manually."
        exit 1
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Update pip
echo "⬆️  Updating pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating configuration file..."
    cp env.example .env
    echo "✅ .env file created. Edit it with your settings."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p models uploads logs

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your database settings"
echo "2. Create the database: createdb family_search_ocr"
echo "3. Run: python run.py"
echo ""
echo "🌐 The API will be available at: http://localhost:8000"
echo "📖 Documentation: http://localhost:8000/docs" 