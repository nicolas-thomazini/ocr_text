# Family Search OCR - AI System

Sistema de IA inteligente para análise e melhoria de documentos antigos em italiano, especificamente desenvolvido para pesquisa genealógica.

## 🎯 Propósito

Este projeto utiliza **Inteligência Artificial avançada** para extrair e melhorar a leitura de documentos antigos em italiano, com foco especial em documentos genealógicos. A IA aprende continuamente com correções humanas, tornando-se cada vez mais precisa na interpretação de textos históricos.

## 🚀 Características Principais

- **OCR Inteligente**: Extração de texto com pré-processamento avançado de imagem
- **IA Adaptativa**: Modelo BERT fine-tuned que aprende com cada correção
- **Feedback Loop**: Sistema de aprendizado contínuo baseado em correções humanas
- **Especializado em Italiano Antigo**: Otimizado para documentos históricos italianos
- **API REST Completa**: Interface para upload, processamento e correção
- **Banco de Dados Persistente**: Armazenamento de documentos, correções e modelos

## 🏗️ Arquitetura

### Backend (Python/FastAPI)
- **OCR Service**: Tesseract com pré-processamento de imagem
- **AI Service**: Fine-tuning de BERT italiano
- **Database**: PostgreSQL com SQLAlchemy
- **API**: FastAPI com documentação automática

### Frontend (Em desenvolvimento)
- Interface web moderna para upload e correção
- Visualização de documentos e resultados
- Dashboard de estatísticas da IA

## 📊 Como Funciona

1. **Upload** → Documento antigo é enviado ao sistema
2. **OCR Inteligente** → Texto é extraído com técnicas avançadas de processamento
3. **Correção Humana** → Usuário corrige erros do OCR
4. **Aprendizado da IA** → Modelo aprende com as correções
5. **Melhoria Contínua** → Sistema fica mais preciso para próximos documentos

## 🛠️ Tecnologias

- **Backend**: Python, FastAPI, SQLAlchemy
- **IA/ML**: PyTorch, Transformers, BERT italiano
- **OCR**: Tesseract com pré-processamento OpenCV
- **Database**: PostgreSQL
- **Deploy**: Docker, Docker Compose

## 🚀 Instalação Rápida

### Opção 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone <repository-url>
cd family_search_OCR

# Execute com Docker Compose
cd backend
docker-compose up -d

# Acesse a API
curl http://localhost:8000
```

### Opção 2: Instalação Manual

```bash
# Backend
cd backend
chmod +x setup.sh
./setup.sh

# Configure o banco de dados
createdb family_search_ocr

# Execute
python run.py
```

### 🔐 Segurança

O sistema já vem com uma **secret key criptograficamente segura** gerada automaticamente. Para gerar uma nova:

```bash
cd backend
python generate_secret.py
```

## 📚 Documentação da API

A API estará disponível em: http://localhost:8000
Documentação interativa: http://localhost:8000/docs

### Endpoints Principais

- `POST /documents/upload` - Upload de documentos
- `POST /documents/{id}/process` - Processar OCR
- `POST /corrections/` - Criar correções
- `POST /ai/train` - Treinar modelo de IA
- `POST /ai/predict` - Predizer qualidade de texto

## 🔄 Fluxo de Trabalho

### 1. Primeiro Uso
1. Faça upload de um documento antigo
2. Processe com OCR
3. Corrija os erros encontrados
4. Repita com mais documentos

### 2. Treinamento da IA
1. Após 10+ correções, treine o modelo
2. A IA aprenderá com seus padrões específicos
3. Novos documentos serão processados com maior precisão

### 3. Melhoria Contínua
1. Continue corrigindo quando necessário
2. Retreine periodicamente o modelo
3. Observe a melhoria gradual na precisão

## 🧠 Especificações da IA

- **Modelo Base**: BERT italiano (dbmdz/bert-base-italian-xxl-cased)
- **Task**: Classificação de qualidade de texto
- **Fine-tuning**: Adaptado aos seus documentos específicos
- **Métricas**: Accuracy, F1-score, Precision, Recall

## 📊 Monitoramento

- Logs em tempo real
- Métricas de performance
- Histórico de treinamentos
- Estatísticas de correções

## 🤝 Contribuição

Este projeto está em desenvolvimento ativo. Contribuições são bem-vindas!

## 📝 Licença

Projeto desenvolvido para pesquisa genealógica e preservação de documentos históricos. 