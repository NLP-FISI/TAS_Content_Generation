# app/services/content/assignment_manager.py
from typing import List
from sqlalchemy import select
from app.services.common.base_service import BaseService
from app.exceptions import DatabaseException

class AssignmentManager(BaseService):
    
    def asignar_texto(self, id_usuario: int, id_texto: int) -> None:
        usuario_texto_model = self.get_model("usuario_texto")
        
        if not usuario_texto_model:
            raise DatabaseException(
                message="Modelo usuario_texto no encontrado",
                details={"modelo": "usuario_texto"}
            )
        
        try:
            registro = usuario_texto_model(
                id_usuario=id_usuario,
                id_texto=id_texto
            )
            self.add(registro)
            self.flush()
        except Exception as e:
            self.rollback()
            raise DatabaseException(
                message="Error al asignar texto a usuario",
                details={
                    "id_usuario": id_usuario,
                    "id_texto": id_texto,
                    "error": str(e)
                }
            )
    
    def obtener_textos_asignados(self, id_usuario: int) -> List[int]:
        usuario_texto_model = self.get_model("usuario_texto")
        
        if not usuario_texto_model:
            return []
        
        registros = self.query(usuario_texto_model).filter(
            usuario_texto_model.id_usuario == id_usuario
        ).all()
        
        return [registro.id_texto for registro in registros]
    
    def texto_esta_asignado(self, id_usuario: int, id_texto: int) -> bool:
        usuario_texto_model = self.get_model("usuario_texto")
        
        if not usuario_texto_model:
            return False
        
        registro = self.query(usuario_texto_model).filter(
            usuario_texto_model.id_usuario == id_usuario,
            usuario_texto_model.id_texto == id_texto
        ).first()
        
        return registro is not None
    
    def crear_subquery_textos_asignados(self, id_usuario: int):
        usuario_texto_model = self.get_model("usuario_texto")
        
        return select(usuario_texto_model.id_texto).where(
            usuario_texto_model.id_usuario == id_usuario
        )