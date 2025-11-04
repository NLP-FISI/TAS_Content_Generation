# app/helper/prompt_builder_helper.py
from typing import List
from app.config.settings import settings


class PromptBuilder:
    
    def __init__(self, catalog_service):
        """
        Inicializa el PromptBuilder con acceso a CatalogService
        para obtener nombres y características desde la BD
        """
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
        """
        Construye UN ÚNICO prompt que genera texto + preguntas juntas.
        
        Args:
            id_grado: ID del grado desde BD
            id_tematica: ID de la temática desde BD
            id_tipo_texto: ID del tipo de texto desde BD
            id_dificultad: ID de la dificultad desde BD
            dificultad_escala: Escala 1-5 para especificar dificultad en texto
            tipos_preguntas: Lista de nombres de tipos de preguntas distribuidos
                            Ej: ["Selección Única", "Comprensión Literal", ...]
        """
        
        # Obtener nombres desde BD (sin hardcoding)
        grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
        tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
        tipo_texto_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
        dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)
        
        # Obtener características del tipo de texto desde BD
        caracteristicas_tipo = self._obtener_caracteristicas_tipo_texto(id_tipo_texto)
        
        # Construir especificación de tipos de preguntas
        especificacion_tipos = "\n".join(
            f"- Pregunta {i+1}: {tipo}" 
            for i, tipo in enumerate(tipos_preguntas)
        )
        
        # Especificación de escala de dificultad
        especificacion_dificultad = self._obtener_especificacion_escala(dificultad_escala)
        
        return f"""Actúa como un experto en redacción de textos para niños y evaluación educativa basada en la Taxonomía de Bloom y las orientaciones del MINEDU.

═══════════════════════════════════════════════════════════════════════════════
📋 ESPECIFICACIONES DEL TEXTO
═══════════════════════════════════════════════════════════════════════════════

Grado: {grado_nombre}º de primaria
Temática: {tematica_nombre}
Tipo de texto: {tipo_texto_nombre}
Características del tipo: {caracteristicas_tipo}

═══════════════════════════════════════════════════════════════════════════════
📊 ESCALA DE DIFICULTAD: {dificultad_escala}/5
═══════════════════════════════════════════════════════════════════════════════

{especificacion_dificultad}

Dificultad seleccionada: {dificultad_nombre} ({dificultad_escala}/5)

═══════════════════════════════════════════════════════════════════════════════
✍️ INSTRUCCIONES PARA EL TEXTO
═══════════════════════════════════════════════════════════════════════════════

1. Genera un texto para un estudiante de {grado_nombre}º de primaria
2. La categoría es "{tematica_nombre}"
3. Tipo de texto: {tipo_texto_nombre}
4. Incluye personajes que vivan la experiencia
5. Usa un lenguaje claro, frases sencillas y vocabulario adecuado al grado
6. Adapta la longitud y complejidad del texto de acuerdo a la dificultad {dificultad_escala}/5
7. Termina con una enseñanza sencilla o reflexión

═══════════════════════════════════════════════════════════════════════════════
❓ INSTRUCCIONES PARA LAS PREGUNTAS
═══════════════════════════════════════════════════════════════════════════════

Genera EXACTAMENTE {settings.PREGUNTAS_POR_TEXTO} preguntas de comprensión lectora.

Distribución de tipos de preguntas:
{especificacion_tipos}

Especificaciones por tipo:
1. **Selección Única**: Elegir la mejor opción de respuesta
2. **Comprensión Literal**: La respuesta se encuentra directamente en el texto
3. **Comprensión Inferencial**: Requiere deducir información no explícita

Cada pregunta debe tener:
- EXACTAMENTE {settings.ALTERNATIVAS_POR_PREGUNTA} alternativas
- SOLO 1 alternativa correcta (es_correcta: true)
- Alternativas incorrectas plausibles (no obviamente falsas)
- Dificultad acorde al nivel {dificultad_escala}/5

═══════════════════════════════════════════════════════════════════════════════
🧠 TAXONOMÍA DE BLOOM - Distribución Equilibrada
═══════════════════════════════════════════════════════════════════════════════

1. **Recordar**: Identificar información explícita o hechos del texto
2. **Comprender**: Interpretar o parafrasear ideas del texto
3. **Aplicar**: Usar información del texto en una situación nueva o práctica
4. **Analizar**: Comparar, clasificar o reconocer relaciones causa-efecto
5. **Evaluar**: Emitir un juicio sobre una acción, decisión o mensaje del texto
6. **Crear**: Proponer un final alternativo o solución diferente a un problema

Adapta los niveles de Bloom al grado {grado_nombre}:
- Grados 1-3: Prioriza Recordar, Comprender y Aplicar
- Grados 4-6: Incluye también Analizar, Evaluar y Crear

═══════════════════════════════════════════════════════════════════════════════
📤 FORMATO DE SALIDA - JSON ESTRICTO
═══════════════════════════════════════════════════════════════════════════════

Devuelve SOLO un bloque JSON válido, sin texto adicional:

{{
  "titulo": "string (máximo 80 caracteres)",
  "cuento": "string (el texto completo)",
  "ensenanza": "string (enseñanza o reflexión)",
  "palabras_aprox": number,
  "preguntas": [
    {{
      "tipo": "Selección Única | Comprensión Literal | Comprensión Inferencial",
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
}}

⚠️ IMPORTANTE: El array "preguntas" debe tener exactamente {settings.PREGUNTAS_POR_TEXTO} elementos
"""

    def _obtener_caracteristicas_tipo_texto(self, id_tipo_texto: int) -> str:
        """
        Obtiene las características del tipo de texto desde BD.
        
        Si la BD no tiene tabla de características, usa valores por defecto.
        Esto mantiene flexibilidad si en futuro se agrega tabla.
        """
        try:
            # Intenta obtener características de la BD (si existe tabla)
            # Por ahora, retorna valores por defecto según el tipo
            tipo_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
            
            caracteristicas = {
                "narrativo": "Incluye personajes con diálogos. Estructura: inicio, desarrollo, final. Genera emociones.",
                "expositivo": "Explica conceptos con claridad. Usa ejemplos concretos. Lenguaje objetivo.",
                "descriptivo": "Describe detalladamente escenas, lugares o elementos. Usa adjetivos precisos.",
                "instructivo": "Pasos claros y ordenados. Usa verbos en imperativo o infinitivo."
            }
            
            return caracteristicas.get(
                tipo_nombre.lower(),
                "Texto educativo claro y estructurado."
            )
        except Exception:
            return "Texto educativo claro y estructurado."
    
    def _obtener_especificacion_escala(self, dificultad_escala: int) -> str:
        """
        Retorna especificación detallada para cada nivel de dificultad 1-5
        """
        especificaciones = {
            1: """NIVEL 1 - MUY FÁCIL
   • Vocabulario muy simple y común
   • Frases cortas (máximo 10 palabras)
   • Conceptos básicos y concretos
   • Preguntas directas y obvias
   • Ideal para primeros grados""",
            
            2: """NIVEL 2 - FÁCIL
   • Vocabulario simple con pocas palabras nuevas
   • Frases medianas (10-15 palabras)
   • Conceptos básicos pero con más detalle
   • Preguntas con respuestas en el texto
   • Ideal para 2-3 primaria""",
            
            3: """NIVEL 3 - MEDIO
   • Vocabulario moderado con palabras nuevas explicadas
   • Frases complejas (15-20 palabras)
   • Conceptos intermedios
   • Algunas preguntas requieren interpretación
   • Ideal para 4 primaria""",
            
            4: """NIVEL 4 - DIFÍCIL
   • Vocabulario avanzado
   • Frases muy complejas (más de 20 palabras)
   • Conceptos abstractos
   • Preguntas que requieren análisis profundo
   • Ideal para 5-6 primaria""",
            
            5: """NIVEL 5 - MUY DIFÍCIL
   • Vocabulario sofisticado y técnico
   • Frases elaboradas con estructura compleja
   • Conceptos abstractos y filosóficos
   • Preguntas que requieren crítica y reflexión
   • Ideal para grados avanzados"""
        }
        
        return especificaciones.get(
            dificultad_escala,
            especificaciones[3]  # Por defecto nivel 3 (medio)
        )