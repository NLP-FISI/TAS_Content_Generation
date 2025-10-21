# app/services/content_service.py
from typing import Dict, Any, List, Optional
from app.services.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException


class ContentService(BaseService):
    
    def obtener_textos_disponibles(
        self,
        id_usuario: int,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int,
        cantidad: int = 1
    ) -> Dict[str, Any]:
        """
        Obtiene textos disponibles para un usuario específico.
        
        Flujo:
        1. Obtener el grado del usuario
        2. Buscar textos que NO hayan sido asignados al usuario
        3. Guardar la asignación en usuario_texto
        4. Retornar los textos con sus preguntas
        """
        try:
            # Paso 1: Obtener grado del usuario
            id_grado = self._obtener_grado_usuario(id_usuario)
            
            # Paso 2: Buscar textos disponibles (sin asignar)
            textos_disponibles = self._buscar_textos_disponibles(
                id_usuario=id_usuario,
                id_tipo_texto=id_tipo_texto,
                id_tematica=id_tematica,
                id_dificultad=id_dificultad,
                id_grado=id_grado,
                cantidad=cantidad
            )
            
            if not textos_disponibles:
                raise ResourceNotFoundException(
                    message="No hay textos disponibles con los criterios especificados",
                    details={
                        "id_usuario": id_usuario,
                        "id_tipo_texto": id_tipo_texto,
                        "id_tematica": id_tematica,
                        "id_dificultad": id_dificultad,
                        "id_grado": id_grado
                    }
                )
            
            # Paso 3: Procesar cada texto y guardar asignación
            textos_con_preguntas = []
            for texto in textos_disponibles:
                # Obtener preguntas del texto
                preguntas = self._obtener_preguntas_con_alternativas(texto.id_texto)
                
                # Guardar asignación en usuario_texto
                self._guardar_usuario_texto(id_usuario, texto.id_texto)
                
                # Construir respuesta con preguntas anidadas
                textos_con_preguntas.append({
                    "id_texto": texto.id_texto,
                    "titulo": texto.titulo,
                    "contenido": texto.contenido,
                    "preguntas": preguntas
                })
            
            return {
                "textos_obtenidos": len(textos_con_preguntas),
                "textos": textos_con_preguntas
            }
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener textos disponibles",
                details={
                    "id_usuario": id_usuario,
                    "id_tipo_texto": id_tipo_texto,
                    "id_tematica": id_tematica,
                    "id_dificultad": id_dificultad,
                    "error": str(e)
                }
            )
    
    def _obtener_grado_usuario(self, id_usuario: int) -> int:
        """Obtiene el grado del usuario desde la tabla usuario"""
        usuario_model = self.get_model("usuario")
        
        if not usuario_model:
            raise DatabaseException(
                message="Modelo usuario no encontrado en la base de datos",
                details={"modelo": "usuario"}
            )
        
        usuario = self.db.query(usuario_model).filter(
            usuario_model.id_usuario == id_usuario
        ).first()
        
        if not usuario:
            raise ResourceNotFoundException(
                message="Usuario no encontrado",
                details={"id_usuario": id_usuario}
            )
        
        # Obtener id_grado del usuario
        id_grado = getattr(usuario, 'id_grado', None)
        
        if id_grado is None:
            raise DatabaseException(
                message="El usuario no tiene un grado asignado",
                details={"id_usuario": id_usuario}
            )
        
        return id_grado
    
    def _buscar_textos_disponibles(
        self,
        id_usuario: int,
        id_tipo_texto: int,
        id_tematica: int,
        id_dificultad: int,
        id_grado: int,
        cantidad: int
    ) -> List[Any]:
        """
        Busca textos que cumplan los criterios y NO hayan sido asignados al usuario
        """
        texto_model = self.get_model("texto")
        usuario_texto_model = self.get_model("usuario_texto")
        
        if not texto_model:
            raise DatabaseException(
                message="Modelo texto no encontrado en la base de datos",
                details={"modelo": "texto"}
            )
        
        if not usuario_texto_model:
            raise DatabaseException(
                message="Modelo usuario_texto no encontrado en la base de datos",
                details={"modelo": "usuario_texto"}
            )
        
        # Subquery para obtener los textos ya asignados al usuario
        textos_asignados = self.db.query(usuario_texto_model.id_texto).filter(
            usuario_texto_model.id_usuario == id_usuario
        ).subquery()
        
        # Buscar textos que cumplan criterios y NO estén asignados
        textos = self.db.query(texto_model).filter(
            texto_model.id_tipo_texto == id_tipo_texto,
            texto_model.id_tematica == id_tematica,
            texto_model.id_dificultad == id_dificultad,
            texto_model.id_grado == id_grado,
            texto_model.id_texto.notin_(textos_asignados)
        ).limit(cantidad).all()
        
        return textos
    
    def _guardar_usuario_texto(self, id_usuario: int, id_texto: int) -> None:
        """Guarda la relación usuario-texto en la tabla intermedia"""
        usuario_texto_model = self.get_model("usuario_texto")
        
        if not usuario_texto_model:
            raise DatabaseException(
                message="Modelo usuario_texto no encontrado en la base de datos",
                details={"modelo": "usuario_texto"}
            )
        
        try:
            # Crear nuevo registro
            usuario_texto = usuario_texto_model(
                id_usuario=id_usuario,
                id_texto=id_texto
            )
            self.db.add(usuario_texto)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(
                message="Error al guardar la asignación usuario-texto",
                details={
                    "id_usuario": id_usuario,
                    "id_texto": id_texto,
                    "error": str(e)
                }
            )
    
    def _obtener_preguntas_con_alternativas(
        self,
        id_texto: int
    ) -> List[Dict[str, Any]]:
        """Obtiene preguntas y alternativas de un texto"""
        pregunta_model = self.get_model("pregunta")
        
        if not pregunta_model:
            raise DatabaseException(
                message="Modelo pregunta no encontrado en la base de datos",
                details={"modelo": "pregunta"}
            )
        
        preguntas = self.db.query(pregunta_model).filter(
            pregunta_model.id_texto == id_texto
        ).all()
        
        preguntas_response = []
        for pregunta in preguntas:
            alternativas = self._obtener_alternativas(pregunta.id_pregunta)
            
            preguntas_response.append({
                "id_pregunta": pregunta.id_pregunta,
                "contenido": pregunta.contenido,
                "alternativas": alternativas
            })
        
        return preguntas_response
    
    def _obtener_alternativas(
        self,
        id_pregunta: int
    ) -> List[Dict[str, Any]]:
        """Obtiene alternativas de una pregunta"""
        alternativa_model = self.get_model("alternativa")
        
        if not alternativa_model:
            raise DatabaseException(
                message="Modelo alternativa no encontrado en la base de datos",
                details={"modelo": "alternativa"}
            )
        
        alternativas = self.db.query(alternativa_model).filter(
            alternativa_model.id_pregunta == id_pregunta
        ).all()
        
        return [
            {
                "id_alternativa": alt.id_alternativa,
                "contenido": alt.contenido
            }
            for alt in alternativas
        ]