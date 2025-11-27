# app/services/evaluation_service.py
from typing import List, Dict, Any
from app.services.common.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException
from app.services.generation.guardar_en_bd import GuardarEnBDService
from app.services.generation.catalog_service import CatalogService

import logging

logger = logging.getLogger(__name__)

class EvaluationService(BaseService):
    
    def verificar_respuestas(
        self,
        respuestas: List[Dict[str, int]]
    ) -> List[Dict[str, Any]]:

        resultados = []
        
        for respuesta in respuestas:
            resultado = self._verificar_respuesta_individual(
                respuesta.get("id_pregunta"), 
                respuesta.get("id_alternativa"),
                respuesta.get("id_usuario"),
                respuesta.get("id_juego")
            )
            resultados.append(resultado)
        
        return resultados
    
    def _verificar_respuesta_individual(
        self,
        id_pregunta: int,
        id_alternativa: int,
        id_usuario: int,
        id_juego: int
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

            obtener_id_texto = CatalogService(self.db)
            id_texto = obtener_id_texto.obtener_texto_por_alternativa(id_alternativa=id_alternativa)
            
            logger.info(f"Verificando respuesta: usuario={id_usuario}, juego={id_juego}, texto={id_texto}, pregunta={id_pregunta}, alternativa={id_alternativa}, correcta={es_correcta}")

            guardar_auditoria = GuardarEnBDService(self.db)
            guardar_auditoria.guardar_usuario_auditoria(
                id_usuario=id_usuario,
                id_juego=id_juego,
                id_pregunta=id_pregunta,
                id_texto=id_texto,
                correcto=es_correcta
            )
            if not guardar_auditoria:
                logger.error("No se pudo guardar la auditoría de la respuesta")
                return {
                    "id_pregunta": id_pregunta,
                    "id_alternativa": id_alternativa,
                    "es_correcta": es_correcta
                }
            
            logger.info(
                f"Auditoría guardada para usuario {id_usuario}, "
                f"pregunta {id_pregunta}, alternativa {id_alternativa}, correcto={es_correcta}"
            )

            return {
                "id_pregunta": id_pregunta,
                "id_alternativa": id_alternativa,
                "es_correcta": es_correcta
            }
            
        except (ResourceNotFoundException, DatabaseException):
            raise

        except Exception as e:
            self.db.rollback()
            raise DatabaseException(
                message="Error al verificar la respuesta",
                details={
                    "id_pregunta": id_pregunta,
                    "id_alternativa": id_alternativa,
                    "error": str(e)
                }
            )