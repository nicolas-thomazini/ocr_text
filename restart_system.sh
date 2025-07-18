#!/bin/bash

echo "=== Reiniciando Sistema Family Search OCR ==="

echo "Parando containers..."
docker-compose down

echo "Limpando cache..."
if [ -d "backend/uploads/preprocessed" ]; then
    rm -rf backend/uploads/preprocessed/*
    echo "Cache limpo"
else
    echo "Diretório de cache não encontrado"
fi

echo "Reconstruindo containers..."
docker-compose build --no-cache

echo "Iniciando containers..."
docker-compose up -d

echo "Aguardando inicialização..."
sleep 10

echo "Verificando status dos containers..."
docker-compose ps

echo "=== Sistema reiniciado com sucesso ==="
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Documentação: http://localhost:8000/docs" 