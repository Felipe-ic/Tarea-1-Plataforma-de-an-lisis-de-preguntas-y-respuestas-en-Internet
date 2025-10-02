# Sistema de Análisis de Preguntas y Respuestas

## Descripción
Sistema distribuido para comparar respuestas generadas por LLM vs respuestas humanas del dataset de Yahoo! Answers.


## Requisitos
- Docker
- Docker Compose
- API Key de Google Gemini (definida en `key.env`)

## Instalación y Ejecución con Docker Compose
```bash
# Construir la imagen
docker-compose build qa-analysis

# Levantar los servicios en segundo plano
docker-compose up -d


### detener servicio
docker-compose down


# Ejecución políticas de caché
python main_lru.py
python main_lfu.py

# Generador de tráfico sintético 
python run_traffic_lru.py
python run_traffic_lfu.py

# Acceder a la base de datos PostgreSQL
docker exec -it qa-analysis-system psql -U postgres -d qa_db

# Abrir bash en el contenedor
docker exec -it qa-analysis-system /bin/bash



