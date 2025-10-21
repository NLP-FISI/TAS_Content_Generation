# app/services/generation/mapping_service.py
from typing import Dict, List, Any
from app.config.settings import settings

class MappingService:
    
    _id_pregunta_counter = 0
    _id_alternativa_counter = 0
    
    @staticmethod
    def mapear_texto_a_bd(
        contenido_ia: dict,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int,
        id_grado: int
    ) -> Dict[str, Any]:
        return {
            "titulo": contenido_ia.get("titulo", "")[:80],
            "contenido": contenido_ia.get("cuento", "").strip(),
            "id_tipo_texto": id_tipo_texto,
            "id_tematica": id_tematica,
            "id_dificultad": id_dificultad,
            "id_grado": id_grado,
            "id_juego": settings.ID_JUEGO_TEXTOS
        }
    
    @staticmethod
    def mapear_preguntas_a_bd(
        preguntas_ia: List[dict],
        id_texto: int,
        id_tipo_pregunta: int,
        id_dificultad: int
    ) -> List[Dict[str, Any]]:
        preguntas_bd = []
        
        MappingService._id_pregunta_counter = 0
        
        for pregunta in preguntas_ia:
            MappingService._id_pregunta_counter += 1
            
            preguntas_bd.append({
                "id_texto": id_texto,
                "contenido": pregunta.get("enunciado", "").strip(),
                "id_tipo_pregunta": id_tipo_pregunta,
                "id_dificultad": id_dificultad,
                "id": MappingService._id_pregunta_counter  
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
                "id_pregunta": id_pregunta,
                "contenido": alternativa.get("texto", "").strip(),
                "correcto": bool(alternativa.get("es_correcta", False)),
            })
        
        return alternativas_bd