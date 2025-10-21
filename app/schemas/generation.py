# app/schemas/generation.py
from pydantic import BaseModel, Field
from typing import List, Optional, Any

class TextosDisponiblesResponse(BaseModel):
    """Respuesta con múltiples textos disponibles"""
    textos_obtenidos: int
    textos: List[Any]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "textos_obtenidos": 1,
                "textos": [
                    {
                        "texto": {
                            "id_texto": 1,
                            "titulo": "El ciclo del agua",
                            "contenido": "El agua es un recurso vital...",
                            "id_tipo_texto": 1,
                            "id_tematica": 2,
                            "id_dificultad": 1,
                            "id_grado": 3
                        },
                        "preguntas": []
                    }
                ]
            }
        }
    }


class GeneracionRequest(BaseModel):
    id_tipo_texto: int = Field(..., gt=0, description="ID del tipo de texto")
    id_tematicas: List[int] = Field(..., min_length=1, description="Lista de IDs de temáticas")
    id_dificultades: List[int] = Field(..., min_length=1, description="Lista de IDs de dificultades")
    id_grados: List[int] = Field(..., min_length=1, description="Lista de IDs de grados")
    textos_por_combinacion: int = Field(default=1, ge=1, le=10, description="Textos a generar por cada combinación")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_tipo_texto": 1,
                "id_tematicas": [1, 2, 3],
                "id_dificultades": [1, 2],
                "id_grados": [3, 4, 5],
                "textos_por_combinacion": 2
            }
        }
    }


class TextoGeneradoInfo(BaseModel):
    id_texto: int
    titulo: str
    id_tematica: int
    id_dificultad: int
    id_grado: int


class GeneracionResponse(BaseModel):
    textos_generados: int
    textos: List[TextoGeneradoInfo]
    archivo_json: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "textos_generados": 4,
                "textos": [
                    {"id_texto": 45, "titulo": "El león valiente", "id_tematica": 1, "id_dificultad": 1, "id_grado": 3},
                    {"id_texto": 46, "titulo": "La aventura espacial", "id_tematica": 2, "id_dificultad": 2, "id_grado": 4}
                ],
                "archivo_json": "bundle_20251008_103045.json"
            }
        }
    }