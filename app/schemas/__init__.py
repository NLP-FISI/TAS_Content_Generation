from .alternativa import AlternativaBase, AlternativaCreate, Alternativa
from .texto_usuario import TextoUsuarioBase, TextoUsuarioCreate, TextoUsuario
from .pregunta import PreguntaBase, PreguntaCreate, Pregunta, PreguntaConAlternativas
from .texto import TextoBase, TextoCreate, Texto, TextoCompleto

# Actualizar forward references después de importar todo
PreguntaConAlternativas.model_rebuild()
TextoCompleto.model_rebuild()

__all__ = [
    "TextoBase", "TextoCreate", "Texto", "TextoCompleto",
    "TextoUsuarioBase", "TextoUsuarioCreate", "TextoUsuario",
    "PreguntaBase", "PreguntaCreate", "Pregunta", "PreguntaConAlternativas",
    "AlternativaBase", "AlternativaCreate", "Alternativa"
]