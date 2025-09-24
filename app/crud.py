from sqlalchemy.orm import Session
from app.models import Texto, TextoUsuario, Preguntas, Alternativa
from app.schemas import TextoCreate, TextoUsuarioCreate, PreguntaCreate, AlternativaCreate
from typing import List, Optional

def get_texto(db: Session, texto_id: int):
    return db.query(Texto).filter(Texto.id_texto == texto_id).first()

def get_textos_by_categoria(db: Session, categoria: str):
    return db.query(Texto).filter(Texto.categoria == categoria).all()

def get_textos_by_grado(db: Session, grado: str):
    return db.query(Texto).filter(Texto.grado == grado).all()

def get_textos_by_dificultad(db: Session, dificultad: str):
    return db.query(Texto).filter(Texto.dificultad == dificultad).all()

def get_textos_by_user(db: Session, user_id: str):
    return db.query(Texto).join(TextoUsuario).filter(TextoUsuario.id_user == user_id).all()

def create_texto(db: Session, texto: TextoCreate):
    db_texto = Texto(**texto.dict())
    db.add(db_texto)
    db.commit()
    db.refresh(db_texto)
    return db_texto

def get_preguntas_by_texto(db: Session, texto_id: int):
    return db.query(Preguntas).filter(Preguntas.id_texto == texto_id).all()

def get_alternativas_by_pregunta(db: Session, pregunta_id: int):
    return db.query(Alternativa).filter(Alternativa.id_pregunta == pregunta_id).all()

def create_texto_usuario(db: Session, texto_usuario: TextoUsuarioCreate):
    db_texto_usuario = TextoUsuario(**texto_usuario.dict())
    db.add(db_texto_usuario)
    db.commit()
    db.refresh(db_texto_usuario)
    return db_texto_usuario

def get_texto_completo(db: Session, texto_id: int):
    texto = get_texto(db, texto_id)
    if not texto:
        return None
    
    preguntas = get_preguntas_by_texto(db, texto_id)
    for pregunta in preguntas:
        pregunta.alternativas = get_alternativas_by_pregunta(db, pregunta.id_pregunta)
    
    texto.preguntas = preguntas
    return texto
