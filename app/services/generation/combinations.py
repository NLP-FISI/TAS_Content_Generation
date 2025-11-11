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
        textos_por_combinacion: int,
        tipos_preguntas_distribuidos: List[int] = None
    ) -> List[Dict[str, Any]]:

        combinaciones = []
        
        for id_grado in id_grados:
            grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
            
            for id_tematica in id_tematicas:
                tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
                
                for id_dificultad in id_dificultades:
                    dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)
                    
                    dificultad_escala = self._calcular_escala_dificultad(id_dificultad)
                    
                    for _ in range(textos_por_combinacion):
                        combinaciones.append({
                            "id_tipo_texto": id_tipo_texto,
                            "tipo_texto_nombre": tipo_texto_nombre,
                            "id_tematica": id_tematica,
                            "tematica_nombre": tematica_nombre,
                            "id_dificultad": id_dificultad,
                            "dificultad_nombre": dificultad_nombre,
                            "dificultad_escala": dificultad_escala,  
                            "id_grado": id_grado,
                            "grado_nombre": grado_nombre,
                            "tipos_preguntas_distribuidos": tipos_preguntas_distribuidos or [] 
                        })
        
        return combinaciones
    
    def _calcular_escala_dificultad(self, id_dificultad: int) -> int:

        if 1 <= id_dificultad <= 5:
            return id_dificultad
        
        try:
            dificultades = self.catalog.obtener_todas_dificultades()
            total_dificultades = len(dificultades)
            
            indices = [d["id_dificultad"] for d in dificultades]
            if id_dificultad in indices:
                indice_actual = indices.index(id_dificultad)
                escala = int((indice_actual / max(total_dificultades - 1, 1)) * 4) + 1
                return min(5, max(1, escala))
        except Exception:
            pass
        
        return 3
    
    def calcular_total_combinaciones(
        self,
        num_tematicas: int,
        num_dificultades: int,
        num_grados: int,
        textos_por_combinacion: int
    ) -> int:
        
        return num_tematicas * num_dificultades * num_grados * textos_por_combinacion


