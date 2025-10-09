# app/services/base_service.py
from sqlalchemy.orm import Session
from app.database import get_models
from typing import Any, Optional

class BaseService:
    
    def __init__(self, db: Session):
        self.db = db
        self._models = None
    
    @property
    def models(self):
        if self._models is None:
            self._models = get_models()
        return self._models
    
    def get_model(self, model_name: str):
        return getattr(self.models, model_name, None)
    
    def find_by_id(self, model_class, id_field: str, id_value: Any) -> Optional[Any]:
        return self.db.query(model_class).filter(
            getattr(model_class, id_field) == id_value
        ).first()
    
    def find_all(self, model_class, **filters) -> list:
        query = self.db.query(model_class)
        for field, value in filters.items():
            if hasattr(model_class, field):
                query = query.filter(getattr(model_class, field) == value)
        return query.all()