from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db, ModelTraining, Correction
from app.models.schemas import ModelTraining as ModelTrainingSchema, TrainingResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/train", response_model=TrainingResponse)
async def train_model(db: Session = Depends(get_db)):
    """
    Treina o modelo de IA com as correções disponíveis
    """
    try:
        # Verificar se há correções suficientes
        corrections_count = db.query(Correction).count()
        if corrections_count < 10:
            raise HTTPException(
                status_code=400, 
                detail=f"Precisamos de pelo menos 10 correções. Atualmente temos {corrections_count}"
            )
        
        # Treinar modelo
        result = ai_service.train_model()
        
        return TrainingResponse(
            message="Modelo treinado com sucesso",
            model_version=result['model_version'],
            accuracy=result['accuracy'],
            samples_used=result['samples_used']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no treinamento: {str(e)}")

@router.post("/predict")
async def predict_text_quality(text: str):
    """
    Prediz a qualidade de um texto extraído
    """
    try:
        result = ai_service.predict_text_quality(text)
        return {
            "text": text,
            "is_correct": result['is_correct'],
            "confidence": result['confidence'],
            "probabilities": result['probabilities']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@router.post("/suggest")
async def suggest_corrections(text: str):
    """
    Sugere correções para um texto
    """
    try:
        suggestions = ai_service.suggest_corrections(text)
        return {
            "original_text": text,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar sugestões: {str(e)}")

@router.get("/models", response_model=List[ModelTrainingSchema])
async def list_models(db: Session = Depends(get_db)):
    """
    Lista todos os modelos treinados
    """
    models = db.query(ModelTraining).all()
    return models

@router.get("/models/active", response_model=ModelTrainingSchema)
async def get_active_model(db: Session = Depends(get_db)):
    """
    Obtém o modelo ativo
    """
    model = db.query(ModelTraining).filter(ModelTraining.is_active == True).first()
    if not model:
        raise HTTPException(status_code=404, detail="Nenhum modelo ativo encontrado")
    return model

@router.post("/models/{model_id}/activate")
async def activate_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """
    Ativa um modelo específico
    """
    # Desativar modelo atual
    db.query(ModelTraining).update({"is_active": False})
    
    # Ativar novo modelo
    model = db.query(ModelTraining).filter(ModelTraining.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    
    model.is_active = True
    db.commit()
    
    return {"message": f"Modelo {model.model_version} ativado com sucesso"}

@router.get("/stats")
async def get_ai_stats(db: Session = Depends(get_db)):
    """
    Obtém estatísticas da IA
    """
    total_corrections = db.query(Correction).count()
    total_models = db.query(ModelTraining).count()
    active_model = db.query(ModelTraining).filter(ModelTraining.is_active == True).first()
    
    return {
        "total_corrections": total_corrections,
        "total_models": total_models,
        "active_model": active_model.model_version if active_model else None,
        "can_train": total_corrections >= 10
    } 