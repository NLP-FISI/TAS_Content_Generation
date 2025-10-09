# app/api/evaluation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import EvaluationService
from app.schemas.evaluation import EvaluacionRequest
from app.schemas.responses import SuccessResponse

router = APIRouter(prefix="/evaluacion")


@router.post("/verificar", response_model=SuccessResponse)
def verificar_respuestas(
    datos: EvaluacionRequest,
    db: Session = Depends(get_db)
):
    service = EvaluationService(db)
    
    resultados = service.verificar_respuestas(
        respuestas=[r.model_dump() for r in datos.respuestas]
    )
    
    return SuccessResponse(
        success=True,
        data={"resultados": resultados}
    )