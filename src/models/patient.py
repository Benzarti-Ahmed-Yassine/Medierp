"""
Smart Medical AI - Patient Model
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from .base import BaseModel
from ..core.database import DatabaseManager


class Patient(BaseModel):
    _table_name = "patients"
    _fields = ["id", "cin", "first_name", "last_name", "date_of_birth",
               "sex", "phone", "email", "address", "city", "postal_code",
               "blood_type", "weight_kg", "height_cm", "emergency_contact_name",
               "emergency_contact_phone", "insurance_provider", "insurance_number",
               "is_active", "created_at", "updated_at"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: Optional[int] = kwargs.get("id")
        self.cin: Optional[str] = kwargs.get("cin")
        self.first_name: str = kwargs.get("first_name", "")
        self.last_name: str = kwargs.get("last_name", "")
        self.date_of_birth: Optional[date] = kwargs.get("date_of_birth")
        self.sex: Optional[str] = kwargs.get("sex")
        self.phone: Optional[str] = kwargs.get("phone")
        self.email: Optional[str] = kwargs.get("email")
        self.address: Optional[str] = kwargs.get("address")
        self.city: Optional[str] = kwargs.get("city")
        self.postal_code: Optional[str] = kwargs.get("postal_code")
        self.blood_type: Optional[str] = kwargs.get("blood_type")
        self.weight_kg: Optional[float] = kwargs.get("weight_kg")
        self.height_cm: Optional[float] = kwargs.get("height_cm")
        self.emergency_contact_name: Optional[str] = kwargs.get("emergency_contact_name")
        self.emergency_contact_phone: Optional[str] = kwargs.get("emergency_contact_phone")
        self.insurance_provider: Optional[str] = kwargs.get("insurance_provider")
        self.insurance_number: Optional[str] = kwargs.get("insurance_number")
        self.is_active: bool = kwargs.get("is_active", True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @property
    def bmi(self) -> Optional[float]:
        if self.weight_kg and self.height_cm and self.height_cm > 0:
            return round(self.weight_kg / ((self.height_cm / 100) ** 2), 1)
        return None

    @staticmethod
    def get_by_id(patient_id: int) -> Optional["Patient"]:
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM patients WHERE id = ?", (patient_id,))
        return Patient.from_db(row) if row else None

    @staticmethod
    def search(query: str, limit: int = 50) -> List["Patient"]:
        db = DatabaseManager()
        sql = """SELECT * FROM patients 
                   WHERE is_active = 1 
                   AND (first_name LIKE ? OR last_name LIKE ? OR cin LIKE ? OR phone LIKE ?)
                   ORDER BY last_name, first_name
                   LIMIT ?"""
        params = (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", limit)
        rows = db.fetch_all(sql, params)
        return [Patient.from_db(row) for row in rows]

    @staticmethod
    def get_all(limit: int = 1000) -> List["Patient"]:
        db = DatabaseManager()
        rows = db.fetch_all(
            "SELECT * FROM patients WHERE is_active = 1 ORDER BY last_name, first_name LIMIT ?",
            (limit,)
        )
        return [Patient.from_db(row) for row in rows]

    def get_allergies(self) -> List[Dict]:
        db = DatabaseManager()
        return db.fetch_all("SELECT * FROM allergies WHERE patient_id = ?", (self.id,))

    def get_family_history(self) -> List[Dict]:
        db = DatabaseManager()
        return db.fetch_all("SELECT * FROM family_history WHERE patient_id = ?", (self.id,))

    def get_last_risk_score(self) -> Optional[Dict]:
        db = DatabaseManager()
        return db.fetch_one(
            """SELECT risk_score, risk_level, start_time as date 
               FROM consultations 
               WHERE patient_id = ? AND status = 'COMPLETED'
               ORDER BY start_time DESC LIMIT 1""",
            (self.id,)
        )

    def save(self) -> int:
        db = DatabaseManager()
        data = self.to_dict()

        # Convertir date en string
        if self.date_of_birth and isinstance(self.date_of_birth, date):
            data["date_of_birth"] = self.date_of_birth.isoformat()

        if "id" in data:
            del data["id"]
        if "created_at" in data:
            del data["created_at"]

        data["updated_at"] = datetime.now().isoformat()

        if self.id:
            db.update("patients", data, "id = ?", (self.id,))
            return self.id
        else:
            self.id = db.insert("patients", data)
            return self.id

    def soft_delete(self) -> None:
        """Suppression logique (GDPR)"""
        db = DatabaseManager()
        db.update("patients", {"is_active": 0}, "id = ?", (self.id,))
