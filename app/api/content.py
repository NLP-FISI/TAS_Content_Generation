# app/api/content.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import ContentService
from app.schemas.responses import SuccessResponse

router = APIRouter(prefix="/contenido")

@router.get("/obtener", response_model=SuccessResponse)
def obtener_contenido(
    tipo: int = Query(..., gt=0, description="ID del tipo de texto"),
    tematica: int = Query(..., gt=0, description="ID de la temática"),
    dificultad: int = Query(..., gt=0, description="ID de la dificultad"),
    db: Session = Depends(get_db)
):
    service = ContentService(db)
    
    contenido = service.obtener_texto_con_preguntas(
        id_tipo_texto=tipo,
        id_tematica=tematica,
        id_dificultad=dificultad
    )
    
    return SuccessResponse(
        success=True,
        data=contenido
    )