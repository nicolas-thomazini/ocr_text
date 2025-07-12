from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from app.config import settings

# Configure engine for SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_path = Column(String, nullable=False)
    processed_path = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, error
    
    # Relacionamentos
    ocr_results = relationship("OCRResult", back_populates="document")
    corrections = relationship("Correction", back_populates="document")

class OCRResult(Base):
    __tablename__ = "ocr_results"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    text_extracted = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=True)
    processing_date = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    document = relationship("Document", back_populates="ocr_results")
    corrections = relationship("Correction", back_populates="ocr_result")

class Correction(Base):
    __tablename__ = "corrections"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    ocr_result_id = Column(Integer, ForeignKey("ocr_results.id"))
    original_text = Column(Text, nullable=False)
    corrected_text = Column(Text, nullable=False)
    correction_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, nullable=True)  # Para tracking de quem fez a correção
    
    # Relacionamentos
    document = relationship("Document", back_populates="corrections")
    ocr_result = relationship("OCRResult", back_populates="corrections")

class ModelTraining(Base):
    __tablename__ = "model_training"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, nullable=False)
    training_date = Column(DateTime, default=datetime.utcnow)
    accuracy_score = Column(Float, nullable=True)
    loss_score = Column(Float, nullable=True)
    training_samples = Column(Integer, nullable=False)
    model_path = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables (commented to avoid connection error)
# Base.metadata.create_all(bind=engine) 