from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from app.services.common.base_service import BaseService
from app.exceptions import DatabaseException
import logging

logger = logging.getLogger(__name__)

class GuardarEnBDService(BaseService):

    def guardar_usuario_auditoria(
        self,
        id_usuario: int,
        id_juego: int,
        id_texto: int,
    ) -> bool:
        try:
            logger.info(
                "Iniciando guardado de auditoría: "
                f"id_usuario={id_usuario}, id_juego={id_juego}, "
            )

            resultado_texto = self.get_model("resultado_texto")
            if resultado_texto is None:
                raise DatabaseException(
                    message="Modelo resultado_texto no encontrado",
                    details={"modelo": "resultado_texto"}
                )
            
            existe = self.db.query(resultado_texto).filter(
                resultado_texto.id_usuario == id_usuario,
                resultado_texto.id_juego == id_juego,
                resultado_texto.id_texto == id_texto,
            ).first()

            if existe:
                logger.info("Ya existe un registro de auditoría para este usuario, juego y texto. No se crea uno nuevo.")
                return True

            nuevo_resultado = resultado_texto(
                id_usuario=id_usuario,
                id_juego=id_juego,
                id_texto=id_texto
            )

            self.db.add(nuevo_resultado)
            self.db.commit()
            self.db.refresh(nuevo_resultado)

            logger.info(f"Resultado de auditoría guardado correctamente (ID: {nuevo_resultado.id_resultado_texto})")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Error SQL al guardar auditoría: {str(e)}", exc_info=True)
            self.db.rollback()
            raise DatabaseException(
                message="Error al guardar auditoría en la base de datos",
                details={"error": str(e), "type": type(e).__name__}
            )

        except Exception as e:
            logger.error(f"Error inesperado al guardar auditoría: {str(e)}", exc_info=True)
            self.db.rollback()
            raise DatabaseException(
                message="Error inesperado al guardar auditoría",
                details={"error": str(e), "type": type(e).__name__}
            )