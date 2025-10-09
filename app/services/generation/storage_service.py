# app/services/generation/storage_service.py
from typing import Dict, List, Any
from sqlalchemy.exc import SQLAlchemyError
from app.services.base_service import BaseService
from app.exceptions import DatabaseException

class StorageService(BaseService):
    
    def guardar_texto_completo(
        self,
        texto_data: Dict[str, Any],
        preguntas_data: List[Dict[str, Any]],
        alternativas_por_pregunta: List[List[Dict[str, Any]]]
    ) -> int:
        try:
            Texto = self.get_model("Texto")
            Pregunta = self.get_model("Pregunta")
            Alternativa = self.get_model("Alternativa")
            
            if not all([Texto, Pregunta, Alternativa]):
                raise DatabaseException(
                    message="No se pudieron cargar los modelos necesarios",
                    details={
                        "Texto": Texto is not None,
                        "Pregunta": Pregunta is not None,
                        "Alternativa": Alternativa is not None
                    }
                )
            
            texto_obj = Texto(**texto_data)
            self.db.add(texto_obj)
            self.db.flush()
            
            id_texto = texto_obj.ID_Texto
            
            for i, pregunta_data in enumerate(preguntas_data):
                pregunta_data["ID_Texto"] = id_texto
                pregunta_obj = Pregunta(**pregunta_data)
                self.db.add(pregunta_obj)
                self.db.flush()
                
                id_pregunta = pregunta_obj.ID_Pregunta
                
                for alternativa_data in alternativas_por_pregunta[i]:
                    alternativa_data["ID_Pregunta"] = id_pregunta
                    alternativa_obj = Alternativa(**alternativa_data)
                    self.db.add(alternativa_obj)
            
            self.db.commit()
            
            return id_texto
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(
                message="Error al guardar el texto completo en la base de datos",
                details={"error": str(e)}
            )
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(
                message="Error inesperado al guardar en la base de datos",
                details={"error": str(e)}
            )