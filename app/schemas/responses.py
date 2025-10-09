# app/schemas/responses.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Código del error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Detalles adicionales del error")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "code": "RESOURCE_NOT_FOUND",
                "message": "Alternativa no encontrada",
                "details": {
                    "id_pregunta": 1,
                    "id_alternativa": 999
                }
            }
        }
    }


class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Indica si la operación fue exitosa")
    error: ErrorDetail = Field(..., description="Detalles del error")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp del error")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": False,
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": "Alternativa no encontrada",
                    "details": {
                        "id_pregunta": 1,
                        "id_alternativa": 999
                    }
                },
                "timestamp": "2025-10-08T10:30:00.000Z"
            }
        }
    }


class SuccessResponse(BaseModel):
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    data: Any = Field(..., description="Datos de respuesta")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la respuesta")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "data": {"id": 1, "name": "Ejemplo"},
                "timestamp": "2025-10-08T10:30:00.000Z"
            }
        }
    }