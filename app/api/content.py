from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import TextoService
from typing import Dict, Any, Optional

router = APIRouter()

@router.get("/content", response_model=Dict[str, Any])
async def get_content(
    user_id: str = Query(..., description="ID del usuario"),
    grade: str = Query(..., description="Grado del estudiante"),
    category: str = Query(..., description="Categoría del texto"),
    difficulty: str = Query(..., description="Dificultad del texto"),
    question_type: Optional[str] = Query(None, description="Tipo de pregunta (opcional)"),
    db: Session = Depends(get_db)
):
    try:
        resultado = TextoService.asignar_texto_a_usuario(
            db=db,
            user_id=user_id,
            categoria=category,
            grado=grade,
            dificultad=difficulty,
            question_type=question_type
        )
        return resultado
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )