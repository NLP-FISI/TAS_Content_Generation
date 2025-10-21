# app/api/content.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import ContentService
from app.schemas.content import TextosDisponiblesResponse

router = APIRouter(prefix="/contenido")

@router.get("/obtener", response_model=TextosDisponiblesResponse)
def obtener_contenido(
    id_usuario: int = Query(..., gt=0, description="ID del usuario"),
    id_tipo_texto: int = Query(..., gt=0, description="ID del tipo de texto"),
    id_tematica: int = Query(..., gt=0, description="ID de la temática"),
    id_dificultad: int = Query(..., gt=0, description="ID de la dificultad"),
    cantidad: int = Query(default=1, ge=1, le=50, description="Cantidad de textos a obtener (default=1)"),
    db: Session = Depends(get_db)
):
    service = ContentService(db)
    
    contenido = service.obtener_textos_disponibles(
        id_usuario=id_usuario,
        id_tipo_texto=id_tipo_texto,
        id_tematica=id_tematica,
        id_dificultad=id_dificultad,
        cantidad=cantidad
    )
    
    return contenido