from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Preguntas(Base):
    __tablename__ = "preguntas"
    
    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_texto = Column(Integer, ForeignKey("texto.id_texto"), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    
    texto = relationship("Texto", back_populates="preguntas")
    alternativas = relationship("Alternativa", back_populates="pregunta")