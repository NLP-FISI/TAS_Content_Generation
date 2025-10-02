from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Alternativa(Base):
    __tablename__ = "alternativa"
    
    id_respuesta = Column(Integer, primary_key=True, index=True)
    id_pregunta = Column(Integer, ForeignKey("preguntas.id_pregunta"), nullable=False)
    bool = Column(Boolean, nullable=False)
    contenido = Column(Text, nullable=False)
    
    pregunta = relationship("Preguntas", back_populates="alternativas")