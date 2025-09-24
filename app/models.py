from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
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

class TextoUsuario(Base):
    __tablename__ = "texto_usuario"
    
    id_texto = Column(Integer, ForeignKey("texto.id_texto"), primary_key=True)
    id_user = Column(String(100), nullable=False)
    
    texto = relationship("Texto", back_populates="texto_usuarios")

class Preguntas(Base):
    __tablename__ = "preguntas"
    
    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_texto = Column(Integer, ForeignKey("texto.id_texto"), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    
    texto = relationship("Texto", back_populates="preguntas")
    alternativas = relationship("Alternativa", back_populates="pregunta")

class Alternativa(Base):
    __tablename__ = "alternativa"
    
    id_respuesta = Column(Integer, primary_key=True, index=True)
    id_pregunta = Column(Integer, ForeignKey("preguntas.id_pregunta"), nullable=False)
    bool = Column(Boolean, nullable=False)
    contenido = Column(Text, nullable=False)
    
    pregunta = relationship("Preguntas", back_populates="alternativas")
