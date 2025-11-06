# app/helper/prompt_builder_helper.py
# ✅ VERSIÓN ADAPTADA: Compatible con tu código + contexto MINEDU Perú
# Cambios mínimos pero efectivos

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
        ✅ Adaptado: Agrega contexto MINEDU Perú sin cambiar estructura
        
        Args:
            id_grado: ID del grado desde BD (1-6)
            id_tematica: ID de la temática desde BD
            id_tipo_texto: ID del tipo de texto desde BD
            id_dificultad: ID de la dificultad desde BD
            dificultad_escala: Escala 1-5 para especificar dificultad en texto
            tipos_preguntas: Lista de nombres de tipos de preguntas distribuidos
        """
        
        # Obtener nombres desde BD
        grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
        tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
        tipo_texto_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
        dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)
        
        # Obtener características del tipo de texto
        caracteristicas_tipo = self._obtener_caracteristicas_tipo_texto(id_tipo_texto)
        
        # Construir especificación de tipos de preguntas
        especificacion_tipos = "\n".join(
            f"- Pregunta {i+1}: {tipo}" 
            for i, tipo in enumerate(tipos_preguntas)
        )
        
        # Obtener información del ciclo educativo
        ciclo_info = self._obtener_informacion_ciclo(id_grado)
        
        # Especificación de escala de dificultad (MEJORADA)
        especificacion_dificultad = self._obtener_especificacion_escala_minedu(
            dificultad_escala, 
            id_grado
        )
        
        return f"""Actúa como un experto en redacción de textos para niños peruanos y evaluación educativa basada en la Taxonomía de Bloom y orientaciones del Currículo Nacional MINEDU.

═══════════════════════════════════════════════════════════════════════════════
📋 ESPECIFICACIONES DEL TEXTO - EDUCACIÓN PERUANA
═══════════════════════════════════════════════════════════════════════════════

Grado: {grado_nombre}º de Educación Primaria
Ciclo: {ciclo_info['ciclo']} ({ciclo_info['rango_grados']})
Temática: {tematica_nombre}
Tipo de texto: {tipo_texto_nombre}

Características del tipo de texto:
{caracteristicas_tipo}

═══════════════════════════════════════════════════════════════════════════════
🎯 ENFOQUE PEDAGÓGICO POR CICLO - MINEDU
═══════════════════════════════════════════════════════════════════════════════

{ciclo_info['enfoque_clave']}

═══════════════════════════════════════════════════════════════════════════════
📊 ESCALA DE DIFICULTAD DEL TEXTO: {dificultad_escala}/5
═══════════════════════════════════════════════════════════════════════════════

{especificacion_dificultad}

Dificultad seleccionada: {dificultad_nombre} ({dificultad_escala}/5)

═══════════════════════════════════════════════════════════════════════════════
✍️ INSTRUCCIONES PARA EL TEXTO
═══════════════════════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════════════════════
❓ INSTRUCCIONES PARA LAS PREGUNTAS
═══════════════════════════════════════════════════════════════════════════════

Genera EXACTAMENTE {settings.PREGUNTAS_POR_TEXTO} preguntas de comprensión lectora.

Distribución de tipos de preguntas:
{especificacion_tipos}

Especificaciones:
1. **Selección Única**: Elegir la mejor opción de respuesta
2. **Comprensión Literal**: Respuesta directa en el texto
3. **Comprensión Inferencial**: Requiere deducir información implícita

Cada pregunta debe tener:
- EXACTAMENTE {settings.ALTERNATIVAS_POR_PREGUNTA} alternativas
- SOLO 1 alternativa correcta (es_correcta: true)
- Alternativas plausibles pero claramente incorrectas
- Dificultad acorde al nivel {dificultad_escala}/5

═══════════════════════════════════════════════════════════════════════════════
🧠 TAXONOMÍA DE BLOOM - Distribución Equilibrada
═══════════════════════════════════════════════════════════════════════════════

1. **Recordar**: Identificar información explícita
2. **Comprender**: Interpretar o parafrasear ideas
3. **Aplicar**: Usar información en nueva situación
4. **Analizar**: Comparar, clasificar, relaciones causa-efecto
5. **Evaluar**: Emitir juicios sobre acciones o decisiones
6. **Crear**: Proponer soluciones o finales alternativos

