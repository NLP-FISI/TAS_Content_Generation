# app/services/generation/catalog_service.py
from typing import Dict, Optional
from app.services.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException

class CatalogService(BaseService):
    
    def obtener_nombre_grado(self, id_grado: int) -> str:
        try:
            grado_model = self.get_model("grado")
            if not grado_model:
                raise DatabaseException(
                    message="Modelo grado no encontrado",
                    details={"modelo": "grado"}
                )
            
            grado = self.db.query(grado_model).filter(
                grado_model.id_grado == id_grado
            ).first()
            
            if not grado:
                raise ResourceNotFoundException(
                    message="Grado no encontrado",
                    details={"id_grado": id_grado}
                )
            
            return grado.nombre_grado
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener grado",
                details={"id_grado": id_grado, "error": str(e)}
            )
    
    def obtener_nombre_tematica(self, id_tematica: int) -> str:
        try:
            tematica_model = self.get_model("tematica")
            if not tematica_model:
                raise DatabaseException(
                    message="Modelo tematica no encontrado",
                    details={"modelo": "tematica"}
                )
            
            tematica = self.db.query(tematica_model).filter(
                tematica_model.id_tematica == id_tematica
            ).first()
            
            if not tematica:
                raise ResourceNotFoundException(
                    message="Temática no encontrada",
                    details={"id_tematica": id_tematica}
                )
            
            return tematica.nombre_tematica
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener temática",
                details={"id_tematica": id_tematica, "error": str(e)}
            )
    
    def obtener_nombre_dificultad(self, id_dificultad: int) -> str:
        try:
            dificultad_model = self.get_model("dificultad")
            if not dificultad_model:
                raise DatabaseException(
                    message="Modelo dificultad no encontrado",
                    details={"modelo": "dificultad"}
                )
            
            dificultad = self.db.query(dificultad_model).filter(
                dificultad_model.id_dificultad == id_dificultad
            ).first()
            
            if not dificultad:
                raise ResourceNotFoundException(
                    message="Dificultad no encontrada",
                    details={"id_dificultad": id_dificultad}
                )
            
            return dificultad.nombre_dificultad
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener dificultad",
                details={"id_dificultad": id_dificultad, "error": str(e)}
            )
    
    def obtener_nombre_tipo_texto(self, id_tipo_texto: int) -> str:
        try:
            tipo_texto_model = self.get_model("tipo_texto")
            if not tipo_texto_model:
                raise DatabaseException(
                    message="Modelo tipo_texto no encontrado",
                    details={"modelo": "tipo_texto"}
                )
            
            tipo_texto = self.db.query(tipo_texto_model).filter(
                tipo_texto_model.id_tipo_texto == id_tipo_texto
            ).first()
            
            if not tipo_texto:
                raise ResourceNotFoundException(
                    message="Tipo de texto no encontrado",
                    details={"id_tipo_texto": id_tipo_texto}
                )
            
            return tipo_texto.nombre_tipo_texto
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener tipo de texto",
                details={"id_tipo_texto": id_tipo_texto, "error": str(e)}
            )
    
    def obtener_nombre_tipo_pregunta(self, id_tipo_pregunta: int) -> str:
        try:
            tipo_pregunta_model = self.get_model("tipo_pregunta")
            if not tipo_pregunta_model:
                raise DatabaseException(
                    message="Modelo tipo_pregunta no encontrado",
                    details={"modelo": "tipo_pregunta"}
                )
            
            tipo_pregunta = self.db.query(tipo_pregunta_model).filter(
                tipo_pregunta_model.id_tipo_pregunta == id_tipo_pregunta
            ).first()
            
            if not tipo_pregunta:
                raise ResourceNotFoundException(
                    message="Tipo de pregunta no encontrado",
                    details={"id_tipo_pregunta": id_tipo_pregunta}
                )
            
            return tipo_pregunta.nombre_tipo_pregunta
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener tipo de pregunta",
                details={"id_tipo_pregunta": id_tipo_pregunta, "error": str(e)}
            )
    
    def validar_ids_existen(
        self,
        id_tipo_texto: int,
        id_tematicas: list,
        id_dificultades: list,
        id_grados: list
    ):
        self.obtener_nombre_tipo_texto(id_tipo_texto)
        
        for id_tematica in id_tematicas:
            self.obtener_nombre_tematica(id_tematica)
        
        for id_dificultad in id_dificultades:
            self.obtener_nombre_dificultad(id_dificultad)
        
        for id_grado in id_grados:
            self.obtener_nombre_grado(id_grado)