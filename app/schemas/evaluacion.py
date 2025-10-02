from pydantic import BaseModel
from typing import List

class RespuestaUsuario(BaseModel):
    id_pregunta: int
    id_respuesta: int

class EvaluacionRequest(BaseModel):
    user_id: str
    id_texto: int
    respuestas: List[RespuestaUsuario]