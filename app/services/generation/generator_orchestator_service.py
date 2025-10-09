# app/services/generation/generation_orchestrator.py
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.services.generation.catalog_service import CatalogService
from app.services.generation.ai_generation_service import AIGenerationService
from app.services.generation.mapping_service import MappingService
from app.services.generation.storage_service import StorageService
from app.helper.file_utils_helper import FileUtils
from app.config.settings import settings
from app.exceptions import BusinessLogicException
import logging

logger = logging.getLogger(__name__)


class GenerationOrchestrator:
    
    def __init__(self, db: Session):
        self.db = db
        self.catalog_service = CatalogService(db)
        self.ai_service = AIGenerationService()
        self.mapping_service = MappingService()
        self.storage_service = StorageService(db)
        self.file_utils = FileUtils()
    
    def generar_textos(
        self,
        id_tipo_texto: int,
        id_tematicas: List[int],
        id_dificultades: List[int],
        textos_por_combinacion: int
    ) -> Dict[str, Any]:
        """
        Genera múltiples textos según las combinaciones especificadas.
        
        Flujo:
        1. Valida que los IDs existan
        2. Verifica límites
        3. Genera textos por cada combinación
        4. Guarda JSON temporal (opcional)
        5. Retorna resultado
        """
        self._validar_request(id_tipo_texto, id_tematicas, id_dificultades, textos_por_combinacion)
        
        tipo_texto_nombre = self.catalog_service.obtener_nombre_tipo_texto(id_tipo_texto)
        
        combinaciones = self._crear_combinaciones(
            id_tipo_texto,
            tipo_texto_nombre,
            id_tematicas,
            id_dificultades,
            textos_por_combinacion
        )
        
        textos_generados, bundle_json = self._procesar_combinaciones(
            combinaciones,
            tipo_texto_nombre
        )
        
        archivo_json = self._guardar_json_temporal(bundle_json, textos_generados)
        
        return {
            "textos_generados": len(textos_generados),
            "textos": textos_generados,
            "archivo_json": archivo_json
        }
    
    def _validar_request(
        self,
        id_tipo_texto: int,
        id_tematicas: List[int],
        id_dificultades: List[int],
        textos_por_combinacion: int
    ):
        """Valida que los IDs existan y no se excedan límites."""
        self.catalog_service.validar_ids_existen(
            id_tipo_texto,
            id_tematicas,
            id_dificultades
        )
        
        total_combinaciones = len(id_tematicas) * len(id_dificultades) * textos_por_combinacion
        
        if total_combinaciones > settings.MAX_TEXTOS_POR_REQUEST:
            raise BusinessLogicException(
                message=f"La solicitud excede el límite de {settings.MAX_TEXTOS_POR_REQUEST} textos",
                code="LIMITE_EXCEDIDO",
                details={
                    "total_solicitado": total_combinaciones,
                    "limite_maximo": settings.MAX_TEXTOS_POR_REQUEST
                }
            )
    
    def _crear_combinaciones(
        self,
        id_tipo_texto: int,
        tipo_texto_nombre: str,
        id_tematicas: List[int],
        id_dificultades: List[int],
        textos_por_combinacion: int
    ) -> List[Dict[str, Any]]:
        """Crea todas las combinaciones de generación necesarias."""
        combinaciones = []
        
        for id_tematica in id_tematicas:
            tematica_nombre = self.catalog_service.obtener_nombre_tematica(id_tematica)
            
            for id_dificultad in id_dificultades:
                dificultad_nombre = self.catalog_service.obtener_nombre_dificultad(id_dificultad)
                
                for _ in range(textos_por_combinacion):
                    combinaciones.append({
                        "id_tipo_texto": id_tipo_texto,
                        "tipo_texto_nombre": tipo_texto_nombre,
                        "id_tematica": id_tematica,
                        "tematica_nombre": tematica_nombre,
                        "id_dificultad": id_dificultad,
                        "dificultad_nombre": dificultad_nombre
                    })
        
        return combinaciones
    
    def _procesar_combinaciones(
        self,
        combinaciones: List[Dict[str, Any]],
        tipo_texto_nombre: str
    ) -> tuple:
        """Procesa cada combinación y genera los textos."""
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
                f"tipo={combo['tipo_texto_nombre']}, "
                f"tematica={combo['tematica_nombre']}, "
                f"dificultad={combo['dificultad_nombre']}"
            )
            
            try:
                resultado = self._generar_y_guardar_texto_simple(combo)
                
                textos_generados.append(resultado["info"])
                bundle_json["textos"].append(resultado["json_data"])
                
                logger.info(f"  ✓ Generado: {resultado['info']['titulo']}")
                
            except Exception as e:
                logger.error(f"  ✗ ERROR: {str(e)}")
                
                if not settings.GUARDAR_JSON_EN_ERROR:
                    raise
        
        bundle_json["metadata"]["total_generados"] = len(textos_generados)
        
        return textos_generados, bundle_json
    
    def _generar_y_guardar_texto_simple(
        self,
        combo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera un único texto con sus preguntas y lo guarda.
        
        Flujo simplificado:
        1. Generar texto con IA
        2. Generar preguntas con IA
        3. Mapear a formato BD
        4. Guardar en BD
        5. Retornar info
        """
        contenido_texto = self._generar_contenido_texto(combo)
        contenido_preguntas = self._generar_contenido_preguntas(contenido_texto, combo)
        datos_mapeados = self._mapear_contenido_a_bd(contenido_texto, contenido_preguntas, combo)
        id_texto = self._guardar_en_bd(datos_mapeados)
        
        return self._construir_resultado(id_texto, contenido_texto, contenido_preguntas, combo)
    
    def _generar_contenido_texto(self, combo: Dict[str, Any]) -> dict:
        """Llama a la IA para generar el texto."""
        return self.ai_service.generar_texto(
            tipo_texto_nombre=combo["tipo_texto_nombre"],
            tematica_nombre=combo["tematica_nombre"],
            dificultad_nombre=combo["dificultad_nombre"]
        )
    
    def _generar_contenido_preguntas(
        self,
        contenido_texto: dict,
        combo: Dict[str, Any]
    ) -> dict:
        """Llama a la IA para generar las preguntas."""
        tipo_pregunta_nombre = self.catalog_service.obtener_nombre_tipo_pregunta(
            settings.ID_TIPO_PREGUNTA_DEFAULT
        )
        
        return self.ai_service.generar_preguntas(
            texto=contenido_texto.get("cuento", ""),
            tipo_pregunta_nombre=tipo_pregunta_nombre,
            dificultad_nombre=combo["dificultad_nombre"]
        )
    
    def _mapear_contenido_a_bd(
        self,
        contenido_texto: dict,
        contenido_preguntas: dict,
        combo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mapea el contenido generado al formato de la BD."""
        texto_bd = self.mapping_service.mapear_texto_a_bd(
            contenido_ia=contenido_texto,
            id_tipo_texto=combo["id_tipo_texto"],
            id_tematica=combo["id_tematica"],
            id_dificultad=combo["id_dificultad"]
        )
        
        preguntas_bd = self.mapping_service.mapear_preguntas_a_bd(
            preguntas_ia=contenido_preguntas["preguntas"],
            id_texto=0,
            id_tipo_pregunta=settings.ID_TIPO_PREGUNTA_DEFAULT,
            id_dificultad=combo["id_dificultad"]
        )
        
        alternativas_bd = [
            self.mapping_service.mapear_alternativas_a_bd(
                alternativas_ia=pregunta["alternativas"],
                id_pregunta=0
            )
            for pregunta in contenido_preguntas["preguntas"]
        ]
        
        return {
            "texto": texto_bd,
            "preguntas": preguntas_bd,
            "alternativas": alternativas_bd
        }
    
    def _guardar_en_bd(self, datos_mapeados: Dict[str, Any]) -> int:
        """Guarda todo el contenido en la BD y retorna el ID del texto."""
        return self.storage_service.guardar_texto_completo(
            texto_data=datos_mapeados["texto"],
            preguntas_data=datos_mapeados["preguntas"],
            alternativas_por_pregunta=datos_mapeados["alternativas"]
        )
    
    def _construir_resultado(
        self,
        id_texto: int,
        contenido_texto: dict,
        contenido_preguntas: dict,
        combo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Construye el objeto de resultado con info y json_data."""
        return {
            "info": {
                "id_texto": id_texto,
                "titulo": contenido_texto.get("titulo", ""),
                "id_tematica": combo["id_tematica"],
                "id_dificultad": combo["id_dificultad"]
            },
            "json_data": {
                "id_texto": id_texto,
                "titulo": contenido_texto.get("titulo", ""),
                "contenido": contenido_texto.get("cuento", ""),
                "ensenanza": contenido_texto.get("ensenanza", ""),
                "tipo_texto": combo["tipo_texto_nombre"],
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
        """Guarda el JSON temporal si está configurado."""
        if not settings.GUARDAR_JSON_TEMPORAL or not textos_generados:
            return None
        
        tag = self.file_utils.now_tag()
        filename = f"bundle_{tag}.json"
        filepath = self.file_utils.save_json(bundle_json, filename)
        
        logger.info(f"JSON temporal guardado: {filepath}")
        
        return filename