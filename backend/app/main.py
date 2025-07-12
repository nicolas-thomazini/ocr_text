from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, Base
from app.api import documents, corrections, ai

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 