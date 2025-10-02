from pydantic import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .pregunta import PreguntaConAlternativas

class TextoBase(BaseModel):
    contenido: str
    categoria: str
    dificultad: str
    grado: str

class TextoCreate(TextoBase):
    pass

class Texto(TextoBase):
    id_texto: int
    
    class Config:
        from_attributes = True

class TextoCompleto(Texto):
    preguntas: List['PreguntaConAlternativas'] = []