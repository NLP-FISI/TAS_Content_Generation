# app/schemas/evaluation.py
from pydantic import BaseModel, Field
from typing import List

class RespuestaUsuario(BaseModel):
    id_pregunta: int = Field(..., gt=0, description="ID de la pregunta")
    id_alternativa: int = Field(..., gt=0, description="ID de la alternativa seleccionada")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_pregunta": 1,
                "id_alternativa": 3
            }
        }
    }


class ResultadoVerificacion(BaseModel):
    id_pregunta: int
    id_alternativa: int
    es_correcta: bool
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_pregunta": 1,
                "id_alternativa": 3,
                "es_correcta": True
            }
        }
    }


class EvaluacionRequest(BaseModel):
    respuestas: List[RespuestaUsuario] = Field(
        ..., 
        min_length=1,
        description="Lista de respuestas a evaluar (mínimo 1)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "respuestas": [
                        {"id_pregunta": 1, "id_alternativa": 3}
                    ]
                },
                {
                    "respuestas": [
                        {"id_pregunta": 1, "id_alternativa": 3},
                        {"id_pregunta": 2, "id_alternativa": 7},
                        {"id_pregunta": 3, "id_alternativa": 10}
                    ]
                }
            ]
        }
    }


class EvaluacionResponse(BaseModel):
    respuestas_evaluadas: int = Field(..., description="Cantidad de respuestas evaluadas")
    resultados: List[ResultadoVerificacion] = Field(..., description="Resultados de la evaluación")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "respuestas_evaluadas": 3,
                "resultados": [
                    {
                        "id_pregunta": 1,
                        "id_alternativa": 3,
                        "es_correcta": True
                    },
                    {
                        "id_pregunta": 2,
                        "id_alternativa": 7,
                        "es_correcta": False
                    },
                    {
                        "id_pregunta": 3,
                        "id_alternativa": 10,
                        "es_correcta": True
                    }
                ]
            }
        }
    }