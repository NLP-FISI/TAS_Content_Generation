# app/services/generation/generators/pregunta_generator.py
from .base_generator import BaseGenerator
from app.helper.prompt_builder_helper import PromptBuilder
from app.config.settings import settings
from app.exceptions import ValidationException

class PreguntaGenerator(BaseGenerator):
    
    def __init__(self):
        super().__init__()
        self.prompt_builder = PromptBuilder()
    
    def generar(
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
        
        raw_response = self.call_ai(prompt)
        parsed = self.parse_json(raw_response)
        
        if "preguntas" not in parsed or not isinstance(parsed["preguntas"], list):
            raise ValidationException(
                message="La respuesta no contiene una lista válida de preguntas",
                details={"estructura_recibida": str(type(parsed.get("preguntas")))}
            )
        
        preguntas = self._procesar_preguntas(parsed["preguntas"])
        
        return {"preguntas": preguntas}
    
    def _procesar_preguntas(self, preguntas: list) -> list:
        preguntas_procesadas = []
        
        preguntas = preguntas[:settings.PREGUNTAS_POR_TEXTO]
        
        for i, pregunta in enumerate(preguntas):
            if "alternativas" not in pregunta:
                raise ValidationException(
                    message=f"La pregunta {i+1} no tiene alternativas",
                    details={"pregunta_index": i}
                )
            
            pregunta_procesada = self._procesar_alternativas(pregunta)
            preguntas_procesadas.append(pregunta_procesada)
        
        return preguntas_procesadas
    
    def _procesar_alternativas(self, pregunta: dict) -> dict:
        alternativas = pregunta["alternativas"][:settings.ALTERNATIVAS_POR_PREGUNTA]
        
        correctas = sum(1 for a in alternativas if a.get("es_correcta"))
        
        if correctas != 1:
            if correctas == 0:
                alternativas[0]["es_correcta"] = True
            else:
                for j, a in enumerate(alternativas):
                    a["es_correcta"] = (j == 0)
        
        pregunta["alternativas"] = alternativas
        return pregunta