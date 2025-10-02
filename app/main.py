from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import content

app = FastAPI(
    title="TAS Content API",
    description="API para gestión de contenido educativo",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(content.router, tags=["Contenido"])

@app.get("/")
async def root():
    return {
        "message": "TAS Content API",
        "version": "1.0.0",
        "docs": "/docs"
    }