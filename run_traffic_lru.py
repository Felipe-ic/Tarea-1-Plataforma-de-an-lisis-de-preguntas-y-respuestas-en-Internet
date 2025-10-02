from main_lru import process_question, get_cache
import psycopg2, os

# Configuración DB
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "qa_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "db"),
    "port": os.getenv("POSTGRES_PORT", 5432),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_traffic(num_questions=10000):
    for i in range(1, num_questions + 1):
        q_id, question, answer, llm_response, scores = process_question()
        if i % 100 == 0:
            print(f"✅ {i} preguntas procesadas")

def save_cache_metrics():
    cache = get_cache()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cache_metrics (cache_hits, cache_misses, total_requests, hit_rate)
        VALUES (%s, %s, %s, %s)
        """,
        (
            cache.hits,
            cache.misses,
            cache.hits + cache.misses,
            cache.hits / (cache.hits + cache.misses) if (cache.hits + cache.misses) > 0 else 0
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Métricas guardadas: Hits={cache.hits}, Misses={cache.misses}")

if __name__ == "__main__":
    run_traffic()
    save_cache_metrics()