Prioriza según ciclo:
- Ciclo II: Recordar, Comprender, Aplicar
- Ciclo III: Recordar, Comprender, Aplicar, Analizar
- Ciclo IV: Todos los niveles, énfasis en Analizar, Evaluar, Crear

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
      "dificultad_pregunta": 1,
      "enunciado": "string (la pregunta)",
      "alternativas": [
        {{"texto": "string", "es_correcta": true}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}},
        {{"texto": "string", "es_correcta": false}}
      ]
    }},
    ... (repite para las demás preguntas con dificultad_pregunta incrementando: 2, 3, 4, 5)
  ]
}}

⚠️ IMPORTANTE: 
- El array "preguntas" debe tener exactamente {settings.PREGUNTAS_POR_TEXTO} elementos
- CADA pregunta DEBE tener "dificultad_pregunta" con valor: 1, 2, 3, 4, 5
"""

    def _obtener_caracteristicas_tipo_texto(self, id_tipo_texto: int) -> str:
        """
        Obtiene características del tipo de texto.
        ✅ MEJORA: Agregados 5 tipos nuevos (argumentativo, dialogado, informativo, poético, literario)
        """
        try:
            tipo_nombre = self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
            
            # CARACTERÍSTICAS MEJORADAS - 9 tipos en total
            caracteristicas = {
                "narrativo": "Incluye personajes con diálogos. Estructura: inicio, desarrollo, desenlace. Genera emociones. Desarrolla comprensión literal e inferencial.",
                
                "literario": "Obra de carácter artístico. Lenguaje figurado y creativo. Usa recursos estilísticos. Desarrolla sensibilidad estética y pensamiento crítico.",
                
                "expositivo": "Explica conceptos e ideas con claridad. Usa ejemplos concretos y contextos reales. Lenguaje objetivo. Desarrolla síntesis y análisis.",
                
                "descriptivo": "Describe detalladamente escenas, lugares, personajes o elementos. Usa adjetivos precisos y comparaciones. Enriquece vocabulario.",
                
                "instructivo": "Pasos claros y ordenados. Usa verbos en imperativo o infinitivo. Lenguaje preciso. Desarrolla seguimiento de secuencias.",
                
                "argumentativo": "Presenta argumentos para convencer. Incluye tesis y conclusiones. Usa evidencia y ejemplos. Desarrolla pensamiento crítico y evaluativo.",
                
                "dialogado": "Conversación entre personajes. Usa guiones o comillas. Interacción directa. Desarrolla comprensión de intenciones y emociones.",
                
                "informativo": "Presenta hechos y datos. Lenguaje claro y directo. Sin opiniones personales. Desarrolla síntesis de información.",
                
                "poético": "Expresión artística con ritmo y musicalidad. Usa figuras literarias. Genera sensaciones y emociones. Desarrolla sensibilidad creativa."
            }
            
            return caracteristicas.get(
                tipo_nombre.lower(),
                "Texto educativo claro y estructurado según estándares MINEDU."
            )
        except Exception:
            return "Texto educativo claro y estructurado según estándares MINEDU."
    
    def _obtener_informacion_ciclo(self, id_grado: int) -> dict:
        """
        Retorna información del ciclo educativo según MINEDU Perú.
        ✅ NUEVA FUNCIÓN: Calcula ciclo automáticamente
        """
        # Calcular ciclo basado en grado
        if id_grado in [1, 2]:
            ciclo = "Ciclo II"
            rango = "1º-2º grado"
            enfoque = "Decodificación y comprensión literal. Énfasis en fluidez lectora y motivación."
        elif id_grado in [3, 4]:
            ciclo = "Ciclo III"
            rango = "3º-4º grado"
            enfoque = "Transición a comprensión inferencial. Ampliar vocabulario y relaciones de causa-efecto."
        else:  # 5, 6
            ciclo = "Ciclo IV"
            rango = "5º-6º grado"
            enfoque = "Pensamiento crítico, análisis profundo y evaluación. Desarrollo de argumentación."
        
        return {
            "ciclo": ciclo,
            "rango_grados": rango,
            "enfoque_clave": f"ENFOQUE {ciclo}: {enfoque}"
        }
    
    def _obtener_especificacion_escala_minedu(self, dificultad_escala: int, id_grado: int) -> str:
        """
        Retorna especificación detallada para cada nivel 1-5.
        ✅ MEJORA: Adapta especificaciones al grado específico
        """
        # Definir especificaciones base para cada nivel
        especificaciones_base = {
            1: {
                "nombre": "MUY FÁCIL",
                "desc_general": "Vocabulario muy simple, frases cortas, conceptos concretos, preguntas directas",
                "palabras_aprox": "40-60 palabras",
                "caracteristicas": [
                    "Máximo 1-2 palabras nuevas (explicadas en contexto)",
                    "Frases cortas (5-8 palabras)",
                    "Estructura sencilla: sujeto + verbo + complemento",
                    "Conceptos muy concretos y cercanos a la experiencia",
                    "Preguntas sobre información exactamente tal como aparece"
                ]
            },
            2: {
                "nombre": "FÁCIL",
                "desc_general": "Vocabulario simple, frases medianas, conceptos básicos, respuestas en el texto",
                "palabras_aprox": "80-120 palabras",
                "caracteristicas": [
                    "2-3 palabras nuevas (definidas por contexto)",
                    "Frases medianas (8-12 palabras)",
                    "Oraciones simples y coordinadas con 'y', 'pero', 'entonces'",
                    "Conceptos básicos con algo de detalle",
                    "Preguntas sobre hechos directamente en el texto"
                ]
            },
            3: {
                "nombre": "MEDIO",
                "desc_general": "Vocabulario moderado, frases complejas, conceptos intermedios, requiere inferencias",
                "palabras_aprox": "150-200 palabras",
                "caracteristicas": [
                    "4-5 palabras nuevas (con apoyo contextual)",
                    "Frases complejas (12-18 palabras)",
                    "Oraciones subordinadas simples (causa-efecto, temporales)",
                    "Conceptos que requieren cierta abstracción",
                    "Preguntas que requieren inferencias: ¿por qué?, ¿qué significa?"
                ]
            },
            4: {
                "nombre": "DIFÍCIL",
                "desc_general": "Vocabulario académico, frases elaboradas, conceptos abstractos, análisis profundo",
                "palabras_aprox": "200-280 palabras",
                "caracteristicas": [
                    "5-7 palabras nuevas/académicas",
                    "Frases elaboradas (15-22 palabras)",
                    "Oraciones subordinadas complejas",
                    "Conceptos más abstractos",
                    "Preguntas que requieren análisis: relaciones, comparaciones, intenciones"
                ]
            },
            5: {
                "nombre": "MUY DIFÍCIL",
                "desc_general": "Vocabulario sofisticado, prosa compleja, conceptos filosóficos, pensamiento crítico",
                "palabras_aprox": "280-350 palabras",
                "caracteristicas": [
                    "7+ palabras académicas/técnicas",
                    "Frases muy complejas (22+ palabras con múltiples cláusulas)",
                    "Estructura de prosa sofisticada",
                    "Conceptos abstractos y filosóficos",
                    "Preguntas que requieren evaluación y crítica"
                ]
            }
        }
        
        # Obtener especificación base
        spec = especificaciones_base.get(dificultad_escala, especificaciones_base[3])
        
        # Construir respuesta formateada
        caracteristicas_str = "\n   ".join([f"• {c}" for c in spec["caracteristicas"]])
        
        return f"""NIVEL {dificultad_escala} - {spec['nombre']}
   
{caracteristicas_str}
   
   • Longitud aproximada: {spec['palabras_aprox']}
   • Descripción: {spec['desc_general']}
   • Ideal para: Grados {self._get_grados_ideales(dificultad_escala)}"""
    
    def _get_grados_ideales(self, dificultad_escala: int) -> str:
        """Helper para indicar grados ideales según dificultad"""
        mapeo = {
            1: "1º-2º (Ciclo II)",
            2: "2º-3º (Ciclo II-III)",
            3: "3º-4º (Ciclo III)",
            4: "4º-5º (Ciclo III-IV)",
            5: "5º-6º (Ciclo IV)"
        }
        return mapeo.get(dificultad_escala, "Todos los grados")