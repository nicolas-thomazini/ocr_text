import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding
)
from datasets import Dataset
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import os
import json
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.database import SessionLocal, Correction, ModelTraining
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()
    
    def load_model(self):
        """
        Carrega o modelo e tokenizer
        """
        try:
            logger.info(f"Carregando modelo: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=settings.MODEL_CACHE_DIR
            )
            
            # Adicionar token especial para padding se não existir
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Carregar modelo para classificação de sequência
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=2,  # Correto/Incorreto
                cache_dir=settings.MODEL_CACHE_DIR
            )
            
            self.model.to(self.device)
            logger.info("Modelo carregado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            raise
    
    def prepare_training_data(self) -> Tuple[Dataset, Dataset]:
        """
        Prepara dados de treinamento a partir das correções no banco
        """
        db = SessionLocal()
        try:
            # Buscar todas as correções
            corrections = db.query(Correction).all()
            
            if len(corrections) < 10:
                raise ValueError("Precisamos de pelo menos 10 correções para treinar o modelo")
            
            # Preparar dados
            texts = []
            labels = []
            
            for correction in corrections:
                # Texto original (incorreto)
                texts.append(correction.original_text)
                labels.append(0)  # Incorreto
                
                # Texto corrigido (correto)
                texts.append(correction.corrected_text)
                labels.append(1)  # Correto
            
            # Dividir em treino e validação
            train_texts, val_texts, train_labels, val_labels = train_test_split(
                texts, labels, test_size=0.2, random_state=42, stratify=labels
            )
            
            # Tokenizar textos
            train_encodings = self.tokenizer(
                train_texts, 
                truncation=True, 
                padding=True, 
                max_length=settings.MAX_SEQUENCE_LENGTH,
                return_tensors="pt"
            )
            
            val_encodings = self.tokenizer(
                val_texts, 
                truncation=True, 
                padding=True, 
                max_length=settings.MAX_SEQUENCE_LENGTH,
                return_tensors="pt"
            )
            
            # Criar datasets
            train_dataset = Dataset.from_dict({
                'input_ids': train_encodings['input_ids'],
                'attention_mask': train_encodings['attention_mask'],
                'labels': train_labels
            })
            
            val_dataset = Dataset.from_dict({
                'input_ids': val_encodings['input_ids'],
                'attention_mask': val_encodings['attention_mask'],
                'labels': val_labels
            })
            
            return train_dataset, val_dataset
            
        finally:
            db.close()
    
    def compute_metrics(self, pred):
        """
        Calcula métricas de avaliação
        """
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    def train_model(self) -> Dict[str, Any]:
        """
        Treina o modelo com as correções disponíveis
        """
        try:
            logger.info("Iniciando treinamento do modelo")
            
            # Preparar dados
            train_dataset, val_dataset = self.prepare_training_data()
            
            # Configurar treinamento
            training_args = TrainingArguments(
                output_dir=f"{settings.MODEL_CACHE_DIR}/checkpoints",
                num_train_epochs=settings.EPOCHS,
                per_device_train_batch_size=settings.BATCH_SIZE,
                per_device_eval_batch_size=settings.BATCH_SIZE,
                warmup_steps=500,
                weight_decay=0.01,
                logging_dir=f"{settings.MODEL_CACHE_DIR}/logs",
                logging_steps=10,
                evaluation_strategy="epoch",
                save_strategy="epoch",
                load_best_model_at_end=True,
                metric_for_best_model="f1",
                greater_is_better=True,
            )
            
            # Data collator
            data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
            
            # Trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                tokenizer=self.tokenizer,
                data_collator=data_collator,
                compute_metrics=self.compute_metrics,
            )
            
            # Treinar
            trainer.train()
            
            # Avaliar
            eval_results = trainer.evaluate()
            
            # Salvar modelo
            model_version = f"v{len(self.get_model_versions()) + 1}"
            model_path = f"{settings.MODEL_CACHE_DIR}/{model_version}"
            trainer.save_model(model_path)
            self.tokenizer.save_pretrained(model_path)
            
            # Salvar no banco
            self.save_training_record(model_version, model_path, eval_results, len(train_dataset))
            
            logger.info(f"Treinamento concluído. Modelo salvo como {model_version}")
            
            return {
                'model_version': model_version,
                'accuracy': eval_results['eval_accuracy'],
                'f1_score': eval_results['eval_f1'],
                'samples_used': len(train_dataset)
            }
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {str(e)}")
            raise
    
    def save_training_record(self, model_version: str, model_path: str, eval_results: Dict, samples_used: int):
        """
        Salva registro do treinamento no banco
        """
        db = SessionLocal()
        try:
            # Desativar modelo anterior
            db.query(ModelTraining).update({"is_active": False})
            
            # Criar novo registro
            training_record = ModelTraining(
                model_version=model_version,
                model_path=model_path,
                accuracy_score=eval_results.get('eval_accuracy', 0.0),
                loss_score=eval_results.get('eval_loss', 0.0),
                training_samples=samples_used,
                is_active=True
            )
            
            db.add(training_record)
            db.commit()
            
        finally:
            db.close()
    
    def get_model_versions(self) -> List[str]:
        """
        Retorna versões dos modelos treinados
        """
        db = SessionLocal()
        try:
            models = db.query(ModelTraining).all()
            return [model.model_version for model in models]
        finally:
            db.close()
    
    def predict_text_quality(self, text: str) -> Dict[str, Any]:
        """
        Prediz a qualidade de um texto extraído
        """
        try:
            # Tokenizar texto
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=settings.MAX_SEQUENCE_LENGTH,
                return_tensors="pt"
            )
            
            # Mover para device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Predição
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=-1)
                prediction = torch.argmax(outputs.logits, dim=-1)
                confidence = torch.max(probabilities, dim=-1)[0]
            
            return {
                'is_correct': bool(prediction.item()),
                'confidence': confidence.item(),
                'probabilities': probabilities.cpu().numpy().tolist()
            }
            
        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}")
            raise
    
    def suggest_corrections(self, text: str) -> List[str]:
        """
        Sugere correções para um texto (implementação básica)
        """
        # Esta é uma implementação básica
        # Em uma versão mais avançada, poderíamos usar:
        # - Modelos de linguagem para gerar sugestões
        # - Regras baseadas em padrões comuns de erro
        # - Dicionário de correções frequentes
        
        suggestions = []
        
        # Correções comuns baseadas em padrões
        common_fixes = {
            '|': 'I',
            '0': 'O',
            '1': 'I',
            '5': 'S',
            '8': 'B'
        }
        
        # Aplicar correções comuns
        for wrong, correct in common_fixes.items():
            if wrong in text:
                suggestions.append(text.replace(wrong, correct))
        
        return suggestions[:5]  # Limitar a 5 sugestões

# Instância global do serviço
ai_service = AIService() 