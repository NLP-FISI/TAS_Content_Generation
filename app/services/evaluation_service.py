# app/services/evaluation_service.py
from typing import List, Dict, Any
from app.services.common.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException


class EvaluationService(BaseService):
    
    def verificar_respuestas(
        self,
        respuestas: List[Dict[str, int]]
    ) -> List[Dict[str, Any]]:

        resultados = []
        
        for respuesta in respuestas:
            resultado = self._verificar_respuesta_individual(
                respuesta.get("id_pregunta"), 
                respuesta.get("id_alternativa")
            )
            resultados.append(resultado)
        
        return resultados
    
    def _verificar_respuesta_individual(
        self,
        id_pregunta: int,
        id_alternativa: int
    ) -> Dict[str, Any]:

        try:
            alternativa_model = self.get_model("alternativa")
            
            if not alternativa_model:
                raise DatabaseException(
                    message="Modelo alternativa no encontrado en la base de datos",
                    details={
                        "modelo": "alternativa",
                        "id_pregunta": id_pregunta,
                        "id_alternativa": id_alternativa
                    }
                )
            
            alternativa = self.db.query(alternativa_model).filter(
                alternativa_model.id_alternativa == id_alternativa,
                alternativa_model.id_pregunta == id_pregunta
            ).first()
            
            if not alternativa:
                raise ResourceNotFoundException(
                    message="Alternativa no encontrada para esta pregunta",
                    details={
                        "id_pregunta": id_pregunta,
                        "id_alternativa": id_alternativa
                    }
                )
            
            es_correcta = bool(alternativa.correcto)
            
            return {
                "id_pregunta": id_pregunta,
                "id_alternativa": id_alternativa,
                "es_correcta": es_correcta
            }
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al verificar la respuesta",
                details={
                    "id_pregunta": id_pregunta,
                    "id_alternativa": id_alternativa,
                    "error": str(e)
                }
            )