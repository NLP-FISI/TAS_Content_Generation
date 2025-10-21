# app/services/generation/ai_generation_service.py
import re
import json
from typing import Dict
from app.config.ai_client import AIClient
from app.helper.prompt_builder_helper import PromptBuilder
from app.config.settings import settings
from app.exceptions import ValidationException

class AIGenerationService:
    
    def __init__(self):
        self.ai_client = AIClient()
        self.prompt_builder = PromptBuilder()
    
    @staticmethod
    def parse_json_from_text(text: str) -> dict:
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
    
    def generar_texto(
        self,
        grado_nombre: str,
        tematica_nombre: str,
        dificultad_nombre: str,
        tipo_pregunta_nombre: str = "literal"
    ) -> dict:
        prompt = self.prompt_builder.build_texto_prompt(
            grado_nombre,
            tematica_nombre,
            dificultad_nombre,
            tipo_pregunta_nombre
        )
        
        raw_response = self.ai_client.call(prompt)
        parsed = self.parse_json_from_text(raw_response)
        
        if not all(k in parsed for k in ["titulo", "cuento"]):
            raise ValidationException(
                message="La respuesta del modelo no contiene los campos requeridos",
                details={"campos_esperados": ["titulo", "cuento"], "campos_recibidos": list(parsed.keys())}
            )
        
        return parsed
    
    def generar_preguntas(
        self,
        texto: str,
        tipo_pregunta_nombre: str,
        dificultad_nombre: str
    ) -> dict:
        prompt = self.prompt_builder.build_preguntas_prompt(
            texto,
            tipo_pregunta_nombre,
            dificultad_nombre
        )
        
        raw_response = self.ai_client.call(prompt)
        parsed = self.parse_json_from_text(raw_response)
        
        if "preguntas" not in parsed or not isinstance(parsed["preguntas"], list):
            raise ValidationException(
                message="La respuesta no contiene una lista válida de preguntas",
                details={"estructura_recibida": str(type(parsed.get("preguntas")))}
            )
        
        preguntas = parsed["preguntas"][:settings.PREGUNTAS_POR_TEXTO]
        
        for i, pregunta in enumerate(preguntas):
            if "alternativas" not in pregunta:
                raise ValidationException(
                    message=f"La pregunta {i+1} no tiene alternativas",
                    details={"pregunta_index": i}
                )
            
            alternativas = pregunta["alternativas"][:settings.ALTERNATIVAS_POR_PREGUNTA]
            correctas = sum(1 for a in alternativas if a.get("es_correcta"))
            
            if correctas != 1:
                if correctas == 0:
                    alternativas[0]["es_correcta"] = True
                else:
                    for j, a in enumerate(alternativas):
                        if j > 0:
                            a["es_correcta"] = False
            
            pregunta["alternativas"] = alternativas
        
        return {"preguntas": preguntas}