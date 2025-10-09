# app/schemas/generation.py
from pydantic import BaseModel, Field
from typing import List, Optional

class GeneracionRequest(BaseModel):
    id_tipo_texto: int = Field(..., gt=0, description="ID del tipo de texto")
    id_tematicas: List[int] = Field(..., min_length=1, description="Lista de IDs de temáticas")
    id_dificultades: List[int] = Field(..., min_length=1, description="Lista de IDs de dificultades")
    textos_por_combinacion: int = Field(default=1, ge=1, le=10, description="Textos a generar por cada combinación")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_tipo_texto": 1,
                "id_tematicas": [1, 2, 3],
                "id_dificultades": [1, 2],
                "textos_por_combinacion": 2
            }
        }
    }


class TextoGeneradoInfo(BaseModel):
    id_texto: int
    titulo: str
    id_tematica: int
    id_dificultad: int


class GeneracionResponse(BaseModel):
    textos_generados: int
    textos: List[TextoGeneradoInfo]
    archivo_json: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "textos_generados": 4,
                "textos": [
                    {"id_texto": 45, "titulo": "El león valiente", "id_tematica": 1, "id_dificultad": 1},
                    {"id_texto": 46, "titulo": "La aventura espacial", "id_tematica": 2, "id_dificultad": 2}
                ],
                "archivo_json": "bundle_20251008_103045.json"
            }
        }
    }