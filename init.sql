-- Script de inicialización de la base de datos
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question_id VARCHAR(50) UNIQUE,  -- <--- Aquí agregamos UNIQUE
    question_text TEXT,
    question_title TEXT,
    best_answer_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS llm_responses (
    id SERIAL PRIMARY KEY,
    question_id VARCHAR(50),
    llm_response TEXT,
    quality_score FLOAT,
    access_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cache_metrics (
    id SERIAL PRIMARY KEY,
    hits INTEGER DEFAULT 0,
    misses INTEGER DEFAULT 0,
    total_requests INTEGER DEFAULT 0,
    hit_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_llm_question_id ON llm_responses(question_id);
CREATE INDEX IF NOT EXISTS idx_created_at ON questions(created_at);
