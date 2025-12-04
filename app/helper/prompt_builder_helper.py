from typing import List
from app.config.settings import settings


class PromptBuilder:

    def __init__(self, catalog_service):
        self.catalog = catalog_service

    def build_texto_y_preguntas_prompt(
        self,
        id_grado: int,
        id_tematica: int,
        id_tipo_texto: int,
        id_dificultad: int,
        dificultad_escala: int,
        tipos_preguntas: List[str]
    ) -> str:

        grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
        tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
        tipo_texto_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
        dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)

        caracteristicas_tipo = self._obtener_caracteristicas_tipo_texto(id_tipo_texto)

        especificacion_tipos = "\n".join(
            f"- Pregunta {i + 1}: {tipo}"
            for i, tipo in enumerate(tipos_preguntas)
        )

        ciclo_info = self._obtener_informacion_ciclo(id_grado)

        especificacion_dificultad = self._obtener_especificacion_escala_minedu(
            dificultad_escala,
            id_grado
        )

        estrategia_distractores = self._obtener_estrategia_distractores(
            dificultad_escala,
            id_grado
        )

        return f"""Actúa como un experto en redacción de textos para niños peruanos y evaluación educativa basada en la Taxonomía de Bloom y orientaciones del Currículo Nacional MINEDU.

ESPECIFICACIONES DEL TEXTO - EDUCACIÓN PERUANA

Grado: {grado_nombre}º de Educación Primaria
Ciclo: {ciclo_info['ciclo']} ({ciclo_info['rango_grados']})
Temática: {tematica_nombre}
Tipo de texto: {tipo_texto_nombre}

Genera el texto usando solo caracteres ASCII.
No incluyas comillas curvas (“ ” ‘ ’), guiones largos (— –) ni espacios especiales.
Usa únicamente comillas rectas (") y apóstrofes simples (').
Usa solo el guion estándar (-).
No incluyas caracteres Unicode no ASCII.

Características del tipo de texto:
{caracteristicas_tipo}

ENFOQUE PEDAGÓGICO POR CICLO - MINEDU

{ciclo_info['enfoque_clave']}

ESCALA DE DIFICULTAD DEL TEXTO: {dificultad_escala}/5

{especificacion_dificultad}

Dificultad seleccionada: {dificultad_nombre} ({dificultad_escala}/5)

INSTRUCCIONES PARA EL TEXTO

1. Genera un texto para un estudiante de {grado_nombre}º de primaria en Perú
2. Categoría: "{tematica_nombre}"
3. Tipo de texto: {tipo_texto_nombre}
4. Incluye personajes en situaciones que resuenen con la realidad peruana
5. Usa lenguaje claro, frases adecuadas y vocabulario acorde al grado {grado_nombre}
6. Adapta longitud y complejidad según dificultad {dificultad_escala}/5
7. Termina con una enseñanza o reflexión que refuerce valores educativos
8. Evita violencia, discriminación o contenido inapropiado

NOTAS POR CICLO:
• Ciclo II (1º-2º): Vocabulario cotidiano, frases cortas, énfasis en decodificación y comprensión literal
• Ciclo III (3º-4º): Vocabulario en expansión, oraciones complejas, trabajo en inferencias básicas
• Ciclo IV (5º-6º): Vocabulario académico, textos complejos, desarrollo de pensamiento crítico

INSTRUCCIONES PARA LAS PREGUNTAS

Genera EXACTAMENTE {settings.PREGUNTAS_POR_TEXTO} preguntas de comprensión lectora.

Distribución de tipos de preguntas:
{especificacion_tipos}

TIPOS DE PREGUNTAS (DEFINICIONES ACTUALIZADAS):
1. Comprensión Crítica**: Analizar y juzgar información del texto, identificar propósitos, evaluar decisiones, comparar alternativas
2. Comprensión Literal**: Respuesta directa y explícita en el texto, hechos concretos, detalles específicos
3. Comprensión Inferencial**: Deducir información implícita, leer entre líneas, inferir causas, emociones, intenciones

Cada pregunta debe tener:
- EXACTAMENTE {settings.ALTERNATIVAS_POR_PREGUNTA} alternativas
- SOLO 1 alternativa correcta (es_correcta: true)
- Alternativas plausibles y creíbles, NO obvias
- Dificultad acorde al nivel {dificultad_escala}/5

🎯 ESTRATEGIA DE DISTRACTORES CREÍBLES - DIFÍCIL PERO JUSTA

{estrategia_distractores}

PRINCIPIOS GENERALES:
• Los distractores deben ser plausibles
• Evita opciones absurdas
• Usa información cercana pero incorrecta
• Deben requerir comprensión real

FORMATO DE SALIDA - JSON ESTRICTO

Devuelve SOLO un bloque JSON válido:

{{
  "titulo": "string",
  "cuento": "string",
  "ensenanza": "string",
  "palabras_aprox": number,
  "preguntas": [
    {{
      "tipo": "Comprensión Crítica | Comprensión Literal | Comprensión Inferencial",
      "nivel_bloom": "Recordar | Comprender | Aplicar | Analizar | Evaluar | Crear",
      "dificultad_pregunta": 1,
      "enunciado": "string",
      "alternativas": [
        {{"texto": "string", "es_correcta": true}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}}
      ]
    }}
  ]
}}

IMPORTANTE:
- Debe haber EXACTAMENTE {settings.PREGUNTAS_POR_TEXTO} preguntas
- Cada pregunta debe tener dificultad_pregunta: 1, 2, 3, 4 y 5
"""

    def _obtener_caracteristicas_tipo_texto(self, id_tipo_texto: int) -> str:
        try:
            tipo_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)

            caracteristicas = {
                "narrativo": "Incluye personajes y diálogos. Inicio, desarrollo, desenlace.",
                "literario": "Lenguaje artístico, recursos literarios, creatividad.",
                "expositivo": "Explica ideas con claridad y ejemplos.",
                "descriptivo": "Describe lugares, personajes y situaciones con detalle.",
                "informativo": "Presenta hechos de forma objetiva y directa.",
            }

            return caracteristicas.get(
                tipo_nombre.lower(),
                "Texto educativo claro y estructurado según MINEDU."
            )
        except Exception:
            return "Texto educativo claro y estructurado según MINEDU."

    def _obtener_informacion_ciclo(self, id_grado: int) -> dict:
        if id_grado in [1, 2]:
            ciclo = "Ciclo II"
            rango = "1º-2º grado"
            enfoque = "Decodificación y comprensión literal."
        elif id_grado in [3, 4]:
            ciclo = "Ciclo III"
            rango = "3º-4º grado"
            enfoque = "Inferencias básicas y ampliación de vocabulario."
        else:
            ciclo = "Ciclo IV"
            rango = "5º-6º grado"
            enfoque = "Pensamiento crítico y análisis profundo."

        return {
            "ciclo": ciclo,
            "rango_grados": rango,
            "enfoque_clave": f"ENFOQUE {ciclo}: {enfoque}"
        }

    def _obtener_especificacion_escala_minedu(self, dificultad_escala: int, id_grado: int) -> str:
        especificaciones = {
            1: {
                "nombre": "MUY FÁCIL",
                "desc_general": "Texto muy simple.",
                "palabras_aprox": "40-60 palabras",
                "caracteristicas": [
                    "Vocabulario básico",
                    "Frases cortas",
                    "Conceptos concretos"
                ]
            },
            2: {
                "nombre": "FÁCIL",
                "desc_general": "Texto simple pero con algunos matices.",
                "palabras_aprox": "80-120 palabras",
                "caracteristicas": [
                    "Vocabulario simple",
                    "Frases medianas",
                    "Detalles explícitos"
                ]
            },
            3: {
                "nombre": "MEDIO",
                "desc_general": "Requiere inferencias básicas.",
                "palabras_aprox": "150-200 palabras",
                "caracteristicas": [
                    "Frases complejas",
                    "Conceptos intermedios"
                ]
            },
            4: {
                "nombre": "DIFÍCIL",
                "desc_general": "Análisis e interpretación profunda.",
                "palabras_aprox": "200-280 palabras",
                "caracteristicas": [
                    "Vocabulario académico",
                    "Conceptos abstractos"
                ]
            },
            5: {
                "nombre": "MUY DIFÍCIL",
                "desc_general": "Requiere pensamiento crítico.",
                "palabras_aprox": "280-350 palabras",
                "caracteristicas": [
                    "Prosa compleja",
                    "Ideas filosóficas"
                ]
            }
        }

        spec = especificaciones.get(dificultad_escala, especificaciones[3])

        caracteristicas_str = "\n   ".join(f"• {c}" for c in spec["caracteristicas"])

        return f"""NIVEL {dificultad_escala} - {spec['nombre']}

   {caracteristicas_str}

   • Longitud aproximada: {spec['palabras_aprox']}
   • Descripción: {spec['desc_general']}
   • Ideal para: {self._get_grados_ideales(dificultad_escala)}"""

    def _get_grados_ideales(self, dificultad_escala: int) -> str:
        mapeo = {
            1: "1º-2º (Ciclo II)",
            2: "2º-3º (Ciclo II-III)",
            3: "3º-4º (Ciclo III)",
            4: "4º-5º (Ciclo III-IV)",
            5: "5º-6º (Ciclo IV)"
        }
        return mapeo.get(dificultad_escala, "Todos los grados")

    def _obtener_estrategia_distractores(self, dificultad_escala: int, id_grado: int) -> str:

        estrategias = {
            1: """CICLO II - NIVEL 1 (MUY FÁCIL)

• Distractor 1: Correcto pero incompleto
• Distractor 2: Similar pero con inversión de detalles
• Distractor 3: Algo mencionado pero no relacionado""",

            2: """CICLO II-III - NIVEL 2 (FÁCIL)

• Distractor 1: Información aplicada al personaje equivocado
• Distractor 2: Detalles válidos pero no responden la pregunta
• Distractor 3: Emoción o acción opuesta""",

            3: """CICLO III - NIVEL 3 (MEDIO)

• Distractor 1: Inferencia incompleta
• Distractor 2: Causa o efecto alternativo
• Distractor 3: Respuestas lógicas pero no exactas""",

            4: """CICLO III-IV - NIVEL 4 (DIFÍCIL)

• Distractor 1: Interpretación parcialmente correcta
• Distractor 2: Razón secundaria o menos relevante
• Distractor 3: Análisis aplicado fuera de contexto""",

            5: """CICLO IV - NIVEL 5 (MUY DIFÍCIL)

• Distractor 1: Interpretación válida pero desde otro personaje
• Distractor 2: Análisis profundo pero incompleto
• Distractor 3: Conclusión perteneciente a otro nivel cognitivo"""
        }

        return estrategias.get(dificultad_escala, estrategias[3])
