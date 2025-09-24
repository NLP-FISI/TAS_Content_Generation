from pydantic import BaseModel
from typing import List, Optional

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

class TextoUsuarioBase(BaseModel):
    id_user: str

class TextoUsuarioCreate(TextoUsuarioBase):
    id_texto: int

class TextoUsuario(TextoUsuarioBase):
    id_texto: int
    
    class Config:
        from_attributes = True

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

class AlternativaBase(BaseModel):
    contenido: str
    bool: bool

class AlternativaCreate(AlternativaBase):
    id_pregunta: int

class Alternativa(AlternativaBase):
    id_respuesta: int
    id_pregunta: int
    
    class Config:
        from_attributes = True

class PreguntaConAlternativas(Pregunta):
    alternativas: List[Alternativa] = []

class TextoCompleto(Texto):
    preguntas: List[PreguntaConAlternativas] = []
