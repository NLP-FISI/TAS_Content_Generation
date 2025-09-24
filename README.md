# Proyecto FastAPI con MySQL

Proyecto con una ruta para generación de contenido y modelos ORM para MySQL.

## Estructura del Proyecto

```
tas_content_generation/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Base de Datos

### Tablas:
- `texto`: Contenido educativo con categoría, dificultad y grado
- `texto_usuario`: Relación entre usuarios y textos
- `preguntas`: Preguntas asociadas a cada texto
- `alternativa`: Opciones de respuesta para cada pregunta

## Instalación

### Opción 1: Python estándar
1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tu DATABASE_URL
   ```

4. Crear tablas y datos de ejemplo:
   ```bash
   python app/seed_data.py
   ```

### Opción 2: Python 3 explícito
1. Crear un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tu DATABASE_URL
   ```

4. La base de datos ya está configurada con datos de ejemplo

## Uso

Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

## Endpoint

- `GET /content` - Recibe JSON con user_id, grade, category

Ejemplo de uso:
```bash
curl -X GET "http://localhost:8000/content" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "grade": "5to", "category": "matematicas"}'
```

## Modelos ORM

Los modelos están listos para usar con SQLAlchemy:
- `Texto`: Contenido educativo
- `TextoUsuario`: Relación usuario-texto
- `Preguntas`: Preguntas por texto
- `Alternativa`: Opciones de respuesta

## CRUD Operations

Funciones disponibles en `crud.py`:
- `get_texto()`: Obtener texto por ID
- `get_textos_by_categoria()`: Filtrar por categoría
- `get_textos_by_grado()`: Filtrar por grado
- `get_textos_by_user()`: Textos de un usuario
- `get_texto_completo()`: Texto con preguntas y alternativas
