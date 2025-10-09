# app/schemas/content.py
from pydantic import BaseModel, Field
from typing import List


class AlternativaResponse(BaseModel):
    id_alternativa: int
    contenido: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_alternativa": 1,
                "contenido": "Opción A"
            }
        }
    }


class PreguntaResponse(BaseModel):
    """Esquema para una pregunta con sus alternativas"""
    id_pregunta: int
    contenido: str
    id_tipo_pregunta: int
    id_dificultad: int
    alternativas: List[AlternativaResponse]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_pregunta": 1,
                "contenido": "¿Cuál es la idea principal del texto?",
                "id_tipo_pregunta": 1,
                "id_dificultad": 2,
                "alternativas": [
                    {"id_alternativa": 1, "contenido": "Opción A"},
                    {"id_alternativa": 2, "contenido": "Opción B"}
                ]
            }
        }
    }


class TextoResponse(BaseModel):
    """Esquema para un texto"""
    id_texto: int
    titulo: str
    contenido: str
    id_tipo_texto: int
    id_tematica: int
    id_dificultad: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_texto": 1,
                "titulo": "El ciclo del agua",
                "contenido": "El agua es un recurso vital...",
                "id_tipo_texto": 1,
                "id_tematica": 2,
                "id_dificultad": 1
            }
        }
    }


class ContenidoResponse(BaseModel):
    """Esquema para la respuesta completa con texto y preguntas"""
    texto: TextoResponse
    preguntas: List[PreguntaResponse]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": {
                    "id_texto": 1,
                    "titulo": "El ciclo del agua",
                    "contenido": "El agua es un recurso vital...",
                    "id_tipo_texto": 1,
                    "id_tematica": 2,
                    "id_dificultad": 1
                },
                "preguntas": [
                    {
                        "id_pregunta": 1,
                        "contenido": "¿Cuál es la idea principal?",
                        "id_tipo_pregunta": 1,
                        "id_dificultad": 2,
                        "alternativas": [
                            {"id_alternativa": 1, "contenido": "Opción A"},
                            {"id_alternativa": 2, "contenido": "Opción B"}
                        ]
                    }
                ]
            }
        }
    }