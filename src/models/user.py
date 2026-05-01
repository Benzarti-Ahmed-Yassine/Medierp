"""
Smart Medical AI - User Model
"""

from typing import Optional, List
from .base import BaseModel
from ..core.database import DatabaseManager


class User(BaseModel):
    _table_name = "users"
    _fields = ["id", "email", "password_hash", "role", "full_name", 
               "phone", "rpps_number", "specialty", "is_active", 
               "last_login", "created_at"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: Optional[int] = kwargs.get("id")
        self.email: str = kwargs.get("email", "")
        self.password_hash: str = kwargs.get("password_hash", "")
        self.role: str = kwargs.get("role", "ASSISTANT")
        self.full_name: str = kwargs.get("full_name", "")
        self.phone: Optional[str] = kwargs.get("phone")
        self.rpps_number: Optional[str] = kwargs.get("rpps_number")
        self.specialty: str = kwargs.get("specialty", "")
        self.is_active: bool = kwargs.get("is_active", True)

    @staticmethod
    def get_by_email(email: str) -> Optional["User"]:
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM users WHERE email = ?", (email,))
        return User.from_db(row) if row else None

    @staticmethod
    def get_by_id(user_id: int) -> Optional["User"]:
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        return User.from_db(row) if row else None

    @staticmethod
    def get_all() -> List["User"]:
        db = DatabaseManager()
        rows = db.fetch_all("SELECT * FROM users WHERE is_active = 1 ORDER BY full_name")
        return [User.from_db(row) for row in rows]

    def save(self) -> int:
        db = DatabaseManager()
        data = self.to_dict()
        if "id" in data:
            del data["id"]

        if self.id:
            db.update("users", data, "id = ?", (self.id,))
            return self.id
        else:
            self.id = db.insert("users", data)
            return self.id
