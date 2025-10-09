# app/services/generation/mapping_service.py
from typing import Dict, List, Any
from app.config.settings import settings

class MappingService:
    
    @staticmethod
    def mapear_texto_a_bd(
        contenido_ia: dict,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int
    ) -> Dict[str, Any]:
        return {
            "Titulo": contenido_ia.get("titulo", "")[:80],
            "Contenido": contenido_ia.get("cuento", "").strip(),
            "ID_Tipo_Texto": id_tipo_texto,
            "ID_Tematica": id_tematica,
            "ID_Dificultad": id_dificultad,
            "ID_Juego": settings.ID_JUEGO_TEXTOS
        }
    
    @staticmethod
    def mapear_preguntas_a_bd(
        preguntas_ia: List[dict],
        id_texto: int,
        id_tipo_pregunta: int,
        id_dificultad: int
    ) -> List[Dict[str, Any]]:
        preguntas_bd = []
        
        for pregunta in preguntas_ia:
            preguntas_bd.append({
                "ID_Texto": id_texto,
                "Contenido": pregunta.get("enunciado", "").strip(),
                "ID_Tipo_Pregunta": id_tipo_pregunta,
                "ID_Dificultad": id_dificultad
            })
        
        return preguntas_bd
    
    @staticmethod
    def mapear_alternativas_a_bd(
        alternativas_ia: List[dict],
        id_pregunta: int
    ) -> List[Dict[str, Any]]:
        alternativas_bd = []
        
        for alternativa in alternativas_ia:
            alternativas_bd.append({
                "ID_Pregunta": id_pregunta,
                "Contenido": alternativa.get("texto", "").strip(),
                "Correcto": bool(alternativa.get("es_correcta", False))
            })
        
        return alternativas_bd