# app/services/generation/storage_service.py
from typing import Dict, List, Any
from sqlalchemy.exc import SQLAlchemyError
from app.services.base_service import BaseService
from app.exceptions import DatabaseException
import json
import logging

logger = logging.getLogger(__name__)

class StorageService(BaseService):
    
    def guardar_texto_completo(
        self,
        texto_data: Dict[str, Any],
        preguntas_data: List[Dict[str, Any]],
        alternativas_por_pregunta: List[List[Dict[str, Any]]]
    ) -> int:
        try:
            # Obtener modelos
            texto_model = self.get_model("texto")
            pregunta_model = self.get_model("pregunta")
            alternativa_model = self.get_model("alternativa")
            
            logger.info(f"Modelos obtenidos: texto={texto_model}, pregunta={pregunta_model}, alternativa={alternativa_model}")
            
            if not all([texto_model, pregunta_model, alternativa_model]):
                raise DatabaseException(
                    message="No se pudieron cargar los modelos necesarios",
                    details={
                        "texto": texto_model is not None,
                        "pregunta": pregunta_model is not None,
                        "alternativa": alternativa_model is not None
                    }
                )
            
            # Guardar texto
            logger.info(f"📝 Guardando texto con datos: {json.dumps(texto_data, ensure_ascii=False, indent=2)}")
            
            texto_obj = texto_model(**texto_data)
            self.db.add(texto_obj)
            self.db.flush()
            
            id_texto = texto_obj.id_texto
            logger.info(f"✅ Texto guardado con ID: {id_texto}")
            
            # Guardar preguntas y alternativas
            for i, pregunta_data in enumerate(preguntas_data):
                try:
                    pregunta_data["id_texto"] = id_texto
                    logger.info(f"📋 Guardando pregunta {i+1}/{len(preguntas_data)}: {json.dumps(pregunta_data, ensure_ascii=False, indent=2)}")
                    
                    pregunta_obj = pregunta_model(**pregunta_data)
                    self.db.add(pregunta_obj)
                    self.db.flush()
                    
                    id_pregunta = pregunta_obj.id_pregunta
                    logger.info(f"✅ Pregunta {i+1} guardada con ID: {id_pregunta}")
                    
                    # Guardar alternativas
                    for j, alternativa_data in enumerate(alternativas_por_pregunta[i]):
                        try:
                            alternativa_data["id_pregunta"] = id_pregunta
                            logger.info(f"   ✓ Alternativa {j+1}: {alternativa_data.get('contenido', '')[:50]}...")
                            
                            alternativa_obj = alternativa_model(**alternativa_data)
                            self.db.add(alternativa_obj)
                            
                        except Exception as e:
                            logger.error(f"❌ Error guardando alternativa {j+1}: {str(e)}")
                            raise
                    
                except Exception as e:
                    logger.error(f"❌ Error guardando pregunta {i+1}: {str(e)}")
                    raise
            
            # Commit final
            logger.info("💾 Ejecutando commit...")
            self.db.commit()
            logger.info(f"🎉 ÉXITO: Texto completo guardado (ID: {id_texto})")
            
            # Mostrar en consola el resultado
            print("\n" + "="*80)
            print("📊 TEXTO GENERADO Y GUARDADO")
            print("="*80)
            print(f"✓ ID Texto: {id_texto}")
            print(f"✓ Título: {texto_data.get('titulo', 'N/A')}")
            print(f"✓ Preguntas: {len(preguntas_data)}")
            print(f"✓ Alternativas por pregunta: {[len(alt) for alt in alternativas_por_pregunta]}")
            print("="*80 + "\n")
            
            return id_texto
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error SQLAlchemy: {str(e)}")
            self.db.rollback()
            raise DatabaseException(
                message="Error al guardar el texto completo en la base de datos",
                details={"error": str(e), "type": type(e).__name__}
            )
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
            self.db.rollback()
            raise DatabaseException(
                message="Error inesperado al guardar en la base de datos",
                details={"error": str(e), "type": type(e).__name__}
            )