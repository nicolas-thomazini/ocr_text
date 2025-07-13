import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
from typing import Tuple, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        # Configurar Tesseract
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Pré-processa a imagem para melhorar a qualidade do OCR
        """
        # Ler imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Não foi possível ler a imagem: {image_path}")
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar filtros para melhorar qualidade
        # 1. Redução de ruído
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 2. Equalização de histograma para melhorar contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 3. Binarização adaptativa
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 4. Morfologia para remover ruído
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        Extrai texto da imagem usando OCR
        """
        try:
            # Pré-processar imagem
            processed_image = self.preprocess_image(image_path)
            
            # Configurações do Tesseract para italiano antigo
            custom_config = r'--oem 3 --psm 6 -l ita'
            
            # Extrair texto
            text = pytesseract.image_to_string(
                processed_image, 
                config=custom_config,
                lang=settings.OCR_LANG
            )
            
            # Obter dados de confiança
            data = pytesseract.image_to_data(
                processed_image, 
                config=custom_config,
                lang=settings.OCR_LANG,
                output_type=pytesseract.Output.DICT
            )
            
            # Calcular confiança média
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            # Limpar texto
            cleaned_text = self.clean_text(text)
            
            return {
                'text': cleaned_text,
                'confidence': avg_confidence,
                'raw_text': text,
                'word_confidences': data['conf']
            }
            
        except Exception as e:
            logger.error(f"Erro no OCR: {str(e)}")
            raise
    
    def clean_text(self, text: str) -> str:
        """
        Limpa e normaliza o texto extraído
        """
        # Remover quebras de linha extras
        text = ' '.join(text.split())
        
        # Remover caracteres especiais problemáticos
        text = text.replace('|', 'I')  # Comum em OCR
        text = text.replace('0', 'O')  # Em alguns contextos
        
        # Normalizar espaços
        text = ' '.join(text.split())
        
        return text.strip()
    
    def extract_text_with_confidence(self, image_path: str) -> Tuple[str, float]:
        """
        Versão simplificada que retorna apenas texto e confiança
        """
        result = self.extract_text(image_path)
        return result['text'], result['confidence']
    
    def batch_process(self, image_paths: list) -> list:
        """
        Processa múltiplas imagens em lote
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.extract_text(image_path)
                results.append({
                    'image_path': image_path,
                    'success': True,
                    **result
                })
            except Exception as e:
                results.append({
                    'image_path': image_path,
                    'success': False,
                    'error': str(e)
                })
        
        return results

# Instância global do serviço
ocr_service = OCRService() 