# app/services/content/text_loader.py
from typing import List, Dict, Any
from sqlalchemy import select
from app.services.common.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException

class TextLoader(BaseService):
    
    def buscar_disponibles(
        self,
        id_usuario: int,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int,
        id_grado: int,
        cantidad: int,
        textos_asignados_query
    ) -> List[Any]:

        texto_model = self.get_model("texto")
        
        if not texto_model:
            raise DatabaseException(
                message="Modelo texto no encontrado",
                details={"modelo": "texto"}
            )
        
        textos = self.query(texto_model).filter(
            texto_model.id_tipo_texto == id_tipo_texto,
            texto_model.id_tematica == id_tematica,
            texto_model.id_dificultad == id_dificultad,
            texto_model.id_grado == id_grado,
            texto_model.id_texto.notin_(textos_asignados_query)
        ).limit(cantidad).all()
        
        return textos
    
    def obtener_preguntas(self, id_texto: int) -> List[Dict[str, Any]]:
        pregunta_model = self.get_model("pregunta")
        
        if not pregunta_model:
            raise DatabaseException(
                message="Modelo pregunta no encontrado",
                details={"modelo": "pregunta"}
            )
        
        preguntas = self.query(pregunta_model).filter(
            pregunta_model.id_texto == id_texto
        ).all()
        
        preguntas_response = []
        for pregunta in preguntas:
            alternativas = self.obtener_alternativas(pregunta.id_pregunta)
            
            preguntas_response.append({
                "id_pregunta": pregunta.id_pregunta,
                "contenido": pregunta.contenido,
                "alternativas": alternativas
            })
        
        return preguntas_response
    
    def obtener_alternativas(self, id_pregunta: int) -> List[Dict[str, Any]]:
        alternativa_model = self.get_model("alternativa")
        
        if not alternativa_model:
            raise DatabaseException(
                message="Modelo alternativa no encontrado",
                details={"modelo": "alternativa"}
            )
        
        alternativas = self.query(alternativa_model).filter(
            alternativa_model.id_pregunta == id_pregunta
        ).all()
        
        return [
            {
                "id_alternativa": alt.id_alternativa,
                "contenido": alt.contenido
            }
            for alt in alternativas
        ]