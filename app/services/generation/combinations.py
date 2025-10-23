# app/services/generation/combinations.py
from typing import List, Dict, Any

class CombinationBuilder:
    
    def __init__(self, catalog_service):
        self.catalog = catalog_service
    
    def crear_combinaciones(
        self,
        id_tipo_texto: int,
        tipo_texto_nombre: str,
        id_tematicas: List[int],
        id_dificultades: List[int],
        id_grados: List[int],
        textos_por_combinacion: int
    ) -> List[Dict[str, Any]]:

        combinaciones = []
        
        for id_grado in id_grados:
            grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
            
            for id_tematica in id_tematicas:
                tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
                
                for id_dificultad in id_dificultades:
                    dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)
                    
                    for _ in range(textos_por_combinacion):
                        combinaciones.append({
                            "id_tipo_texto": id_tipo_texto,
                            "tipo_texto_nombre": tipo_texto_nombre,
                            "id_tematica": id_tematica,
                            "tematica_nombre": tematica_nombre,
                            "id_dificultad": id_dificultad,
                            "dificultad_nombre": dificultad_nombre,
                            "id_grado": id_grado,
                            "grado_nombre": grado_nombre
                        })
        
        return combinaciones
    
    def calcular_total_combinaciones(
        self,
        num_tematicas: int,
        num_dificultades: int,
        num_grados: int,
        textos_por_combinacion: int
    ) -> int:
        return num_tematicas * num_dificultades * num_grados * textos_por_combinacion