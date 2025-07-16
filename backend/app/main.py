import os
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base, get_db
from app.api import documents, corrections, ai
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar diretório para armazenar imagens pré-processadas
os.makedirs("./uploads/preprocessed", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando aplicação Family Search OCR")
    
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("Encerrando aplicação Family Search OCR")

# Criar aplicação
app = FastAPI(
    title="Family Search OCR - AI System",
    description="Sistema de IA para análise de documentos antigos em italiano",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(documents.router)
app.include_router(corrections.router)
app.include_router(ai.router)

# Após criar a aplicação FastAPI (após app = FastAPI(...))
app.mount(
    "/preprocessed-images",
    StaticFiles(directory="./uploads/preprocessed"),
    name="preprocessed-images"
)

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": "Family Search OCR - AI System",
        "version": "1.0.0",
        "description": "Sistema de IA para análise de documentos antigos em italiano",
        "endpoints": {
            "documents": "/documents",
            "corrections": "/corrections", 
            "ai": "/ai",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """
    Verificação de saúde da aplicação
    """
    return {"status": "healthy", "message": "Sistema funcionando normalmente"}

@app.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Obtém estatísticas gerais do sistema
    """
    try:
        from app.database import Document, OCRResult, Correction
        
        # Total de documentos
        total_documents = db.query(Document).count()
        
        # Documentos processados (com status completed)
        processed_documents = db.query(Document).filter(Document.status == "completed").count()
        
        # Documentos de hoje
        today = datetime.utcnow().date()
        documents_today = db.query(Document).filter(
            Document.upload_date >= today
        ).count()
        
        # Confiança média dos OCRs
        ocr_results = db.query(OCRResult).all()
        if ocr_results:
            average_confidence = sum(result.confidence_score for result in ocr_results) / len(ocr_results)
        else:
            average_confidence = 0.0
        
        # Total de correções
        total_corrections = db.query(Correction).count()
        
        # Precisão da IA (placeholder - pode ser melhorado)
        ai_accuracy = 0.85  # Valor padrão, pode ser calculado baseado no histórico
        
        return {
            "total_documents": total_documents,
            "processed_documents": processed_documents,
            "documents_today": documents_today,
            "average_confidence": average_confidence,
            "total_corrections": total_corrections,
            "ai_accuracy": ai_accuracy
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 