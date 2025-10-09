from ..services.generations.text_prompt_service import GeneratorService
from app.helper.file_utils_helper import FileUtils
from app.config.openrouter_config import settings

def main():
    generator = GeneratorService()
    file_utils = FileUtils()
    
    tag = file_utils.now_tag()
    bundle = {
        "Texto": [],
        "Preguntas": [],
        "Alternativa": []
    }
    counters = {"texto": 0, "pregunta": 0, "alternativa": 0}
    
    total_objetivo = (
        len(settings.CATEGORIAS) * 
        len(settings.GRADOS) * 
        settings.CUENTOS_POR_CATEGORIA
    )
    
    print(f"Usando modelo: {settings.OPENROUTER_MODEL}")
    print(f"Total a generar: {total_objetivo} textos\n")
    
    n = 0
    for categoria in settings.CATEGORIAS:
        for grado in settings.GRADOS:
            for _ in range(settings.CUENTOS_POR_CATEGORIA):
                n += 1
                print(f"[{n}/{total_objetivo}] Generando: categoria='{categoria}', grado={grado}...")
                
                try:
                    contenido = generator.generar_contenido_completo(grado, categoria)
                    
                    mapped = generator.to_db_format(contenido, counters)
                    
                    bundle["Texto"].extend(mapped["Texto"])
                    bundle["Preguntas"].extend(mapped["Preguntas"])
                    bundle["Alternativa"].extend(mapped["Alternativa"])
                    
                    print(f"  ✓ Generado: {contenido.get('titulo', 'Sin título')}")
                    
                except Exception as e:
                    print(f"  ✗ ERROR: {e}")
                    continue
    
    output_file = file_utils.save_json(bundle, f"bundle_{tag}.json")
    
    print("\n== Listo ==")
    print(f"Archivo generado: {output_file}")
    print(f"Textos: {len(bundle['Texto'])}")
    print(f"Preguntas: {len(bundle['Preguntas'])}")
    print(f"Alternativas: {len(bundle['Alternativa'])}")

if __name__ == "__main__":
    main()