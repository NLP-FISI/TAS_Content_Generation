# app/services/generation/catalog_service.py
from typing import Dict, Optional
from app.services.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException

class CatalogService(BaseService):
    
    def obtener_nombre_tematica(self, id_tematica: int) -> str:
        try:
            Tematica = self.get_model("Tematica")
            if not Tematica:
                raise DatabaseException(
                    message="Modelo Tematica no encontrado",
                    details={"modelo": "Tematica"}
                )
            
            tematica = self.db.query(Tematica).filter(
                Tematica.ID_Tematica == id_tematica
            ).first()
            
            if not tematica:
                raise ResourceNotFoundException(
                    message="Temática no encontrada",
                    details={"id_tematica": id_tematica}
                )
            
            return tematica.Nombre_Tematica
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener temática",
                details={"id_tematica": id_tematica, "error": str(e)}
            )
    
    def obtener_nombre_dificultad(self, id_dificultad: int) -> str:
        try:
            Dificultad = self.get_model("Dificultad")
            if not Dificultad:
                raise DatabaseException(
                    message="Modelo Dificultad no encontrado",
                    details={"modelo": "Dificultad"}
                )
            
            dificultad = self.db.query(Dificultad).filter(
                Dificultad.ID_Dificultad == id_dificultad
            ).first()
            
            if not dificultad:
                raise ResourceNotFoundException(
                    message="Dificultad no encontrada",
                    details={"id_dificultad": id_dificultad}
                )
            
            return dificultad.Nombre_Dificultad
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener dificultad",
                details={"id_dificultad": id_dificultad, "error": str(e)}
            )
    
    def obtener_nombre_tipo_texto(self, id_tipo_texto: int) -> str:
        try:
            TipoTexto = self.get_model("Tipo_Texto")
            if not TipoTexto:
                raise DatabaseException(
                    message="Modelo Tipo_Texto no encontrado",
                    details={"modelo": "Tipo_Texto"}
                )
            
            tipo_texto = self.db.query(TipoTexto).filter(
                TipoTexto.ID_Tipo_Texto == id_tipo_texto
            ).first()
            
            if not tipo_texto:
                raise ResourceNotFoundException(
                    message="Tipo de texto no encontrado",
                    details={"id_tipo_texto": id_tipo_texto}
                )
            
            return tipo_texto.Nombre_Tipo_Texto
            
        except (ResourceNotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(
                message="Error al obtener tipo de texto",
                details={"id_tipo_texto": id_tipo_texto, "error": str(e)}
            )
    
    def obtener_nombre_tipo_pregunta(self, id_tipo_pregunta: int) -> str:
        try:
            TipoPregunta = self.get_model("Tipo_Pregunta")
            if not TipoPregunta:
                raise DatabaseException(
                    message="Modelo Tipo_Pregunta no encontrado",
                    details={"modelo": "Tipo_Pregunta"}
                )
            
            tipo_pregunta = self.db.query(TipoPregunta).filter(
                TipoPregunta.ID_Tipo_Pregunta == id_tipo_pregunta
            ).first()
            
            if not tipo_pregunta:
                raise ResourceNotFoundException(
                    message="Tipo de pregunta no encontrado",
                    details={"id_tipo_pregunta": id_tipo_pregunta}
                )
            
            return tipo_pregunta.Nombre_Tipo_Pregunta
            
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
        id_dificultades: list
    ):
        self.obtener_nombre_tipo_texto(id_tipo_texto)
        
        for id_tematica in id_tematicas:
            self.obtener_nombre_tematica(id_tematica)
        
        for id_dificultad in id_dificultades:
            self.obtener_nombre_dificultad(id_dificultad)