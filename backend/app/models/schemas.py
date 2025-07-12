from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Document schemas
class DocumentBase(BaseModel):
    filename: str
    status: str = "uploaded"

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    original_path: str
    processed_path: Optional[str] = None
    upload_date: datetime
    
    class Config:
        from_attributes = True

# OCR Result schemas
class OCRResultBase(BaseModel):
    text_extracted: str
    confidence_score: Optional[float] = None

class OCRResultCreate(OCRResultBase):
    document_id: int

class OCRResult(OCRResultBase):
    id: int
    document_id: int
    processing_date: datetime
    
    class Config:
        from_attributes = True

# Correction schemas
class CorrectionBase(BaseModel):
    original_text: str
    corrected_text: str

class CorrectionCreate(CorrectionBase):
    document_id: int
    ocr_result_id: int
    user_id: Optional[int] = None

class Correction(CorrectionBase):
    id: int
    document_id: int
    ocr_result_id: int
    correction_date: datetime
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Model Training schemas
class ModelTrainingBase(BaseModel):
    model_version: str
    training_samples: int
    model_path: str

class ModelTrainingCreate(ModelTrainingBase):
    pass

class ModelTraining(ModelTrainingBase):
    id: int
    training_date: datetime
    accuracy_score: Optional[float] = None
    loss_score: Optional[float] = None
    is_active: bool
    
    class Config:
        from_attributes = True

# API Response schemas
class DocumentWithOCR(Document):
    ocr_results: List[OCRResult] = []
    corrections: List[Correction] = []

class TrainingResponse(BaseModel):
    message: str
    model_version: str
    accuracy: float
    samples_used: int

class OCRResponse(BaseModel):
    text: str
    confidence: float
    document_id: int 