# app/services/generation/generators/base_generator.py
import re
import json
from abc import ABC, abstractmethod
from typing import Optional
from app.config.ai_client import AIClient
from app.exceptions import ValidationException

class BaseGenerator(ABC):
    
    def __init__(self, api_key):
        self.ai_client = AIClient(api_key=api_key)
    
    @abstractmethod
    def generar(self, **kwargs) -> dict:
        pass
    
    def parse_json(self, text: str) -> dict:

        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not m:
            raise ValidationException(
                message="La respuesta del modelo no contiene un bloque JSON válido",
                details={"respuesta_raw": text[:200]}
            )
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError as e:
            raise ValidationException(
                message="Error al parsear JSON de la respuesta del modelo",
                details={"error": str(e), "json_extraido": m.group(0)[:200]}
            )
    def call_ai(self, prompt: str, api_key: Optional[str] = None) -> str:
        if api_key:
            self.ai_client.client.api_key = api_key
        return self.ai_client.call(prompt)