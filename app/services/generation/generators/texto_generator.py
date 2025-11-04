# app/services/generation/generators/texto_generator.py
from typing import List
from .base_generator import BaseGenerator
from app.helper.prompt_builder_helper import PromptBuilder
from app.exceptions import ValidationException


class TextoGenerator(BaseGenerator):
    
    def __init__(self, prompt_builder: PromptBuilder):
        """
        Inicializa el generador de textos con PromptBuilder inyectado
        
        Args:
            prompt_builder: Instancia de PromptBuilder con CatalogService
        """
        super().__init__()
        self.prompt_builder = prompt_builder
    
    def generar(
        self,
        id_grado: int,
        id_tematica: int,
        id_tipo_texto: int,
        id_dificultad: int,
        dificultad_escala: int,
        tipos_preguntas: List[str]
    ) -> dict:
        """
        Genera un texto completo (cuento + preguntas) en una sola llamada IA.
        
        Args:
            id_grado: ID del grado desde BD
            id_tematica: ID de la temática desde BD
            id_tipo_texto: ID del tipo de texto desde BD
            id_dificultad: ID de la dificultad desde BD
            dificultad_escala: Escala 1-5 para especificar en prompt
            tipos_preguntas: Lista de nombres de tipos distribuidos
                            Ej: ["Selección Única", "Comprensión Literal", ...]
        
        Returns:
            dict con estructura:
            {
                "titulo": str,
                "cuento": str,
                "ensenanza": str,
                "preguntas": List[dict]
            }
        """
        
        # Construir prompt unificado que genera texto + preguntas
        prompt = self.prompt_builder.build_texto_y_preguntas_prompt(
            id_grado=id_grado,
            id_tematica=id_tematica,
            id_tipo_texto=id_tipo_texto,
            id_dificultad=id_dificultad,
            dificultad_escala=dificultad_escala,
            tipos_preguntas=tipos_preguntas
        )
        
        # Llamar al IA
        raw_response = self.call_ai(prompt)
        
        # Parsear JSON
        parsed = self.parse_json(raw_response)
        
        # Validar estructura básica
        if not all(k in parsed for k in ["titulo", "cuento"]):
            raise ValidationException(
                message="La respuesta del modelo no contiene los campos requeridos",
                details={
                    "campos_esperados": ["titulo", "cuento", "ensenanza", "preguntas"],
                    "campos_recibidos": list(parsed.keys())
                }
            )
        
        # Validar que tenga preguntas
        if "preguntas" not in parsed or not isinstance(parsed["preguntas"], list):
            raise ValidationException(
                message="La respuesta no contiene una lista válida de preguntas",
                details={"estructura_recibida": str(type(parsed.get("preguntas")))}
            )
        
        # Procesar preguntas para garantizar estructura correcta
        preguntas = self._procesar_preguntas(parsed["preguntas"])
        
        return {
            "titulo": parsed.get("titulo", ""),
            "cuento": parsed.get("cuento", "").strip(),
            "ensenanza": parsed.get("ensenanza", ""),
            "palabras_aprox": parsed.get("palabras_aprox", 0),
            "preguntas": preguntas
        }
    
    def _procesar_preguntas(self, preguntas: list) -> list:
        """
        Procesa y valida preguntas de la respuesta IA.
        
        - Limita a PREGUNTAS_POR_TEXTO
        - Valida que cada pregunta tenga alternativas
        - Procesa alternativas (máximo ALTERNATIVAS_POR_PREGUNTA)
        - Garantiza exactamente 1 respuesta correcta por pregunta
        """
        from app.config.settings import settings
        
        preguntas_procesadas = []
        
        # Limitar a cantidad configurada
        preguntas = preguntas[:settings.PREGUNTAS_POR_TEXTO]
        
        for i, pregunta in enumerate(preguntas):
            if "alternativas" not in pregunta:
                raise ValidationException(
                    message=f"La pregunta {i+1} no tiene alternativas",
                    details={"pregunta_index": i, "pregunta": str(pregunta)[:100]}
                )
            
            pregunta_procesada = self._procesar_alternativas(pregunta)
            preguntas_procesadas.append(pregunta_procesada)
        
        return preguntas_procesadas
    
    def _procesar_alternativas(self, pregunta: dict) -> dict:
        """
        Procesa alternativas de una pregunta.
        
        - Limita a ALTERNATIVAS_POR_PREGUNTA
        - Valida que haya exactamente 1 correcta
        - Si no hay correcta, marca la primera
        - Si hay múltiples, ajusta para dejar solo 1
        """
        from app.config.settings import settings
        
        alternativas = pregunta.get("alternativas", [])
        alternativas = alternativas[:settings.ALTERNATIVAS_POR_PREGUNTA]
        
        # Contar cuántas están marcadas como correctas
        correctas = sum(1 for a in alternativas if a.get("es_correcta"))
        
        if correctas != 1:
            if correctas == 0:
                # Si no hay correcta, marcar la primera
                alternativas[0]["es_correcta"] = True
            else:
                # Si hay múltiples, dejar solo la primera como correcta
                for j, a in enumerate(alternativas):
                    a["es_correcta"] = (j == 0)
        
        pregunta["alternativas"] = alternativas
        return pregunta