# app/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4-fast:free")
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