from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_textos_by_categoria, get_textos_by_grado, get_textos_by_user, create_texto_usuario
from app.schemas import Texto, TextoUsuarioCreate
from typing import List

app = FastAPI()

class ContentRequest(BaseModel):
    user_id: str
    grade: str
    category: str

@app.get("/content")
async def get_content(request: ContentRequest, db: Session = Depends(get_db)):
    try:
        textos_categoria = get_textos_by_categoria(db, request.category)
        textos_grado = get_textos_by_grado(db, request.grade)
        textos_encontrados = list(set(textos_categoria + textos_grado))
        
        if not textos_encontrados:
            return {
                "message": "No se encontraron textos con los criterios especificados",
                "user_id": request.user_id,
                "grade": request.grade,
                "category": request.category,
                "textos": []
            }
        
        texto_seleccionado = textos_encontrados[0]
        
        texto_usuario_data = TextoUsuarioCreate(
            id_texto=texto_seleccionado.id_texto,
            id_user=request.user_id
        )
        
        try:
            create_texto_usuario(db, texto_usuario_data)
            mensaje = "Texto asignado al usuario exitosamente"
        except Exception as e:
            mensaje = f"Texto ya asignado al usuario o error: {str(e)}"
        
        return {
            "message": mensaje,
            "user_id": request.user_id,
            "grade": request.grade,
            "category": request.category,
            "texto_asignado": {
                "id": texto_seleccionado.id_texto,
                "contenido": texto_seleccionado.contenido[:200] + "..." if len(texto_seleccionado.contenido) > 200 else texto_seleccionado.contenido,
                "categoria": texto_seleccionado.categoria,
                "dificultad": texto_seleccionado.dificultad,
                "grado": texto_seleccionado.grado
            },
            "total_textos_encontrados": len(textos_encontrados)
        }
        
    except Exception as e:
        return {
            "error": f"Error interno del servidor: {str(e)}",
            "user_id": request.user_id,
            "grade": request.grade,
            "category": request.category
        }