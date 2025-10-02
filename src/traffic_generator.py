# traffic_generator.py
import csv
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "test.csv")

# Columnas del dataset
column_names = ["question_id", "question_text", "question_title", "best_answer_text"]

# Cargar dataset
with open(DATA_PATH, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, fieldnames=column_names)
    dataset = list(reader)

def get_random_question():
    """
    Retorna una pregunta aleatoria del dataset
    """
    row = random.choice(dataset)
    return row["question_id"], row["question_text"], row["best_answer_text"]
