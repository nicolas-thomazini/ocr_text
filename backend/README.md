# Family Search OCR - Backend AI System

AI system for analyzing and improving ancient Italian documents through OCR and machine learning.

## 🚀 Features

- **Advanced OCR**: Text extraction from ancient documents with image preprocessing
- **Adaptive AI**: BERT fine-tuned model that learns from human corrections
- **Feedback Loop**: Correction system that continuously improves the model
- **REST API**: Complete interface for document upload, processing and correction
- **Database**: Persistent storage of documents, corrections and models

## 🏗️ Architecture

### Main Components

1. **OCR Service**: Image processing with Tesseract
2. **AI Service**: Italian BERT model fine-tuning
3. **Database**: PostgreSQL with SQLAlchemy
4. **API**: FastAPI with automatic documentation

### Workflow

1. **Upload** → Document is sent to the system
2. **OCR** → Text is extracted with confidence
3. **Correction** → User corrects OCR errors
4. **Training** → AI learns from corrections
5. **Improvement** → Model becomes more accurate for future documents

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- Tesseract OCR
- CUDA (optional, for GPU)

## 🛠️ Installation

### 1. Clone and configure environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ita
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### 4. Configure database

```bash
# Create PostgreSQL database
createdb family_search_ocr

# Copy configuration file
cp env.example .env

# Edit .env with your settings
```

### 5. Configure environment variables

The `.env` file comes with a secure secret key generated automatically. If you need to generate a new one:

```bash
python generate_secret.py
```

Or manually edit the `.env` file:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost/family_search_ocr
SECRET_KEY=IbUl-MZh4GH-j9uYjjcd7Y6weLJHNQRT0FZYMJ5vEHg
```

## 🚀 Executando

### Desenvolvimento

```bash
python run.py
```

### Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: http://localhost:8000
Documentação: http://localhost:8000/docs

## 📚 Endpoints Principais

### Documentos
- `POST /documents/upload` - Upload de documento
- `POST /documents/{id}/process` - Processar OCR
- `GET /documents/` - Listar documentos
- `GET /documents/{id}` - Obter documento específico

### Correções
- `POST /corrections/` - Criar correção
- `GET /corrections/` - Listar correções
- `GET /corrections/document/{id}` - Correções de um documento

### IA
- `POST /ai/train` - Treinar modelo
- `POST /ai/predict` - Predizer qualidade de texto
- `POST /ai/suggest` - Sugerir correções
- `GET /ai/models` - Listar modelos treinados
- `GET /ai/stats` - Estatísticas da IA

## 🔄 Fluxo de Uso

### 1. Primeiro Uso
```bash
# 1. Upload de documento
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@documento.jpg"

# 2. Processar OCR
curl -X POST "http://localhost:8000/documents/1/process"

# 3. Corrigir erros (via API ou interface)
curl -X POST "http://localhost:8000/corrections/" \
  -H "Content-Type: application/json" \
  -d '{"document_id": 1, "ocr_result_id": 1, "original_text": "texto_errado", "corrected_text": "texto_correto"}'
```

### 2. Treinamento da IA
```bash
# Após 10+ correções, treinar modelo
curl -X POST "http://localhost:8000/ai/train"
```

### 3. Uso da IA Treinada
```bash
# Predizer qualidade de novo texto
curl -X POST "http://localhost:8000/ai/predict" \
  -H "Content-Type: application/json" \
  -d '"texto_para_analisar"'

# Obter sugestões de correção
curl -X POST "http://localhost:8000/ai/suggest" \
  -H "Content-Type: application/json" \
  -d '"texto_com_erros"'
```

## 🧠 Modelo de IA

### Especificações
- **Modelo Base**: BERT italiano (dbmdz/bert-base-italian-xxl-cased)
- **Task**: Classificação binária (correto/incorreto)
- **Fine-tuning**: Com correções específicas dos documentos
- **Métricas**: Accuracy, F1-score, Precision, Recall

### Treinamento
- **Batch Size**: 8
- **Learning Rate**: 2e-5
- **Epochs**: 3
- **Mínimo de amostras**: 10 correções

## 📊 Monitoramento

### Logs
- Logs de aplicação em stdout
- Logs de treinamento em `./models/logs/`

### Métricas
- `GET /ai/stats` - Estatísticas gerais
- `GET /ai/models` - Histórico de modelos

## 🔐 Segurança

### Secret Key
- Uma secret key criptograficamente segura é gerada automaticamente
- Para gerar uma nova: `python generate_secret.py`
- Nunca compartilhe ou commite a secret key em produção
- Use variáveis de ambiente para secrets em produção

### Configurações de Segurança
- **JWT Algorithm**: HS256
- **Token Expiration**: 30 minutos
- **CORS**: Configurado para desenvolvimento (ajuste para produção)

## 🔧 Configuração Avançada

### GPU
Para usar GPU, certifique-se de ter CUDA instalado:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Modelo Customizado
Para usar outro modelo base, edite `MODEL_NAME` no `.env`:
```env
MODEL_NAME=seu/modelo/italiano
```

## 🐛 Troubleshooting

### Erro de Tesseract
```bash
# Verificar instalação
tesseract --version
# Verificar idioma italiano
tesseract --list-langs
```

### Erro de GPU
```bash
# Verificar CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

### Erro de banco
```bash
# Verificar conexão
psql -h localhost -U seu_usuario -d family_search_ocr
```

## 📝 Licença

Este projeto é parte do Family Search OCR System. 