from pydantic import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .alternativa import Alternativa

class PreguntaBase(BaseModel):
    contenido: str
    tipo: str

class PreguntaCreate(PreguntaBase):
    id_texto: int

class Pregunta(PreguntaBase):
    id_pregunta: int
    id_texto: int
    
    class Config:
        from_attributes = True

class PreguntaConAlternativas(Pregunta):
    alternativas: List['Alternativa'] = []