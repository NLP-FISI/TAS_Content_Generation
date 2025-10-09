# app/helpers/prompt_builder.py
from typing import Tuple
from app.config.settings import settings

class PromptBuilder:
    
    @staticmethod
    def word_range_for_dificultad(dificultad: str) -> Tuple[int, int]:
        dificultad_lower = dificultad.lower()
        if dificultad_lower == "facil":
            return (100, 200)
        elif dificultad_lower == "media":
            return (200, 300)
        elif dificultad_lower == "dificil":
            return (250, 400)
        else:
            return (150, 250)
    
    @staticmethod
    def get_caracteristicas_tipo_texto(tipo: str) -> str:
        caracteristicas = {
            "narrativo": "Incluye personajes con diálogos. Estructura: inicio, desarrollo, final. Genera emociones.",
            "expositivo": "Explica conceptos con claridad. Usa ejemplos concretos. Lenguaje objetivo.",
            "descriptivo": "Describe detalladamente escenas, lugares o elementos. Usa adjetivos precisos.",
            "instructivo": "Pasos claros y ordenados. Usa verbos en imperativo o infinitivo."
        }
        return caracteristicas.get(tipo.lower(), "Texto educativo claro y estructurado.")
    
    @staticmethod
    def get_indicaciones_dificultad(dificultad: str) -> str:
        indicaciones = {
            "facil": "Oraciones cortas (máx 15 palabras). Vocabulario muy común. Conceptos simples.",
            "media": "Oraciones de longitud moderada. Introduce 1-2 palabras nuevas explicadas en contexto.",
            "dificil": "Oraciones más complejas. Vocabulario amplio. Conceptos que requieren reflexión."
        }
        return indicaciones.get(dificultad.lower(), "Lenguaje claro y apropiado.")
    
    @staticmethod
    def build_texto_prompt(
        tipo_texto_nombre: str,
        tematica_nombre: str,
        dificultad_nombre: str
    ) -> str:
        wmin, wmax = PromptBuilder.word_range_for_dificultad(dificultad_nombre)
        caracteristicas = PromptBuilder.get_caracteristicas_tipo_texto(tipo_texto_nombre)
        indicaciones = PromptBuilder.get_indicaciones_dificultad(dificultad_nombre)
        
        return f"""Actúa como un experto en redacción de textos educativos para niños.

Genera un texto de tipo {tipo_texto_nombre.upper()} sobre el tema "{tematica_nombre}".
Dificultad: {dificultad_nombre.upper()}

Características del tipo {tipo_texto_nombre}:
{caracteristicas}

Indicaciones de dificultad {dificultad_nombre}:
{indicaciones}

Extensión del texto: {wmin}-{wmax} palabras.
Incluye una enseñanza o reflexión final apropiada.

Devuelve JSON estricto con este esquema (sin texto adicional):
{{
  "titulo": "string (máximo 80 caracteres)",
  "cuento": "string (el texto completo)",
  "ensenanza": "string (la enseñanza o reflexión)",
  "palabras_aprox": number
}}"""
    
    @staticmethod
    def get_descripcion_tipo_pregunta(tipo: str) -> str:
        descripciones = {
            "literal": "La respuesta se encuentra directamente en el texto. Ej: ¿Qué hizo el personaje?",
            "inferencial": "Requiere deducir información no explícita. Ej: ¿Por qué actuó así el personaje?",
            "critica": "Requiere opinión fundamentada del lector. Ej: ¿Qué opinas sobre...?",
            "vocabulario": "Significado de palabras en contexto. Ej: ¿Qué significa 'X' en el texto?"
        }
        return descripciones.get(tipo.lower(), "Preguntas de comprensión lectora.")
    
    @staticmethod
    def build_preguntas_prompt(
        texto: str,
        tipo_pregunta_nombre: str,
        dificultad_nombre: str
    ) -> str:
        num_preguntas = settings.PREGUNTAS_POR_TEXTO
        num_alternativas = settings.ALTERNATIVAS_POR_PREGUNTA
        descripcion_tipo = PromptBuilder.get_descripcion_tipo_pregunta(tipo_pregunta_nombre)
        
        return f"""Actúa como un experto en evaluación educativa.

Dado el siguiente texto:

{texto}

Genera EXACTAMENTE {num_preguntas} preguntas de comprensión lectora.
Tipo de preguntas: {tipo_pregunta_nombre.upper()}
Dificultad: {dificultad_nombre.upper()}

{descripcion_tipo}

Cada pregunta debe tener EXACTAMENTE {num_alternativas} alternativas.
SOLO 1 alternativa debe ser correcta (es_correcta: true).
Las alternativas incorrectas deben ser plausibles (no obviamente falsas).

Devuelve JSON estricto con este esquema (sin texto adicional):
{{
  "preguntas": [
    {{
      "enunciado": "string (la pregunta)",
      "alternativas": [
        {{"texto": "string", "es_correcta": true}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}}
      ]
    }}
  ]
}}"""