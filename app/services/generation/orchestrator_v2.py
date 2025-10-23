# app/services/generation/orchestrator_v2.py

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.services.generation.catalog_service import CatalogService
from app.services.generation.validators import GenerationRequestValidator
from app.services.generation.combinations import CombinationBuilder
from app.services.generation.generators.texto_generator import TextoGenerator
from app.services.generation.generators.pregunta_generator import PreguntaGenerator
from app.services.generation.mapping_service import MappingService
from app.services.generation.storage_service import StorageService
from app.helper.file_utils_helper import FileUtils
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class GenerationOrchestratorV2:
    
    def __init__(self, db: Session):
        self.db = db
        
        self.catalog_service = CatalogService(db)
        self.validator = GenerationRequestValidator(self.catalog_service)
        self.combination_builder = CombinationBuilder(self.catalog_service)
        
        self.texto_generator = TextoGenerator()
        self.pregunta_generator = PreguntaGenerator()
        
        self.mapping_service = MappingService()
        self.storage_service = StorageService(db)
        self.file_utils = FileUtils()
    
    def generar_textos(
        self,
        id_tipo_texto: int,
        id_tematicas: List[int],
        id_dificultades: List[int],
        id_grados: List[int],
        textos_por_combinacion: int
    ) -> Dict[str, Any]:

        try:
            self._paso_1_validar(
                id_tipo_texto, id_tematicas, id_dificultades, 
                id_grados, textos_por_combinacion
            )
            
            tipo_texto_nombre = self.catalog_service.obtener_nombre_tipo_texto(id_tipo_texto)
            combinaciones = self.combination_builder.crear_combinaciones(
                id_tipo_texto, tipo_texto_nombre, id_tematicas,
                id_dificultades, id_grados, textos_por_combinacion
            )
            
            textos_generados, bundle_json = self._paso_3_procesar(
                combinaciones, tipo_texto_nombre
            )
            
            archivo_json = self._guardar_json_temporal(bundle_json, textos_generados)
            
            return {
                "textos_generados": len(textos_generados),
                "textos": textos_generados,
                "archivo_json": archivo_json
            }
            
        except Exception as e:
            logger.error(f"Error en generación: {str(e)}", exc_info=True)
            raise
    
    def _paso_1_validar(
        self,
        id_tipo_texto: int,
        id_tematicas: List[int],
        id_dificultades: List[int],
        id_grados: List[int],
        textos_por_combinacion: int
    ) -> None:
        self.validator.validar_ids_existen(
            id_tipo_texto, id_tematicas, id_dificultades, id_grados
        )
        
        total = self.combination_builder.calcular_total_combinaciones(
            len(id_tematicas), len(id_dificultades), 
            len(id_grados), textos_por_combinacion
        )
        self.validator.validar_limites(total)
    
    def _paso_3_procesar(
        self,
        combinaciones: List[Dict[str, Any]],
        tipo_texto_nombre: str
    ) -> tuple:
        textos_generados = []
        bundle_json = {
            "textos": [],
            "metadata": {
                "tipo_texto": tipo_texto_nombre,
                "total_generados": 0
            }
        }
        
        total = len(combinaciones)
        
        for i, combo in enumerate(combinaciones, 1):
            logger.info(
                f"[{i}/{total}] Generando: "
                f"grado={combo['grado_nombre']}, "
                f"tematica={combo['tematica_nombre']}, "
                f"dificultad={combo['dificultad_nombre']}"
            )
            
            try:
                resultado = self._generar_uno(combo)
                textos_generados.append(resultado["info"])
                bundle_json["textos"].append(resultado["json_data"])
                logger.info(f"  ✓ {resultado['info']['titulo']}")
                
            except Exception as e:
                logger.error(f"  ✗ ERROR: {str(e)}")
                if not settings.GUARDAR_JSON_EN_ERROR:
                    raise
        
        bundle_json["metadata"]["total_generados"] = len(textos_generados)
        return textos_generados, bundle_json
    
    def _generar_uno(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        contenido_texto = self.texto_generator.generar(
            combo["grado_nombre"],
            combo["tematica_nombre"],
            combo["dificultad_nombre"]
        )
        
        contenido_preguntas = self.pregunta_generator.generar(
            contenido_texto.get("cuento", ""),
            "literal",
            combo["dificultad_nombre"]
        )
        
        texto_bd = self.mapping_service.mapear_texto_a_bd(
            contenido_texto,
            combo["id_tipo_texto"],
            combo["id_tematica"],
            combo["id_dificultad"],
            combo["id_grado"]
        )
        
        preguntas_bd = self.mapping_service.mapear_preguntas_a_bd(
            contenido_preguntas["preguntas"],
            0, 
            settings.ID_TIPO_PREGUNTA_DEFAULT,
            combo["id_dificultad"]
        )
        
        alternativas_bd = [
            self.mapping_service.mapear_alternativas_a_bd(
                pregunta["alternativas"],
                0
            )
            for pregunta in contenido_preguntas["preguntas"]
        ]
        
        id_texto = self.storage_service.guardar_texto_completo(
            texto_bd, preguntas_bd, alternativas_bd
        )
        
        return {
            "info": {
                "id_texto": id_texto,
                "titulo": contenido_texto.get("titulo", ""),
                "id_tematica": combo["id_tematica"],
                "id_dificultad": combo["id_dificultad"],
                "id_grado": combo["id_grado"]
            },
            "json_data": {
                "id_texto": id_texto,
                "titulo": contenido_texto.get("titulo", ""),
                "contenido": contenido_texto.get("cuento", ""),
                "ensenanza": contenido_texto.get("ensenanza", ""),
                "tipo_texto": combo["tipo_texto_nombre"],
                "grado": combo["grado_nombre"],
                "tematica": combo["tematica_nombre"],
                "dificultad": combo["dificultad_nombre"],
                "preguntas": contenido_preguntas["preguntas"]
            }
        }
    
    def _guardar_json_temporal(
        self,
        bundle_json: dict,
        textos_generados: List[dict]
    ) -> str:
        if not settings.GUARDAR_JSON_TEMPORAL or not textos_generados:
            return None
        
        tag = self.file_utils.now_tag()
        filename = f"bundle_{tag}.json"
        filepath = self.file_utils.save_json(bundle_json, filename)
        
        logger.info(f"JSON guardado: {filepath}")
        return filename