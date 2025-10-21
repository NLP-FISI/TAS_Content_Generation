# app/schemas/content.py
from pydantic import BaseModel, Field
from typing import List


class AlternativaSimpleResponse(BaseModel):
    """Esquema simple de alternativa"""
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


class PreguntaSimpleResponse(BaseModel):
    """Esquema simple de pregunta con sus alternativas"""
    id_pregunta: int
    contenido: str
    alternativas: List[AlternativaSimpleResponse]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_pregunta": 1,
                "contenido": "¿Cuál es la idea principal del texto?",
                "alternativas": [
                    {"id_alternativa": 1, "contenido": "Opción A"},
                    {"id_alternativa": 2, "contenido": "Opción B"},
                    {"id_alternativa": 3, "contenido": "Opción C"},
                    {"id_alternativa": 4, "contenido": "Opción D"}
                ]
            }
        }
    }


class TextoConPreguntasResponse(BaseModel):
    """Esquema de texto con sus preguntas anidadas"""
    id_texto: int
    titulo: str
    contenido: str
    preguntas: List[PreguntaSimpleResponse]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_texto": 1,
                "titulo": "El ciclo del agua",
                "contenido": "El agua es un recurso vital...",
                "preguntas": [
                    {
                        "id_pregunta": 1,
                        "contenido": "¿Cuál es la idea principal?",
                        "alternativas": [
                            {"id_alternativa": 1, "contenido": "Opción A"},
                            {"id_alternativa": 2, "contenido": "Opción B"},
                            {"id_alternativa": 3, "contenido": "Opción C"},
                            {"id_alternativa": 4, "contenido": "Opción D"}
                        ]
                    }
                ]
            }
        }
    }


class TextosDisponiblesResponse(BaseModel):
    """Respuesta con múltiples textos disponibles para un usuario"""
    textos_obtenidos: int = Field(..., description="Cantidad de textos obtenidos")
    textos: List[TextoConPreguntasResponse] = Field(..., description="Lista de textos con sus preguntas anidadas")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "textos_obtenidos": 2,
                "textos": [
                    {
                        "id_texto": 1,
                        "titulo": "El ciclo del agua",
                        "contenido": "El agua es un recurso vital...",
                        "preguntas": [
                            {
                                "id_pregunta": 1,
                                "contenido": "¿Cuál es la idea principal?",
                                "alternativas": [
                                    {"id_alternativa": 1, "contenido": "Opción A"},
                                    {"id_alternativa": 2, "contenido": "Opción B"},
                                    {"id_alternativa": 3, "contenido": "Opción C"},
                                    {"id_alternativa": 4, "contenido": "Opción D"}
                                ]
                            }
                        ]
                    },
                    {
                        "id_texto": 2,
                        "titulo": "Las plantas",
                        "contenido": "Las plantas son seres vivos...",
                        "preguntas": []
                    }
                ]
            }
        }
    }