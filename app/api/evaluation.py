# app/api/evaluation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import EvaluationService
from app.schemas.evaluation import EvaluacionRequest, EvaluacionResponse

router = APIRouter(prefix="/evaluacion")


@router.post("/verificar", response_model=EvaluacionResponse)
def verificar_respuestas(
    datos: EvaluacionRequest,
    db: Session = Depends(get_db)
):
    service = EvaluationService(db)
    
    resultados = service.verificar_respuestas(
        respuestas=[r.model_dump() for r in datos.respuestas]
    )
    
    return {
        "respuestas_evaluadas": len(resultados),
        "resultados": resultados
    }