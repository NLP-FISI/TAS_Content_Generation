# app/services/generation/generators/texto_generator.py
# ✅ ACTUALIZADO: Procesa dificultad individual por pregunta (1-5)

from typing import List
from .base_generator import BaseGenerator
from app.helper.prompt_builder_helper import PromptBuilder
from app.exceptions import ValidationException


class TextoGenerator(BaseGenerator):
    
    def __init__(self, prompt_builder: PromptBuilder, api_key=str):
        self.prompt_builder = prompt_builder
        super().__init__(api_key=api_key)

    
    def generar(
        self,
        id_grado: int,
        id_tematica: int,
        id_tipo_texto: int,
        id_dificultad: int,
        dificultad_escala: int,
        tipos_preguntas: List[str],
        api_key: str = None
    ) -> dict:

        
        prompt = self.prompt_builder.build_texto_y_preguntas_prompt(
            id_grado=id_grado,
            id_tematica=id_tematica,
            id_tipo_texto=id_tipo_texto,
            id_dificultad=id_dificultad,
            dificultad_escala=dificultad_escala,
            tipos_preguntas=tipos_preguntas
        )
        
        raw_response = self.call_ai(prompt, api_key=api_key)
        parsed = self.parse_json(raw_response)
        
        if not all(k in parsed for k in ["titulo", "cuento"]):
            raise ValidationException(
                message="La respuesta del modelo no contiene los campos requeridos",
                details={
                    "campos_esperados": ["titulo", "cuento", "ensenanza", "preguntas"],
                    "campos_recibidos": list(parsed.keys())
                }
            )
        
        if "preguntas" not in parsed or not isinstance(parsed["preguntas"], list):
            raise ValidationException(
                message="La respuesta no contiene una lista válida de preguntas",
                details={"estructura_recibida": str(type(parsed.get("preguntas")))}
            )
        
        preguntas = self._procesar_preguntas(parsed["preguntas"])
        
        return {
            "titulo": parsed.get("titulo", ""),
            "cuento": parsed.get("cuento", "").strip(),
            "ensenanza": parsed.get("ensenanza", ""),
            "palabras_aprox": parsed.get("palabras_aprox", 0),
            "preguntas": preguntas
        }
    
    def _procesar_preguntas(self, preguntas: list) -> list:

        from app.config.settings import settings
        
        preguntas_procesadas = []
        
        preguntas = preguntas[:settings.PREGUNTAS_POR_TEXTO]
        
        for i, pregunta in enumerate(preguntas):
            if "alternativas" not in pregunta:
                raise ValidationException(
                    message=f"La pregunta {i+1} no tiene alternativas",
                    details={"pregunta_index": i, "pregunta": str(pregunta)[:100]}
                )
            
            pregunta["dificultad_pregunta"] = i + 1  
            
            pregunta_procesada = self._procesar_alternativas(pregunta)
            preguntas_procesadas.append(pregunta_procesada)
        
        return preguntas_procesadas
    
    def _procesar_alternativas(self, pregunta: dict) -> dict:

        from app.config.settings import settings
        
        alternativas = pregunta.get("alternativas", [])
        alternativas = alternativas[:settings.ALTERNATIVAS_POR_PREGUNTA]
        
        correctas = sum(1 for a in alternativas if a.get("es_correcta"))
        
        if correctas != 1:
            if correctas == 0:
                alternativas[0]["es_correcta"] = True
            else:
                for j, a in enumerate(alternativas):
                    a["es_correcta"] = (j == 0)
        
        pregunta["alternativas"] = alternativas
        return pregunta