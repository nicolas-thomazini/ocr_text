# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências do Python
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o código da aplicação
COPY backend/ .

# Exponha a porta padrão do FastAPI
EXPOSE 8000

# Comando padrão para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 