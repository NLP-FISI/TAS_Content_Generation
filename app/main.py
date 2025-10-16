from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api import content, evaluation, generation
from app.database import init_db
from app.exceptions import (
    APIException,
    api_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

app = FastAPI(
    title="TAS Content API",
    description="API para gestión de contenido educativo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(content.router, tags=["Contenido"])
app.include_router(evaluation.router, tags=["Evaluación"])
app.include_router(generation.router, tags=["Generación"])

@app.get("/")
async def root():
    return {
        "message": "TAS Content API",
        "version": "1.0.0",
        "docs": "/docs"
    }