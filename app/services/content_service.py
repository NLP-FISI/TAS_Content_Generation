# app/services/content_service.py
from typing import Dict, Any, List, Optional
from app.services.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException


class ContentService(BaseService):
    
    def obtener_texto_con_preguntas(
        self,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int
    ) -> Dict[str, Any]:
        try:
            texto = self._buscar_texto(id_tipo_texto, id_tematica, id_dificultad)
            preguntas = self._obtener_preguntas_con_alternativas(texto.ID_Texto)
            
            return {
                "texto": {
                    "id_texto": texto.ID_Texto,
                    "titulo": texto.Titulo,
                    "contenido": texto.Contenido,
                    "id_tipo_texto": texto.ID_Tipo_Texto,
                    "id_tematica": texto.ID_Tematica,
                    "id_dificultad": texto.ID_Dificultad
                },
                "preguntas": preguntas
            }
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener el texto con preguntas",
                details={
                    "id_tipo_texto": id_tipo_texto,
                    "id_tematica": id_tematica,
                    "id_dificultad": id_dificultad,
                    "error": str(e)
                }
            )
    
    def _buscar_texto(
        self,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int
    ):
        Texto = self.get_model("Texto")
        
        if not Texto:
            raise DatabaseException(
                message="Modelo Texto no encontrado en la base de datos",
                details={"modelo": "Texto"}
            )
        
        texto = self.db.query(Texto).filter(
            Texto.ID_Tipo_Texto == id_tipo_texto,
            Texto.ID_Tematica == id_tematica,
            Texto.ID_Dificultad == id_dificultad
        ).first()
        
        if not texto:
            raise ResourceNotFoundException(
                message="No se encontró ningún texto con los criterios especificados",
                details={
                    "id_tipo_texto": id_tipo_texto,
                    "id_tematica": id_tematica,
                    "id_dificultad": id_dificultad
                }
            )
        
        return texto
    
    def _obtener_preguntas_con_alternativas(
        self,
        id_texto: int
    ) -> List[Dict[str, Any]]:
        Pregunta = self.get_model("Pregunta")
        
        if not Pregunta:
            raise DatabaseException(
                message="Modelo Pregunta no encontrado en la base de datos",
                details={"modelo": "Pregunta"}
            )
        
        preguntas = self.db.query(Pregunta).filter(
            Pregunta.ID_Texto == id_texto
        ).all()
        
        preguntas_response = []
        for pregunta in preguntas:
            alternativas = self._obtener_alternativas(pregunta.ID_Pregunta)
            
            preguntas_response.append({
                "id_pregunta": pregunta.ID_Pregunta,
                "contenido": pregunta.Contenido,
                "id_tipo_pregunta": pregunta.ID_Tipo_Pregunta,
                "id_dificultad": pregunta.ID_Dificultad,
                "alternativas": alternativas
            })
        
        return preguntas_response
    
    def _obtener_alternativas(
        self,
        id_pregunta: int
    ) -> List[Dict[str, Any]]:
        Alternativa = self.get_model("Alternativa")
        
        if not Alternativa:
            raise DatabaseException(
                message="Modelo Alternativa no encontrado en la base de datos",
                details={"modelo": "Alternativa"}
            )
        
        alternativas = self.db.query(Alternativa).filter(
            Alternativa.ID_Pregunta == id_pregunta
        ).all()
        
        return [
            {
                "id_alternativa": alt.ID_Alternativa,
                "contenido": alt.Contenido
            }
            for alt in alternativas
        ]