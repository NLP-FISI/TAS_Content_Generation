from sqlalchemy.orm import Session
from app.models import Alternativa
from typing import List, Dict, Any

class EvaluationService:
    
    @staticmethod
    def evaluar_respuestas(
        db: Session,
        id_texto: int,
        respuestas: List[Dict[str, int]]
    ) -> Dict[str, Any]:
        correctas = 0
        incorrectas = 0
        detalles = []
        
        for respuesta in respuestas:
            resultado = EvaluationService._evaluar_respuesta_individual(
                db, 
                respuesta.get("id_pregunta"), 
                respuesta.get("id_respuesta")
            )
            
            if resultado["es_correcta"]:
                correctas += 1
            else:
                incorrectas += 1
            
            detalles.append(resultado)
        
        total = correctas + incorrectas
        porcentaje = (correctas / total * 100) if total > 0 else 0
        aprobado = porcentaje >= 60
        
        return {
            "correctas": correctas,
            "incorrectas": incorrectas,
            "total": total,
            "porcentaje": round(porcentaje, 2),
            "aprobado": aprobado,
            "detalles": detalles
        }
    
    @staticmethod
    def _evaluar_respuesta_individual(
        db: Session,
        id_pregunta: int,
        id_respuesta: int
    ) -> Dict[str, Any]:
        alternativa = db.query(Alternativa).filter(
            Alternativa.id_respuesta == id_respuesta,
            Alternativa.id_pregunta == id_pregunta
        ).first()
        
        if not alternativa:
            return {
                "id_pregunta": id_pregunta,
                "id_respuesta_usuario": id_respuesta,
                "es_correcta": False,
                "id_respuesta_correcta": None,
                "error": "Respuesta no encontrada"
            }
        
        es_correcta = alternativa.bool
        
        respuesta_correcta = db.query(Alternativa).filter(
            Alternativa.id_pregunta == id_pregunta,
            Alternativa.bool == True
        ).first()
        
        return {
            "id_pregunta": id_pregunta,
            "id_respuesta_usuario": id_respuesta,
            "es_correcta": es_correcta,
            "id_respuesta_correcta": respuesta_correcta.id_respuesta if respuesta_correcta else None
        }