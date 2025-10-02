from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Texto, TextoUsuario, Preguntas, Alternativa
from app.schemas import TextoUsuarioCreate
from typing import Optional, Dict, Any, List

class TextoService:
    
    @staticmethod
    def get_texto_disponible_para_usuario(
        db: Session, 
        user_id: str, 
        categoria: str, 
        grado: str, 
        dificultad: str
    ) -> Optional[Texto]:
        textos_usados = db.query(TextoUsuario.id_texto).filter(
            TextoUsuario.id_user == user_id
        ).subquery()
        
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
        texto = db.query(Texto).filter(Texto.id_texto == texto_id).first()
        if not texto:
            return None
        
        preguntas = db.query(Preguntas).filter(Preguntas.id_texto == texto_id).all()
        
        for pregunta in preguntas:
            pregunta.alternativas = db.query(Alternativa).filter(
                Alternativa.id_pregunta == pregunta.id_pregunta
            ).all()
        
        texto.preguntas = preguntas
        return texto
    
    @staticmethod
    def create_texto_usuario(db: Session, texto_usuario: TextoUsuarioCreate) -> TextoUsuario:
        db_texto_usuario = TextoUsuario(**texto_usuario.dict())
        db.add(db_texto_usuario)
        db.commit()
        db.refresh(db_texto_usuario)
        return db_texto_usuario
    
    @staticmethod
    def asignar_texto_a_usuario(
        db: Session,
        user_id: str,
        categoria: str,
        grado: str,
        dificultad: str,
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        texto_disponible = TextoService.get_texto_disponible_para_usuario(
            db=db,
            user_id=user_id,
            categoria=categoria,
            grado=grado,
            dificultad=dificultad
        )
        
        if not texto_disponible:
            return {
                "success": False,
                "message": "No hay textos disponibles con los criterios especificados o ya completaste todos los textos disponibles",
                "data": None
            }
        
        texto_usuario_data = TextoUsuarioCreate(
            id_texto=texto_disponible.id_texto,
            id_user=user_id
        )
        
        try:
            TextoService.create_texto_usuario(db, texto_usuario_data)
        except Exception as e:
            print(f"Advertencia al registrar texto_usuario: {str(e)}")
        
        texto_completo = TextoService.get_texto_completo(db, texto_disponible.id_texto)
        
        return TextoService._formatear_respuesta_texto(texto_completo, question_type)
    
    @staticmethod
    def _formatear_respuesta_texto(texto: Texto, question_type: Optional[str]) -> Dict[str, Any]:
        preguntas_response = []
        
        for pregunta in texto.preguntas:
            if question_type and pregunta.tipo != question_type:
                continue
            
            alternativas_response = [
                {
                    "id_respuesta": alt.id_respuesta,
                    "contenido": alt.contenido
                }
                for alt in pregunta.alternativas
            ]
            
            preguntas_response.append({
                "id_pregunta": pregunta.id_pregunta,
                "contenido": pregunta.contenido,
                "tipo": pregunta.tipo,
                "alternativas": alternativas_response
            })
        
        return {
            "success": True,
            "message": "Texto asignado exitosamente",
            "data": {
                "texto": {
                    "id_texto": texto.id_texto,
                    "contenido": texto.contenido,
                    "categoria": texto.categoria,
                    "dificultad": texto.dificultad,
                    "grado": texto.grado
                },
                "preguntas": preguntas_response
            }
        }