from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TextoUsuario(Base):
    __tablename__ = "texto_usuario"
    
    id_texto = Column(Integer, ForeignKey("texto.id_texto"), primary_key=True)
    id_user = Column(String(100), nullable=False)
    
    texto = relationship("Texto", back_populates="texto_usuarios")