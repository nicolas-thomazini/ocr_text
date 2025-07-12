from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create application
app = FastAPI(
    title="Family Search OCR - AI System",
    description="AI system for analyzing ancient Italian documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": "Family Search OCR - AI System",
        "version": "1.0.0",
        "description": "AI system for analyzing ancient Italian documents",
        "status": "running",
        "mode": "test (no database)",
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """
    Application health check
    """
    return {"status": "healthy", "message": "System running normally"}

@app.get("/test")
async def test_endpoint():
    """
    Test endpoint
    """
    return {
        "message": "Test working!",
        "config": {
            "upload_dir": "./uploads",
            "model_cache_dir": "./models"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 