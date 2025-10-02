# main_lfu.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from src.traffic_generator import get_random_question
from src.cache import LFUCache
from src.llm_client import ask_gemini
from src.scoring import score_responses
import uuid

# Configuración DB
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "qa_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "db"),
    "port": os.getenv("POSTGRES_PORT", 5432),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Inicializar caché LFU
cache = LFUCache(capacity=500)

def get_cache():
    return cache


def process_question():
    # Generar ID único para cada ejecución
    q_id = str(uuid.uuid4())
    
    # Obtener pregunta y respuesta del dataset
    _, question, answer = get_random_question()  # ignoramos ID original

    # Revisar caché
    cached = cache.get(question)
    if cached:
        llm_response = cached
    else:
        llm_response = ask_gemini(question)
        cache.set(question, llm_response)

    # Calcular métricas
    scores = score_responses(llm_response, answer)

    # Guardar en DB
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (question_id, question_text, best_answer_text) VALUES (%s, %s, %s)",
        (q_id, question, answer)
    )
    cur.execute(
        "INSERT INTO llm_responses (question_id, llm_response, quality_score) VALUES (%s, %s, %s)",
        (q_id, llm_response, scores["overall_quality"])
    )
    conn.commit()
    cur.close()
    conn.close()

    return q_id, question, answer, llm_response, scores

if __name__ == "__main__":
    q_id, question, answer, llm_response, scores = process_question()
    print(f"\n[Q{q_id}] {question}")
    print(f"[Dataset Answer] {answer}")
    print(f"[LLM Response] {llm_response}")
    print(f"Score: {scores['overall_quality']:.3f}")
