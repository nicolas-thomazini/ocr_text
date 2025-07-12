from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, Correction, OCRResult
from app.models.schemas import Correction as CorrectionSchema, CorrectionCreate
from app.services.ai_service import ai_service

router = APIRouter(prefix="/corrections", tags=["corrections"])

@router.post("/", response_model=CorrectionSchema)
async def create_correction(
    correction: CorrectionCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma correção para um texto extraído
    """
    # Verificar se o OCR result existe
    ocr_result = db.query(OCRResult).filter(OCRResult.id == correction.ocr_result_id).first()
    if not ocr_result:
        raise HTTPException(status_code=404, detail="Resultado OCR não encontrado")
    
    # Criar correção
    db_correction = Correction(
        document_id=correction.document_id,
        ocr_result_id=correction.ocr_result_id,
        original_text=correction.original_text,
        corrected_text=correction.corrected_text,
        user_id=correction.user_id
    )
    
    db.add(db_correction)
    db.commit()
    db.refresh(db_correction)
    
    return db_correction

@router.get("/", response_model=List[CorrectionSchema])
async def list_corrections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as correções
    """
    corrections = db.query(Correction).offset(skip).limit(limit).all()
    return corrections

@router.get("/{correction_id}", response_model=CorrectionSchema)
async def get_correction(
    correction_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém uma correção específica
    """
    correction = db.query(Correction).filter(Correction.id == correction_id).first()
    if not correction:
        raise HTTPException(status_code=404, detail="Correção não encontrada")
    return correction

@router.get("/document/{document_id}", response_model=List[CorrectionSchema])
async def get_corrections_by_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Lista correções de um documento específico
    """
    corrections = db.query(Correction).filter(Correction.document_id == document_id).all()
    return corrections

@router.delete("/{correction_id}")
async def delete_correction(
    correction_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove uma correção
    """
    correction = db.query(Correction).filter(Correction.id == correction_id).first()
    if not correction:
        raise HTTPException(status_code=404, detail="Correção não encontrada")
    
    db.delete(correction)
    db.commit()
    
    return {"message": "Correção removida com sucesso"} 