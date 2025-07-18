#!/usr/bin/env python3
"""
Script para limpar o cache de processamento do sistema OCR
"""

import os
import shutil
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_cache():
    """
    Limpa o cache de processamento
    """
    try:
        # Limpar diretório de imagens pré-processadas
        preprocessed_dir = "./uploads/preprocessed"
        if os.path.exists(preprocessed_dir):
            for file in os.listdir(preprocessed_dir):
                file_path = os.path.join(preprocessed_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logger.info(f"Arquivo removido: {file_path}")
                except Exception as e:
                    logger.warning(f"Erro ao remover arquivo: {file_path} - {str(e)}")
            
            logger.info("Cache de imagens pré-processadas limpo")
        else:
            logger.info("Diretório de cache não existe")
        
        # Limpar diretório de modelos (opcional)
        models_dir = "./models"
        if os.path.exists(models_dir):
            logger.info("Cache de modelos encontrado (não removido por segurança)")
        
        logger.info("Limpeza de cache concluída com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {str(e)}")
        raise

if __name__ == "__main__":
    clear_cache() 