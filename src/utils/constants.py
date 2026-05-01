"""
Smart Medical AI - Constantes globales
"""

from enum import Enum

# ============================================
# RÔLES UTILISATEURS
# ============================================
class UserRole(Enum):
    DOCTOR = "DOCTOR"
    ASSISTANT = "ASSISTANT"
    ADMIN = "ADMIN"

# ============================================
# NIVEAUX DE RISQUE
# ============================================
class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

RISK_COLORS = {
    RiskLevel.LOW: "#41cd52",
    RiskLevel.MEDIUM: "#ffd43b",
    RiskLevel.HIGH: "#e94560"
}

RISK_THRESHOLDS = {
    RiskLevel.LOW: (0, 30),
    RiskLevel.MEDIUM: (30, 70),
    RiskLevel.HIGH: (70, 100)
}

# ============================================
# TYPES DE RENDEZ-VOUS
# ============================================
class AppointmentType(Enum):
    CONSULTATION = "CONSULTATION"
    FOLLOW_UP = "FOLLOW_UP"
    URGENT = "URGENT"
    ROUTINE = "ROUTINE"

# ============================================
# STATUTS
# ============================================
class ConsultationStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

class PaymentStatus(Enum):
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"

# ============================================
# GROUPES SANGUINS
# ============================================
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ============================================
# COULEURS THÈME
# ============================================
THEME = {
    "background": "#0a0a1a",
    "surface": "#0f0f1a",
    "surface_light": "#1a1a2e",
    "primary": "#00d4ff",
    "danger": "#e94560",
    "success": "#41cd52",
    "warning": "#ffd43b",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0a0",
    "border": "#333333"
}

# ============================================
# SEUILS MÉDICAUX
# ============================================
VITAL_THRESHOLDS = {
    "systolic_bp": {"min": 90, "max": 140, "critical_high": 180},
    "diastolic_bp": {"min": 60, "max": 90, "critical_high": 110},
    "heart_rate": {"min": 60, "max": 100, "critical_low": 40, "critical_high": 120},
    "spo2": {"min": 95, "critical_low": 90},
    "temperature": {"min": 36.1, "max": 37.2, "critical_high": 39.0}
}

# ============================================
# CODES CCAM (exemples)
# ============================================
CCAM_CODES = {
    "C": {
        "code": "C",
        "description": "Consultation",
        "base_rate": 25.0
    },
    "CS": {
        "code": "CS",
        "description": "Consultation spécialisée",
        "base_rate": 30.0
    },
    "V": {
        "code": "V",
        "description": "Visite",
        "base_rate": 30.0
    },
    "VL": {
        "code": "VL",
        "description": "Visite longue",
        "base_rate": 40.0
    }
}

# ============================================
# FEATURES ML (pour prédiction cardiaque)
# ============================================
ML_FEATURES = [
    "age",
    "sex",
    "systolic_bp",
    "diastolic_bp",
    "cholesterol",
    "glucose",
    "smoker",
    "diabetes",
    "family_history_cvd"
]

# ============================================
# ÉVÉNEMENTS EVENT BUS
# ============================================
class EventType(Enum):
    PATIENT_CREATED = "patient.created"
    PATIENT_UPDATED = "patient.updated"
    CONSULTATION_STARTED = "consultation.started"
    CONSULTATION_COMPLETED = "consultation.completed"
    ML_PREDICTION_READY = "ml.prediction_ready"
    ALERT_TRIGGERED = "alert.triggered"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
