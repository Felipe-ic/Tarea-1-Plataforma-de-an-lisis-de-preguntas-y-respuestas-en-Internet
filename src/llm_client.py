# llm_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Modelo a usar - usando un modelo más estable
modelo = genai.GenerativeModel("models/gemini-2.0-flash")

def ask_gemini(prompt: str) -> str:
    """
    Envía un prompt a Gemini y retorna la respuesta en texto
    """
    try:
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        # Capturamos el error y devolvemos un mensaje
        return f"[Error Gemini capturado] {e}"
