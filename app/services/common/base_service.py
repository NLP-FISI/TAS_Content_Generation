# app/services/common/base_service.py
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
    
    def query(self, model_class):
        return self.db.query(model_class)
    
    def add(self, obj):
        self.db.add(obj)
    
    def commit(self):
        self.db.commit()
    
    def rollback(self):
        self.db.rollback()
    
    def flush(self):
        self.db.flush()