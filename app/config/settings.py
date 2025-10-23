# app/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY: str = "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"
    OPENROUTER_MODEL: str = "mistralai/mistral-small-3.2-24b-instruct:free"
    REFERER: str = os.getenv("REFERER", "http://localhost")
    TITLE: str = os.getenv("TITLE", "tas-content-api")
    
    PREGUNTAS_POR_TEXTO: int = 5
    ALTERNATIVAS_POR_PREGUNTA: int = 4
    MAX_TEXTOS_POR_REQUEST: int = 100
    
    GUARDAR_JSON_TEMPORAL: bool = os.getenv("GUARDAR_JSON_TEMPORAL", "true").lower() == "true"
    GUARDAR_JSON_EN_ERROR: bool = True
    
    ID_JUEGO_TEXTOS: int = int(os.getenv("ID_JUEGO_TEXTOS", "1"))
    ID_TIPO_PREGUNTA_DEFAULT: int = int(os.getenv("ID_TIPO_PREGUNTA_DEFAULT", "1"))
    
    @classmethod
    def validate(cls):
        if not cls.OPENROUTER_API_KEY:
            raise SystemExit("Falta OPENROUTER_API_KEY en .env")

settings = Settings()
settings.validate()