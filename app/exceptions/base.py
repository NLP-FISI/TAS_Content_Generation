# app/exceptions/base.py
from typing import Optional, Dict, Any

class APIException(Exception):
    """Excepción base para todas las excepciones personalizadas de la API"""
    
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundException(APIException):
    """Excepción cuando no se encuentra un recurso"""
    
    def __init__(self, message: str = "Recurso no encontrado", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details=details
        )


class ValidationException(APIException):
    """Excepción para errores de validación"""
    
    def __init__(self, message: str = "Error de validación", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class DatabaseException(APIException):
    """Excepción para errores de base de datos"""
    
    def __init__(self, message: str = "Error de base de datos", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details
        )


class BusinessLogicException(APIException):
    """Excepción para errores de lógica de negocio"""
    
    def __init__(self, message: str, code: str = "BUSINESS_LOGIC_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=code,
            status_code=400,
            details=details
        )