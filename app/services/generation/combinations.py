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
        """
        Crea combinaciones de: grado × tematica × dificultad × cantidad
        
        Args:
            id_tipo_texto: ID del tipo de texto
            tipo_texto_nombre: Nombre del tipo de texto
            id_tematicas: Lista de IDs de temáticas
            id_dificultades: Lista de IDs de dificultades
            id_grados: Lista de IDs de grados
            textos_por_combinacion: Cantidad de textos por cada combinación
            tipos_preguntas_distribuidos: Lista de IDs de tipos de preguntas distribuidos
                                         (ej: [1, 2, 3, 1, 2] para 5 preguntas)
        
        Returns:
            List[Dict]: Combinaciones con estructura completa incluyendo dificultad_escala
        """

        combinaciones = []
        
        for id_grado in id_grados:
            grado_nombre = self.catalog.obtener_nombre_grado(id_grado)
            
            for id_tematica in id_tematicas:
                tematica_nombre = self.catalog.obtener_nombre_tematica(id_tematica)
                
                for id_dificultad in id_dificultades:
                    dificultad_nombre = self.catalog.obtener_nombre_dificultad(id_dificultad)
                    
                    # Obtener escala 1-5 de dificultad
                    # Si existe en BD, obtenerla; si no, calcularla
                    dificultad_escala = self._calcular_escala_dificultad(id_dificultad)
                    
                    for _ in range(textos_por_combinacion):
                        combinaciones.append({
                            "id_tipo_texto": id_tipo_texto,
                            "tipo_texto_nombre": tipo_texto_nombre,
                            "id_tematica": id_tematica,
                            "tematica_nombre": tematica_nombre,
                            "id_dificultad": id_dificultad,
                            "dificultad_nombre": dificultad_nombre,
                            "dificultad_escala": dificultad_escala,  # ✅ NUEVO
                            "id_grado": id_grado,
                            "grado_nombre": grado_nombre,
                            "tipos_preguntas_distribuidos": tipos_preguntas_distribuidos or []  # ✅ NUEVO
                        })
        
        return combinaciones
    
    def _calcular_escala_dificultad(self, id_dificultad: int) -> int:
        """
        Calcula la escala 1-5 basada en el ID de dificultad.
        
        Mapeo por defecto:
        - ID 1 → Escala 1 (Muy Fácil)
        - ID 2 → Escala 2 (Fácil)
        - ID 3 → Escala 3 (Medio)
        - ID 4 → Escala 4 (Difícil)
        - ID 5 → Escala 5 (Muy Difícil)
        
        Si hay más de 5 dificultades en BD, distribuye proporcionalmente.
        
        Args:
            id_dificultad: ID de la dificultad desde BD
        
        Returns:
            int: Escala 1-5
        """
        # Mapeo simple si los IDs corresponden directamente a escalas
        if 1 <= id_dificultad <= 5:
            return id_dificultad
        
        # Si hay más de 5, distribuir proporcionalmente
        # Esto es fallback en caso de múltiples dificultades
        try:
            dificultades = self.catalog.obtener_todas_dificultades()
            total_dificultades = len(dificultades)
            
            # Encontrar índice del id_dificultad actual
            indices = [d["id_dificultad"] for d in dificultades]
            if id_dificultad in indices:
                indice_actual = indices.index(id_dificultad)
                # Mapear de 0 a total_dificultades-1 a 1-5
                escala = int((indice_actual / max(total_dificultades - 1, 1)) * 4) + 1
                return min(5, max(1, escala))
        except Exception:
            pass
        
        # Fallback: retornar escala media
        return 3
    
    def calcular_total_combinaciones(
        self,
        num_tematicas: int,
        num_dificultades: int,
        num_grados: int,
        textos_por_combinacion: int
    ) -> int:
        """
        Calcula el total de combinaciones que se generarán.
        
        Returns:
            int: Total de textos = tematicas × dificultades × grados × textos_por_combinacion
        """
        return num_tematicas * num_dificultades * num_grados * textos_por_combinacion


