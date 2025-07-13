#!/bin/bash

echo "🚀 Setting up Family Search OCR Backend..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.8+ first."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Install pip first."
    exit 1
fi

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

echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "⬆️  Updating pip..."
pip install --upgrade pip

echo "📚 Installing dependencies..."
pip install -r requirements.txt

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