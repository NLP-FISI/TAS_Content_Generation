from pydantic import BaseModel

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