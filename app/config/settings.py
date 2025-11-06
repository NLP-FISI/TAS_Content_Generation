# app/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys y configuración
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-small-3.2-24b-instruct:free")
    REFERER: str = os.getenv("REFERER", "http://localhost")
    TITLE: str = os.getenv("TITLE", "tas-content-api")
    DELAY_BETWEEN_API_CALLS: float = float(os.getenv("DELAY_BETWEEN_API_CALLS", "10.0"))
    DELAY_BETWEEN_TEXTS: float = float(os.getenv("DELAY_BETWEEN_TEXTS", "10.0"))

    PREGUNTAS_POR_TEXTO: int = 5
    ALTERNATIVAS_POR_PREGUNTA: int = 4
    MAX_TEXTOS_POR_REQUEST: int = 300
    
    DIFICULTAD_ESCALA_MIN: int = 1
    DIFICULTAD_ESCALA_MAX: int = 5
    
    # Configuración de almacenamiento
    GUARDAR_JSON_TEMPORAL: bool = os.getenv("GUARDAR_JSON_TEMPORAL", "true").lower() == "true"
    GUARDAR_JSON_EN_ERROR: bool = True
    
    # IDs de configuración
    ID_JUEGO_TEXTOS: int = int(os.getenv("ID_JUEGO_TEXTOS", "1"))
    ID_TIPO_PREGUNTA_DEFAULT: int = int(os.getenv("ID_TIPO_PREGUNTA_DEFAULT", "1"))
    
    @classmethod
    def validate(cls):
        if not cls.OPENROUTER_API_KEY:
            raise SystemExit("Falta OPENROUTER_API_KEY en .env")

settings = Settings()
settings.validate()