# app/services/generation/mapping_service.py - MÉTODO ACTUALIZADO
# ✅ CAMBIO: Usar dificultad individual por pregunta en lugar de la del texto

from typing import Dict, List, Any
from app.config.settings import settings

class MappingService:

    _id_pregunta_counter = 0
    
    @staticmethod
    def mapear_texto_a_bd(
        contenido_ia: dict,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int,
        id_grado: int
    ) -> Dict[str, Any]:
        """Mapea texto generado por IA al formato de BD"""
        return {
            "titulo": contenido_ia.get("titulo", "")[:80],
            "contenido": contenido_ia.get("cuento", "").strip(),
            "id_tipo_texto": id_tipo_texto,
            "id_tematica": id_tematica,
            "id_dificultad": id_dificultad,
            "id_grado": id_grado,
        }
    
    @staticmethod
    def mapear_preguntas_a_bd(
        preguntas_ia: List[dict],
        id_texto: int,
        id_tipo_pregunta_por_pregunta: List[int],
        id_dificultad_texto: int  # ⚠️ MANTENER para compatibilidad (pero NO se usará)
    ) -> List[Dict[str, Any]]:
        """
        Mapea preguntas generadas por IA al formato de BD.
        
        ✅ CAMBIO: Ahora usa dificultad INDIVIDUAL por pregunta (1-5)
                   en lugar de heredar la dificultad del texto
        
        Args:
            preguntas_ia: Lista de preguntas con "dificultad_pregunta" (1-5)
            id_texto: ID del texto
            id_tipo_pregunta_por_pregunta: Lista de ID de tipos de preguntas
            id_dificultad_texto: ID de dificultad del texto (DEPRECATED)
        
        Returns:
            Lista de preguntas mapeadas con su dificultad individual
        """
        
        if len(preguntas_ia) != len(id_tipo_pregunta_por_pregunta):
            raise ValueError(
                f"Cantidad de preguntas ({len(preguntas_ia)}) no coincide con "
                f"tipos distribuidos ({len(id_tipo_pregunta_por_pregunta)})"
            )
        
        preguntas_bd = []
        MappingService._id_pregunta_counter = 0
        
        for i, pregunta in enumerate(preguntas_ia):
            MappingService._id_pregunta_counter += 1
            
            # ✅ NUEVO: Obtener dificultad INDIVIDUAL de la pregunta
            # Si no existe, asignar progresiva (1, 2, 3, 4, 5)
            dificultad_pregunta = pregunta.get("dificultad_pregunta", i + 1)
            
            # Validar que sea entre 1-5
            if not isinstance(dificultad_pregunta, int) or dificultad_pregunta < 1 or dificultad_pregunta > 5:
                dificultad_pregunta = i + 1  # Fallback: progresiva
            
            preguntas_bd.append({
                "id_texto": id_texto,
                "contenido": pregunta.get("enunciado", "").strip(),
                "id_tipo_pregunta": id_tipo_pregunta_por_pregunta[i],
                "id_dificultad": dificultad_pregunta, 
            })
        
        return preguntas_bd
    
    @staticmethod
    def mapear_alternativas_a_bd(
        alternativas_ia: List[dict],
        id_pregunta: int
    ) -> List[Dict[str, Any]]:
        """Mapea alternativas de preguntas al formato de BD"""
        
        alternativas_bd = []
        
        for alternativa in alternativas_ia:
            alternativas_bd.append({
                "id_pregunta": id_pregunta,
                "contenido": alternativa.get("texto", "").strip(),
                "correcto": bool(alternativa.get("es_correcta", False)),
            })
        
        return alternativas_bd