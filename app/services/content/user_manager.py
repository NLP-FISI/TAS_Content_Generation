# app/services/content/user_manager.py
from app.services.common.base_service import BaseService
from app.exceptions import ResourceNotFoundException, DatabaseException

class UserManager(BaseService):
    
    def obtener_grado(self, id_usuario: int) -> int:
        usuario_model = self.get_model("usuario")
        
        if not usuario_model:
            raise DatabaseException(
                message="Modelo usuario no encontrado",
                details={"modelo": "usuario"}
            )
        
        usuario = self.query(usuario_model).filter(
            usuario_model.id_usuario == id_usuario
        ).first()
        
        if not usuario:
            raise ResourceNotFoundException(
                message="Usuario no encontrado",
                details={"id_usuario": id_usuario}
            )
        
        id_grado = getattr(usuario, 'id_grado', None)
        
        if id_grado is None:
            raise DatabaseException(
                message="El usuario no tiene un grado asignado",
                details={"id_usuario": id_usuario}
            )
        
        return id_grado
    
    def usuario_existe(self, id_usuario: int) -> bool:
        usuario_model = self.get_model("usuario")
        if not usuario_model:
            return False
        
        usuario = self.query(usuario_model).filter(
            usuario_model.id_usuario == id_usuario
        ).first()
        
        return usuario is not None