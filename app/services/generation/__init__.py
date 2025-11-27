# app/services/generation/__init__.py

# Versión nueva (refactorizada)
from .orchestrator_v2 import GenerationOrchestratorV2

# Componentes individuales
from .generators import BaseGenerator, TextoGenerator
from .validators import GenerationRequestValidator
from .combinations import CombinationBuilder
from .catalog_service import CatalogService
from .mapping_service import MappingService
from .storage_service import StorageService
from .guardar_en_bd import GuardarEnBDService

__all__ = [
    "GenerationOrchestratorV2",         
    
    # Componentes
    "BaseGenerator",
    "TextoGenerator",
    "GenerationRequestValidator",
    "CombinationBuilder",
    "CatalogService",
    "MappingService",
    "StorageService",
    "GuardarEnBDService"
]