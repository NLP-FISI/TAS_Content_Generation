from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services import EvaluationService
from typing import Dict, Any, List

router = APIRouter()

class RespuestaUsuario(BaseModel):
    id_pregunta: int
    id_respuesta: int

class EvaluacionRequest(BaseModel):
    user_id: str
    id_texto: int
    respuestas: List[RespuestaUsuario]

@router.post("/evaluate", response_model=Dict[str, Any])
async def evaluate_answers(
    request: EvaluacionRequest,
    db: Session = Depends(get_db)
):
    try:
        respuestas_dict = [
            {"id_pregunta": r.id_pregunta, "id_respuesta": r.id_respuesta}
            for r in request.respuestas
        ]
        
        resultado = EvaluationService.evaluar_respuestas(
            db=db,
            id_texto=request.id_texto,
            respuestas=respuestas_dict
        )
        
        return {
            "success": True,
            "message": "Evaluación completada",
            "data": resultado
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al evaluar respuestas: {str(e)}"
        )