from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import TextoService
from app.schemas import TextoUsuarioCreate
from typing import Dict, Any

router = APIRouter()

@router.get("/content", response_model=Dict[str, Any])
async def get_content(
    user_id: str = Query(..., description="ID del usuario"),
    grade: str = Query(..., description="Grado del estudiante (ej: 5to, 6to)"),
    category: str = Query(..., description="Categoría del texto"),
    difficulty: str = Query(..., description="Dificultad del texto (facil, media, dificil)"),
    db: Session = Depends(get_db)
):
    try:
        texto_disponible = TextoService.get_texto_disponible_para_usuario(
            db=db,
            user_id=user_id,
            categoria=category,
            grado=grade,
            dificultad=difficulty
        )
        
        if not texto_disponible:
            return {
                "success": False,
                "message": "No hay textos disponibles con los criterios especificados o ya completaste todos los textos disponibles",
                "data": None
            }
        
        texto_usuario_data = TextoUsuarioCreate(
            id_texto=texto_disponible.id_texto,
            id_user=user_id
        )
        
        try:
            TextoService.create_texto_usuario(db, texto_usuario_data)
        except Exception as e:
            print(f"Advertencia al registrar texto_usuario: {str(e)}")
        
        texto_completo = TextoService.get_texto_completo(db, texto_disponible.id_texto)
        
        preguntas_response = []
        for pregunta in texto_completo.preguntas:
            alternativas_response = [
                {
                    "id_respuesta": alt.id_respuesta,
                    "contenido": alt.contenido,
                    "es_correcta": alt.bool
                }
                for alt in pregunta.alternativas
            ]
            
            preguntas_response.append({
                "id_pregunta": pregunta.id_pregunta,
                "contenido": pregunta.contenido,
                "tipo": pregunta.tipo,
                "alternativas": alternativas_response
            })
        
        return {
            "success": True,
            "message": "Texto asignado exitosamente",
            "data": {
                "texto": {
                    "id_texto": texto_completo.id_texto,
                    "contenido": texto_completo.contenido,
                    "categoria": texto_completo.categoria,
                    "dificultad": texto_completo.dificultad,
                    "grado": texto_completo.grado
                },
                "preguntas": preguntas_response
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )