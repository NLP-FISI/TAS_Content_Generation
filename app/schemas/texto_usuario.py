from pydantic import BaseModel

class TextoUsuarioBase(BaseModel):
    id_user: str

class TextoUsuarioCreate(TextoUsuarioBase):
    id_texto: int

class TextoUsuario(TextoUsuarioBase):
    id_texto: int
    
    class Config:
        from_attributes = True