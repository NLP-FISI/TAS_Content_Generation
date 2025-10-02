from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Texto(Base):
    __tablename__ = "texto"
    
    id_texto = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(100), nullable=False)
    dificultad = Column(String(50), nullable=False)
    grado = Column(String(50), nullable=False)
    
    preguntas = relationship("Preguntas", back_populates="texto")
    texto_usuarios = relationship("TextoUsuario", back_populates="texto")