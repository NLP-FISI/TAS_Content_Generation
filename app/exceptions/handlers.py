# app/exceptions/handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.base import APIException
from app.schemas.responses import ErrorResponse, ErrorDetail
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Handler para excepciones personalizadas de la API"""
    
    logger.error(
        f"APIException: {exc.code} - {exc.message}",
        extra={
            "code": exc.code,
            "details": exc.details,
            "path": request.url.path
        }
    )
    
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
            details=exc.details
        ),
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler para errores de validación de Pydantic"""
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation error en {request.url.path}",
        extra={"errors": errors}
    )
    
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Error de validación en los datos enviados",
            details={"errors": errors}
        ),
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handler para errores de SQLAlchemy"""
    
    logger.error(
        f"Database error en {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="DATABASE_ERROR",
            message="Error al acceder a la base de datos",
            details={"error": "Error interno de base de datos"}
        ),
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler para excepciones no capturadas"""
    
    logger.error(
        f"Unhandled exception en {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="Error interno del servidor",
            details={"error": str(exc) if logger.level == logging.DEBUG else "Error interno"}
        ),
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )