from .content import (
    AlternativaSimpleResponse, 
    PreguntaSimpleResponse, 
    TextoConPreguntasResponse, 
    TextosDisponiblesResponse
)
from .evaluation import (EvaluacionRequest, RespuestaUsuario, ResultadoVerificacion)
from .responses import (SuccessResponse, ErrorResponse, ErrorDetail)
from .generation import (GeneracionRequest, GeneracionResponse, TextoGeneradoInfo)

__all__ = [
    "AlternativaSimpleResponse", 
    "PreguntaSimpleResponse", 
    "TextoConPreguntasResponse", 
    "TextosDisponiblesResponse",
    "EvaluacionRequest", 
    "RespuestaUsuario", 
    "ResultadoVerificacion",
    "SuccessResponse", 
    "ErrorResponse", 
    "ErrorDetail",
    "GeneracionRequest", 
    "GeneracionResponse", 
    "TextoGeneradoInfo"
]