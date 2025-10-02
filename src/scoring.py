# scoring.py - Sistema de métricas de calidad para comparar respuestas
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Tuple, Dict

class ResponseScorer:
    """
    Clase para evaluar la calidad de respuestas comparando respuestas del LLM 
    con respuestas originales del dataset
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para mejorar la comparación
        """
        if not text:
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales pero mantener espacios
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remover espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def cosine_similarity_score(self, llm_response: str, original_response: str) -> float:
        """
        Calcula la similitud de coseno entre dos respuestas
        Retorna un score entre 0 y 1 (1 = idénticas, 0 = completamente diferentes)
        """
        if not llm_response or not original_response:
            return 0.0
        
        # Preprocesar textos
        llm_clean = self.preprocess_text(llm_response)
        original_clean = self.preprocess_text(original_response)
        
        if not llm_clean or not original_clean:
            return 0.0
        
        try:
            # Vectorizar textos
            vectors = self.vectorizer.fit_transform([llm_clean, original_clean])
            
            # Calcular similitud de coseno
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error calculando similitud de coseno: {e}")
            return 0.0
    
    def jaccard_similarity_score(self, llm_response: str, original_response: str) -> float:
        """
        Calcula la similitud de Jaccard entre dos respuestas
        Retorna un score entre 0 y 1
        """
        if not llm_response or not original_response:
            return 0.0
        
        # Preprocesar y tokenizar
        llm_tokens = set(self.preprocess_text(llm_response).split())
        original_tokens = set(self.preprocess_text(original_response).split())
        
        if not llm_tokens or not original_tokens:
            return 0.0
        
        # Calcular Jaccard
        intersection = len(llm_tokens.intersection(original_tokens))
        union = len(llm_tokens.union(original_tokens))
        
        return intersection / union if union > 0 else 0.0
    
    def length_ratio_score(self, llm_response: str, original_response: str) -> float:
        """
        Calcula la relación de longitudes entre respuestas
        Retorna un score entre 0 y 1 (1 = longitudes similares)
        """
        if not llm_response or not original_response:
            return 0.0
        
        llm_len = len(llm_response.split())
        original_len = len(original_response.split())
        
        if original_len == 0:
            return 0.0
        
        ratio = min(llm_len, original_len) / max(llm_len, original_len)
        return float(ratio)
    
    def comprehensive_score(self, llm_response: str, original_response: str) -> Dict[str, float]:
        """
        Calcula un score comprehensivo combinando múltiples métricas
        """
        cosine_score = self.cosine_similarity_score(llm_response, original_response)
        jaccard_score = self.jaccard_similarity_score(llm_response, original_response)
        length_score = self.length_ratio_score(llm_response, original_response)
        
        # Score ponderado (ajustar pesos según necesidades)
        weighted_score = (
            cosine_score * 0.5 +      # 50% similitud semántica
            jaccard_score * 0.3 +     # 30% superposición léxica
            length_score * 0.2        # 20% similitud de longitud
        )
        
        return {
            'cosine_similarity': cosine_score,
            'jaccard_similarity': jaccard_score,
            'length_ratio': length_score,
            'weighted_score': weighted_score,
            'overall_quality': weighted_score
        }

def score_responses(llm_response: str, original_response: str) -> Dict[str, float]:
    """
    Función de conveniencia para calcular scores de respuestas
    """
    scorer = ResponseScorer()
    return scorer.comprehensive_score(llm_response, original_response)
