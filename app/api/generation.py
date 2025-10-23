# app/api/generation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.generation import GenerationOrchestratorV2
from app.schemas.generation import GeneracionRequest
from app.schemas.responses import SuccessResponse

router = APIRouter(prefix="/generacion")

@router.post("/generar", response_model=SuccessResponse)
def generar_contenido(
    datos: GeneracionRequest,
    db: Session = Depends(get_db)
):

    orchestrator = GenerationOrchestratorV2(db)
    
    resultado = orchestrator.generar_textos(
        id_tipo_texto=datos.id_tipo_texto,
        id_tematicas=datos.id_tematicas,
        id_dificultades=datos.id_dificultades,
        id_grados=datos.id_grados,
        textos_por_combinacion=datos.textos_por_combinacion
    )
    
    return SuccessResponse(
        success=True,
        data=resultado
    )