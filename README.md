# Family Search OCR - AI System

Intelligent AI system for analyzing and improving ancient Italian documents, specifically developed for genealogical research.

## 🐳 Docker Quickstart

1. Build and start all services:
   ```bash
   docker-compose up --build
   ```

2. Access the services:
   - Frontend: http://localhost:3000
   - Backend (API): http://localhost:8000/docs
   - Database: localhost:5432 (user: postgres, password: postgres)

3. To stop:
   ```bash
   docker-compose down
   ```

---

For more details, see the README files in each service directory.

---

## 🎯 Purpose

This project uses **advanced Artificial Intelligence** to extract and improve the reading of ancient Italian documents, with special focus on genealogical documents. The AI learns continuously from human corrections, becoming increasingly accurate in interpreting historical texts.

## 🚀 Key Features

- **Intelligent OCR**: Text extraction with advanced image preprocessing
- **Adaptive AI**: BERT fine-tuned model that learns from each correction
- **Feedback Loop**: Continuous learning system based on human corrections
- **Specialized in Ancient Italian**: Optimized for Italian historical documents
- **Complete REST API**: Interface for upload, processing and correction
- **Persistent Database**: Storage of documents, corrections and models

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **OCR Service**: Tesseract with image preprocessing
- **AI Service**: Italian BERT fine-tuning
- **Database**: PostgreSQL with SQLAlchemy
- **API**: FastAPI with automatic documentation

### Frontend (In development)
- Modern web interface for upload and correction
- Document and results visualization
- AI statistics dashboard

## 📊 How It Works

1. **Upload** → Ancient document is sent to the system
2. **Intelligent OCR** → Text is extracted with advanced processing techniques
3. **Human Correction** → User corrects OCR errors
4. **AI Learning** → Model learns from corrections
5. **Continuous Improvement** → System becomes more accurate for future documents

## 🛠️ Technologies

- **Backend**: Python, FastAPI, SQLAlchemy
- **AI/ML**: PyTorch, Transformers, Italian BERT
- **OCR**: Tesseract with OpenCV preprocessing
- **Database**: PostgreSQL
- **Deploy**: Docker, Docker Compose

## 🚀 Quick Installation

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd family_search_OCR

# Run with Docker Compose
docker-compose up --build

# Access the API
curl http://localhost:8000
```

### Option 2: Manual Installation

```bash
# Backend
cd backend
chmod +x setup.sh
./setup.sh

# Configure the database
createdb family_search_ocr

# Run
python run.py
```

### 🔐 Security

The system comes with a **cryptographically secure secret key** generated automatically. To generate a new one:

```bash
cd backend
python generate_secret.py
```

## 📚 API Documentation

The API will be available at: http://localhost:8000
Interactive documentation: http://localhost:8000/docs

### Main Endpoints

- `POST /documents/upload` - Upload documents
- `POST /documents/{id}/process` - Process OCR
- `POST /corrections/` - Create corrections
- `POST /ai/train` - Train AI model
- `POST /ai/predict` - Predict text quality

## 🔄 Workflow

### 1. First Use
1. Upload an ancient document
2. Process with OCR
3. Correct found errors
4. Repeat with more documents

### 2. AI Training
1. After 10+ corrections, train the model
2. AI will learn from your specific patterns
3. New documents will be processed with higher accuracy

### 3. Continuous Improvement
1. Continue correcting when necessary
2. Retrain the model periodically
3. Observe gradual improvement in accuracy

## 🧠 AI Specifications

- **Base Model**: Italian BERT (dbmdz/bert-base-italian-xxl-cased)
- **Task**: Text quality classification
- **Fine-tuning**: Adapted to your specific documents
- **Metrics**: Accuracy, F1-score, Precision, Recall

## 📊 Monitoring

- Real-time logs
- Performance metrics
- Training history
- Correction statistics

## 🤝 Contributing

This project is under active development. Contributions are welcome!

## 📝 License

Project developed for genealogical research and preservation of historical documents.
