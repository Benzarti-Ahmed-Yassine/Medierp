"""
Smart Medical AI - Base Model (ORM léger)
"""

from typing import Dict, Any, Optional
from datetime import datetime


class BaseModel:
    """
    Classe de base pour tous les modèles.
    Fournit sérialisation/désérialisation commune.
    """

    _table_name: str = ""
    _fields: list = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_db(cls, row: Dict[str, Any]) -> "BaseModel":
        """Créer un modèle depuis une ligne DB"""
        return cls(**dict(row))

    def to_dict(self) -> Dict[str, Any]:
        """Convertir en dictionnaire"""
        return {
            field: getattr(self, field, None)
            for field in self._fields
            if hasattr(self, field)
        }

    def to_json(self) -> str:
        """Convertir en JSON"""
        import json
        data = self.to_dict()
        # Convertir datetime en string
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return json.dumps(data, indent=2, default=str)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()})"
