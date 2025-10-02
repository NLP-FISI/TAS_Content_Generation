from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Texto, TextoUsuario, Preguntas, Alternativa
from app.schemas import TextoUsuarioCreate
from typing import Optional

class TextoService:
    
    @staticmethod
    def get_texto_disponible_para_usuario(
        db: Session, 
        user_id: str, 
        categoria: str, 
        grado: str, 
        dificultad: str
    ) -> Optional[Texto]:
        """
        Busca un texto que coincida con los criterios y que NO haya sido usado por el usuario
        """
        # Subconsulta: IDs de textos ya usados por el usuario
        textos_usados = db.query(TextoUsuario.id_texto).filter(
            TextoUsuario.id_user == user_id
        ).subquery()
        
        # Buscar texto que coincida con criterios y NO esté en textos usados
        texto_disponible = db.query(Texto).filter(
            and_(
                Texto.categoria == categoria,
                Texto.grado == grado,
                Texto.dificultad == dificultad,
                ~Texto.id_texto.in_(textos_usados)
            )
        ).first()
        
        return texto_disponible
    
    @staticmethod
    def get_texto_completo(db: Session, texto_id: int) -> Optional[Texto]:
        """
        Obtiene el texto con sus preguntas y alternativas
        """
        texto = db.query(Texto).filter(Texto.id_texto == texto_id).first()
        if not texto:
            return None
        
        # Obtener preguntas
        preguntas = db.query(Preguntas).filter(Preguntas.id_texto == texto_id).all()
        
        # Para cada pregunta, obtener sus alternativas
        for pregunta in preguntas:
            pregunta.alternativas = db.query(Alternativa).filter(
                Alternativa.id_pregunta == pregunta.id_pregunta
            ).all()
        
        texto.preguntas = preguntas
        return texto
    
    @staticmethod
    def create_texto_usuario(db: Session, texto_usuario: TextoUsuarioCreate) -> TextoUsuario:
        """
        Registra que un usuario ha usado un texto
        """
        db_texto_usuario = TextoUsuario(**texto_usuario.dict())
        db.add(db_texto_usuario)
        db.commit()
        db.refresh(db_texto_usuario)
        return db_texto_usuario