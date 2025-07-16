from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database import get_db, Document, OCRResult
from app.models.schemas import Document as DocumentSchema, OCRResponse
from app.services.ocr_service import ocr_service
from app.services.ai_service import ai_service
from app.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Faz upload de um documento para processamento
    """
    # Validar tipo de arquivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Apenas arquivos de imagem são aceitos")
    
    # Validar tamanho
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande")
    
    # Salvar arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Criar registro no banco
    document = Document(
        filename=file.filename,
        original_path=file_path,
        status="uploaded"
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document

@router.post("/{document_id}/process", response_model=OCRResponse)
async def process_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Processa um documento com OCR
    """
    # Buscar documento
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    try:
        # Atualizar status
        document.status = "processing"
        db.commit()
        
        # Processar OCR
        ocr_result = ocr_service.extract_text(document.original_path)
        
        # Salvar resultado no banco
        db_result = OCRResult(
            document_id=document.id,
            text_extracted=ocr_result['text'],
            confidence_score=ocr_result['confidence']
        )
        db.add(db_result)
        
        # Atualizar status do documento
        document.status = "completed"
        db.commit()
        
        return OCRResponse(
            text=ocr_result['text'],
            confidence=ocr_result['confidence'],
            document_id=document.id
        )
        
    except Exception as e:
        document.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@router.get("/", response_model=None)
async def list_documents(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Lista todos os documentos (paginado)
    """
    total = db.query(Document).count()
    documents = db.query(Document).offset((page - 1) * limit).limit(limit).all()
    total_pages = (total + limit - 1) // limit if limit else 1
    # Serializar documentos manualmente para garantir compatibilidade
    items = []
    for doc in documents:
        # Buscar o OCRResult mais recente (se existir)
        ocr_result = None
        if hasattr(doc, 'ocr_results') and doc.ocr_results:
            ocr_result = sorted(doc.ocr_results, key=lambda x: x.processing_date or datetime.min, reverse=True)[0]
        items.append({
            'id': str(doc.id),
            'filename': doc.filename,
            'status': doc.status.lower() if doc.status else None,
            'original_path': doc.original_path,
            'processed_path': getattr(doc, 'processed_path', None),
            'upload_date': doc.upload_date.isoformat() if doc.upload_date else None,
            'confidence_score': ocr_result.confidence_score if ocr_result else None,
            'original_text': ocr_result.text_extracted if ocr_result else None,
        })
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': limit,
        'total_pages': total_pages
    }

@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um documento específico
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove um documento
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    # Remover arquivo
    if os.path.exists(document.original_path):
        os.remove(document.original_path)
    
    # Remover do banco
    db.delete(document)
    db.commit()
    
    return {"message": "Documento removido com sucesso"} 