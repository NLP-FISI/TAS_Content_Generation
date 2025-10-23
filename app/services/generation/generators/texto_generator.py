# app/services/generation/generators/texto_generator.py
from .base_generator import BaseGenerator
from app.helper.prompt_builder_helper import PromptBuilder
from app.exceptions import ValidationException

class TextoGenerator(BaseGenerator):
    
    def __init__(self):
        super().__init__()
        self.prompt_builder = PromptBuilder()
    
    def generar(
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
        
        raw_response = self.call_ai(prompt)
        parsed = self.parse_json(raw_response)
        
        # Validar que tenga campos requeridos
        if not all(k in parsed for k in ["titulo", "cuento"]):
            raise ValidationException(
                message="La respuesta del modelo no contiene los campos requeridos",
                details={
                    "campos_esperados": ["titulo", "cuento"],
                    "campos_recibidos": list(parsed.keys())
                }
            )
        
        return parsed