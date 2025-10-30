# app/helpers/prompt_builder.py
from typing import Tuple
from app.config.settings import settings

class PromptBuilder:
        
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
    def build_texto_prompt(
        grado_nombre: str,
        tematica_nombre: str,
        tipo_pregunta_nombre: str = "literal"
    ) -> str:
        
        return f"""Actúa como un experto en redacción de textos para niños y evaluación educativa basada en la Taxonomía de Bloom y las orientaciones del MINEDU.

Genera un texto para un estudiante de {grado_nombre}º de primaria.
La categoría del cuento es "{tematica_nombre}".
Incluye personajes que vivan la experiencia.
Usa un lenguaje claro, frases sencillas y vocabulario adecuado al grado.
Adapta la longitud y complejidad del cuento de acuerdo al grado del estudiante.

Termina con una enseñanza sencilla o reflexión.

Después del cuento, genera EXACTAMENTE {settings.PREGUNTAS_POR_TEXTO} preguntas de comprensión lectora.
Tipo de preguntas: {tipo_pregunta_nombre}
Cada una con EXACTAMENTE {settings.ALTERNATIVAS_POR_PREGUNTA} alternativas y SOLO 1 alternativa correcta.

Las preguntas deben cubrir distintos niveles cognitivos según la Taxonomía de Bloom:
1. **Recordar**: identificar información explícita o hechos del texto.
2. **Comprender**: interpretar o parafrasear ideas del texto.
3. **Aplicar**: usar información del texto en una situación nueva o práctica.
4. **Analizar**: comparar, clasificar o reconocer relaciones causa-efecto.
5. **Evaluar**: emitir un juicio sobre una acción, decisión o mensaje del texto.
6. **Crear**: proponer un final alternativo o solución diferente a un problema del cuento.

Distribuye las preguntas de forma equilibrada entre estos niveles, ajustadas al grado educativo.
Por ejemplo, para grados menores (1°–3°) prioriza recordar, comprender y aplicar; para grados mayores (4°–6°), incluye también analizar, evaluar y crear.

Devuelve la salida en formato JSON ESTRICTO, siguiendo este esquema (sin texto adicional):
{{
  "titulo": "string (<=80 chars)",
  "cuento": "string",
  "ensenanza": "string",
  "palabras_aprox": number,
  "preguntas": [
    {{
      "tipo": "{tipo_pregunta_nombre}",
      "nivel_bloom": "Recordar | Comprender | Aplicar | Analizar | Evaluar | Crear",
      "enunciado": "string",
      "alternativas": [
        {{"texto":"string","es_correcta":bool}},
        {{"texto":"string","es_correcta":bool}},
        {{"texto":"string","es_correcta":bool}},
        {{"texto":"string","es_correcta":bool}}
      ]
    }}
  ]
}}"""
    
    @staticmethod
    def get_descripcion_tipo_pregunta(tipo: str) -> str:
        descripciones = {
            "literal": "La respuesta se encuentra directamente en el texto.",
            "inferencial": "Requiere deducir información no explícita.",
            "critica": "Requiere opinión fundamentada del lector.",
            "vocabulario": "Significado de palabras en contexto.",
        }
        return descripciones.get(tipo.lower(), "Preguntas de comprensión lectora.")
    
    @staticmethod
    def build_preguntas_prompt(
        texto: str,
        tipo_pregunta_nombre: str
    ) -> str:
        num_preguntas = settings.PREGUNTAS_POR_TEXTO
        num_alternativas = settings.ALTERNATIVAS_POR_PREGUNTA
        descripcion_tipo = PromptBuilder.get_descripcion_tipo_pregunta(tipo_pregunta_nombre)
        
        return f"""Actúa como un experto en evaluación educativa basada en la Taxonomía de Bloom.

Dado el siguiente texto:

{texto}

Genera EXACTAMENTE {num_preguntas} preguntas de comprensión lectora.
Tipo de preguntas: {tipo_pregunta_nombre.upper()}
Dificultad: Proporcional a la complejidad del texto.

{descripcion_tipo}

Cada pregunta debe tener EXACTAMENTE {num_alternativas} alternativas.
SOLO 1 alternativa debe ser correcta (es_correcta: true).
Las alternativas incorrectas deben ser plausibles (no obviamente falsas).

Las preguntas deben cubrir distintos niveles cognitivos según la Taxonomía de Bloom:
1. **Recordar**: identificar información explícita o hechos del texto.
2. **Comprender**: interpretar o parafrasear ideas del texto.
3. **Aplicar**: usar información del texto en una situación nueva o práctica.
4. **Analizar**: comparar, clasificar o reconocer relaciones causa-efecto.
5. **Evaluar**: emitir un juicio sobre una acción, decisión o mensaje del texto.
6. **Crear**: proponer un final alternativo o solución diferente a un problema del cuento.

Distribuye las preguntas de forma equilibrada entre estos niveles cognitivos.

Devuelve JSON estricto con este esquema (sin texto adicional):
{{
  "preguntas": [
    {{
      "tipo": "{tipo_pregunta_nombre}",
      "nivel_bloom": "Recordar | Comprender | Aplicar | Analizar | Evaluar | Crear",
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