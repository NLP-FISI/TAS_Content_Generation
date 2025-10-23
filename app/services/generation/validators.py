# app/services/generation/validators.py
from typing import List
from app.exceptions import BusinessLogicException
from app.config.settings import settings

class GenerationRequestValidator:
    
    def __init__(self, catalog_service):
        self.catalog = catalog_service
    
    def validar_ids_existen(
        self,
        id_tipo_texto: int,
        id_tematicas: List[int],
        id_dificultades: List[int],
        id_grados: List[int]
    ) -> None:
        self.catalog.obtener_nombre_tipo_texto(id_tipo_texto)
        
        for id_tematica in id_tematicas:
            self.catalog.obtener_nombre_tematica(id_tematica)
        
        for id_dificultad in id_dificultades:
            self.catalog.obtener_nombre_dificultad(id_dificultad)
        
        for id_grado in id_grados:
            self.catalog.obtener_nombre_grado(id_grado)
    
    def validar_limites(self, cantidad_textos: int) -> None:
        if cantidad_textos > settings.MAX_TEXTOS_POR_REQUEST:
            raise BusinessLogicException(
                message=f"La solicitud excede el límite de {settings.MAX_TEXTOS_POR_REQUEST} textos",
                code="LIMITE_EXCEDIDO",
                details={
                    "total_solicitado": cantidad_textos,
                    "limite_maximo": settings.MAX_TEXTOS_POR_REQUEST
                }
            )