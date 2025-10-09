import re
import json
from typing import Dict, List
from app.config.ai_client import AIClient
from app.helper.prompt_builder_helper import PromptBuilder
from app.config.settings import settings

class GeneratorService:
    
    def __init__(self):
        self.ai_client = AIClient()
        self.prompt_builder = PromptBuilder()
    
    @staticmethod
    def parse_json_from_text(text: str) -> dict:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not m:
            raise ValueError("La respuesta del modelo no contiene un bloque JSON.")
        return json.loads(m.group(0))
    
    @staticmethod
    def estima_dificultad(grado: int, palabras: int) -> str:
        if grado <= 3:
            return "facil"
        elif grado <= 5:
            if palabras >= 300:
                return "media"
            return "facil"
        else:
            if palabras >= 300:
                return "dificil"
            return "media"
    
    def generar_texto(self, grado: int, categoria: str) -> dict:
        prompt = self.prompt_builder.build_texto_prompt(grado, categoria)
        raw_response = self.ai_client.call(prompt)
        return self.parse_json_from_text(raw_response)
    
    def generar_preguntas(self, texto: str) -> dict:
        prompt = self.prompt_builder.build_preguntas_prompt(
            texto,
            settings.PREGUNTAS_POR_CUENTO,
            settings.ALTERNATIVAS_POR_PREGUNTA
        )
        raw_response = self.ai_client.call(prompt)
        return self.parse_json_from_text(raw_response)
    
    def generar_contenido_completo(self, grado: int, categoria: str) -> dict:
        texto_data = self.generar_texto(grado, categoria)
        
        texto_cuento = texto_data.get("cuento", "")
        palabras = int(texto_data.get("palabras_aprox", 0))
        
        preguntas_data = self.generar_preguntas(texto_cuento)
        
        return {
            "titulo": texto_data.get("titulo", ""),
            "cuento": texto_cuento,
            "ensenanza": texto_data.get("ensenanza", ""),
            "palabras_aprox": palabras,
            "dificultad": self.estima_dificultad(grado, palabras),
            "grado": grado,
            "categoria": categoria,
            "preguntas": preguntas_data.get("preguntas", [])
        }
    
    def to_db_format(self, contenido: dict, base_ids: Dict[str, int]) -> Dict[str, List[dict]]:
        base_ids.setdefault("texto", 0)
        base_ids.setdefault("pregunta", 0)
        base_ids.setdefault("alternativa", 0)
        
        base_ids["texto"] += 1
        id_texto = base_ids["texto"]
        
        texto_row = {
            "id_texto": id_texto,
            "contenido": contenido.get("cuento", "").strip(),
            "categoria": contenido.get("categoria", ""),
            "dificultad": contenido.get("dificultad", ""),
            "grado": str(contenido.get("grado", ""))
        }
        
        preguntas_rows: List[dict] = []
        alternativas_rows: List[dict] = []
        
        preguntas = contenido.get("preguntas", [])[:settings.PREGUNTAS_POR_CUENTO]
        
        for q in preguntas:
            base_ids["pregunta"] += 1
            pid = base_ids["pregunta"]
            
            preguntas_rows.append({
                "id_pregunta": pid,
                "id_texto": id_texto,
                "contenido": q.get("enunciado", "").strip(),
                "tipo": "opcion_multiple"
            })
            
            alts = q.get("alternativas", [])[:settings.ALTERNATIVAS_POR_PREGUNTA]
            any_correct = any(a.get("es_correcta") for a in alts)
            
            for i, a in enumerate(alts):
                base_ids["alternativa"] += 1
                alternativas_rows.append({
                    "id_respuesta": base_ids["alternativa"],
                    "id_pregunta": pid,
                    "bool": bool(a.get("es_correcta")) if any_correct else (i == 0),
                    "contenido": a.get("texto", "").strip()
                })
        
        return {
            "Texto": [texto_row],
            "Preguntas": preguntas_rows,
            "Alternativa": alternativas_rows
        }