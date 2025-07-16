import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
from typing import Tuple, Dict, Any
from app.config import settings
import logging
from skimage import exposure, transform

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        # Configurar Tesseract
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
    def preprocess_image(self, image_path: str, save_debug: bool = True) -> str:
        """
        Pré-processa a imagem para melhorar a qualidade do OCR e salva o resultado se desejado.
        Retorna o caminho da imagem pré-processada.
        """
        # Ler imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Não foi possível ler a imagem: {image_path}")
        # 1. Converter para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 2. Remover ruído
        denoised = cv2.fastNlMeansDenoising(gray, h=15)
        # 3. Ajustar contraste (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(denoised)
        # 4. Binarização adaptativa
        binary = cv2.adaptiveThreshold(
            contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 31, 15
        )
        # 5. Sharpening (nitidez)
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharp = cv2.filter2D(binary, -1, kernel)
        # 6. Redimensionar para altura mínima (ex: 1000px)
        min_height = 1000
        if sharp.shape[0] < min_height:
            scale = min_height / sharp.shape[0]
            sharp = cv2.resize(sharp, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        # 7. Deskew (correção de inclinação)
        from skimage.transform import rotate
        from skimage.filters import threshold_otsu
        import math
        def compute_skew(image):
            edges = cv2.Canny(image, 50, 150)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
            if lines is None:
                return 0
            angles = []
            for line in lines:
                for rho, theta in line:
                    angle = (theta * 180 / np.pi) - 90
                    angles.append(angle)
            if len(angles) == 0:
                return 0
            median_angle = np.median(angles)
            return median_angle
        skew_angle = compute_skew(sharp)
        if abs(skew_angle) > 0.5:
            sharp = rotate(sharp, -skew_angle, resize=False, mode='edge', preserve_range=True).astype(np.uint8)
        # 8. Salvar imagem pré-processada
        pre_dir = os.path.join(os.path.dirname(image_path), 'preprocessed')
        os.makedirs(pre_dir, exist_ok=True)
        preprocessed_path = os.path.join(pre_dir, os.path.basename(image_path))
        if save_debug:
            cv2.imwrite(preprocessed_path, sharp)
        return preprocessed_path
    
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        Extrai texto da imagem usando OCR
        """
        try:
            # Pré-processar imagem e salvar
            preprocessed_path = self.preprocess_image(image_path, save_debug=True)
            processed_image = cv2.imread(preprocessed_path)
            
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
                'word_confidences': data['conf'],
                'preprocessed_path': preprocessed_path
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