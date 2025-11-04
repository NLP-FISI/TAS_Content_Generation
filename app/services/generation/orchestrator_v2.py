# app/services/generation/orchestrator_v2.py

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.services.generation.catalog_service import CatalogService
from app.services.generation.validators import GenerationRequestValidator
from app.services.generation.combinations import CombinationBuilder
from app.services.generation.generators.texto_generator import TextoGenerator
from app.services.generation.mapping_service import MappingService
from app.services.generation.storage_service import StorageService
from app.helper.file_utils_helper import FileUtils
from app.helper.prompt_builder_helper import PromptBuilder
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class GenerationOrchestratorV2:
    
    def __init__(self, db: Session):
        self.db = db
        
        # Servicios principales
        self.catalog_service = CatalogService(db)
        self.validator = GenerationRequestValidator(self.catalog_service)
        self.combination_builder = CombinationBuilder(self.catalog_service)
        
        # Inyectar CatalogService en PromptBuilder
        self.prompt_builder = PromptBuilder(self.catalog_service)
        
        # Generador unificado (solo TextoGenerator, sin PreguntaGenerator)
        self.texto_generator = TextoGenerator(self.prompt_builder)
        
        # Servicios de almacenamiento
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
        """
        Orquesta el proceso completo de generación de contenido.
        
        Flujo:
        1. Validar IDs y límites
        2. Crear combinaciones
        3. Para cada combinación: Generar texto + preguntas (1 llamada IA)
        4. Mapear y guardar en BD
        5. Retornar resumen
        """

        try:
            # PASO 1: Validación
            self._paso_1_validar(
                id_tipo_texto, id_tematicas, id_dificultades, 
                id_grados, textos_por_combinacion
            )
            
            # PASO 2: Obtener nombre del tipo de texto
            tipo_texto_nombre = self.catalog_service.obtener_nombre_tipo_texto(id_tipo_texto)
            
            # PASO 3: Crear combinaciones
            combinaciones = self.combination_builder.crear_combinaciones(
                id_tipo_texto, tipo_texto_nombre, id_tematicas,
                id_dificultades, id_grados, textos_por_combinacion
            )
            
            # PASO 4: Procesar cada combinación
            textos_generados, bundle_json = self._paso_3_procesar(
                combinaciones, tipo_texto_nombre
            )
            
            # PASO 5: Guardar JSON temporal (opcional)
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
        """Valida que IDs existan y límites sean respetados"""
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
        """
        Procesa cada combinación: genera contenido, mapea y guarda.
        
        Returns:
            tuple: (textos_generados, bundle_json)
        """
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
                f"dificultad={combo['dificultad_nombre']} ({combo['dificultad_escala']}/5)"
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
        """
        Genera UN texto completo (texto + preguntas en 1 llamada IA).
        
        Args:
            combo: Dict con todos los parámetros de la combinación
        
        Returns:
            Dict con estructura: {"info": {...}, "json_data": {...}}
        """
        
        # Obtener distribución de tipos de preguntas
        tipos_preguntas_ids = self._distribuir_tipos_preguntas(
            settings.PREGUNTAS_POR_TEXTO
        )
        
        # Obtener nombres de tipos distribuidos
        tipos_preguntas_nombres = [
            self.catalog_service.obtener_nombre_tipo_pregunta(id_tipo)
            for id_tipo in tipos_preguntas_ids
        ]
        
        # GENERAR TEXTO + PREGUNTAS EN UNA SOLA LLAMADA IA ✅
        contenido = self.texto_generator.generar(
            id_grado=combo["id_grado"],
            id_tematica=combo["id_tematica"],
            id_tipo_texto=combo["id_tipo_texto"],
            id_dificultad=combo["id_dificultad"],
            dificultad_escala=combo["dificultad_escala"],
            tipos_preguntas=tipos_preguntas_nombres
        )
        
        # Mapear texto a formato BD
        texto_bd = self.mapping_service.mapear_texto_a_bd(
            contenido,
            combo["id_tipo_texto"],
            combo["id_tematica"],
            combo["id_dificultad"],
            combo["id_grado"]
        )
        
        # Mapear preguntas a formato BD (con tipo específico para cada una)
        preguntas_bd = self.mapping_service.mapear_preguntas_a_bd(
            contenido["preguntas"],
            0,  # id_texto será asignado tras insertar
            tipos_preguntas_ids,  # ✅ Pasar tipos distribuidos
            combo["id_dificultad"]
        )
        
        # Mapear alternativas (una lista por pregunta)
        alternativas_bd = [
            self.mapping_service.mapear_alternativas_a_bd(
                pregunta["alternativas"],
                0  # id_pregunta será asignado tras insertar
            )
            for pregunta in contenido["preguntas"]
        ]
        
        # GUARDAR EN BD (devuelve id_texto)
        id_texto = self.storage_service.guardar_texto_completo(
            texto_bd, preguntas_bd, alternativas_bd
        )
        
        return {
            "info": {
                "id_texto": id_texto,
                "titulo": contenido.get("titulo", ""),
                "id_tematica": combo["id_tematica"],
                "id_dificultad": combo["id_dificultad"],
                "id_grado": combo["id_grado"]
            },
            "json_data": {
                "id_texto": id_texto,
                "titulo": contenido.get("titulo", ""),
                "contenido": contenido.get("cuento", ""),
                "ensenanza": contenido.get("ensenanza", ""),
                "tipo_texto": combo["tipo_texto_nombre"],
                "grado": combo["grado_nombre"],
                "tematica": combo["tematica_nombre"],
                "dificultad": combo["dificultad_nombre"],
                "dificultad_escala": combo["dificultad_escala"],
                "preguntas": [
                    {
                        **pregunta,
                        "id_tipo_pregunta": tipos_preguntas_ids[i]
                    }
                    for i, pregunta in enumerate(contenido["preguntas"])
                ]
            }
        }
    
    def _distribuir_tipos_preguntas(self, num_preguntas: int) -> List[int]:
        """
        Distribuye tipos de preguntas de forma rotativa.
        
        Obtiene todos los tipos de la BD y los distribuye ciclando.
        
        Args:
            num_preguntas: Cantidad de preguntas (normalmente 5)
        
        Returns:
            List[int]: IDs de tipos distribuidos
            
        Ejemplo:
            Si hay 3 tipos (IDs: 1, 2, 3) y 5 preguntas:
            → [1, 2, 3, 1, 2]
        """
        tipos = self.catalog_service.obtener_tipos_preguntas()
        tipos_ids = [t["id_tipo_pregunta"] for t in tipos]
        
        distribuidos = []
        for i in range(num_preguntas):
            distribuidos.append(tipos_ids[i % len(tipos_ids)])
        
        logger.debug(f"Distribución de tipos: {distribuidos}")
        return distribuidos
    
    def _guardar_json_temporal(
        self,
        bundle_json: dict,
        textos_generados: List[dict]
    ) -> str:
        """
        Guarda un JSON con todos los textos generados (opcional, configurable).
        
        Returns:
            str: Nombre del archivo generado, o None si no se guardó
        """
        if not settings.GUARDAR_JSON_TEMPORAL or not textos_generados:
            return None
        
        tag = self.file_utils.now_tag()
        filename = f"bundle_{tag}.json"
        filepath = self.file_utils.save_json(bundle_json, filename)
        
        logger.info(f"JSON guardado: {filepath}")
        return filename