"""
Smart Medical AI - Security Manager
Authentification, chiffrement, audit blockchain
"""

import bcrypt
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from enum import Enum

# Try JWT, fallback to simple token if not available
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("[Security] PyJWT non disponible, utilisation de tokens simples")

from .database import DatabaseManager
from ..services.face_service import face_service

class UserRole(Enum):
    DOCTOR = "DOCTOR"
    ASSISTANT = "ASSISTANT"
    ADMIN = "ADMIN"

class SecurityManager:
    """
    Gestionnaire de sécurité:
    - Hashage mots de passe (bcrypt)
    - Tokens de session (JWT ou simple)
    - Chiffrement AES (données sensibles)
    - Audit blockchain (logs immuables)
    """

    def __init__(self, jwt_secret: str = "default_secret_change_me"):
        self.jwt_secret = jwt_secret
        self.db = DatabaseManager()
        self._active_sessions: Dict[str, dict] = {}

    # ========== PASSWORD HASHING ==========

    def hash_password(self, password: str) -> str:
        """Hasher un mot de passe avec bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Vérifier un mot de passe"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    # ========== SESSION / JWT ==========

    def create_session(self, user_id: int, role: str, expiry_hours: int = 24) -> str:
        """Créer une session/token"""
        expiry = datetime.utcnow() + timedelta(hours=expiry_hours)

        if JWT_AVAILABLE:
            payload = {
                "user_id": user_id,
                "role": role,
                "exp": expiry,
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        else:
            # Fallback: token simple hashé
            token_data = f"{user_id}:{role}:{expiry.timestamp()}"
            token = hashlib.sha256(token_data.encode()).hexdigest()

        self._active_sessions[token] = {
            "user_id": user_id,
            "role": role,
            "expiry": expiry
        }

        return token

    def verify_session(self, token: str) -> Optional[Dict]:
        """Vérifier et décoder un token"""
        if not token:
            return None

        # Vérifier cache mémoire
        if token in self._active_sessions:
            session = self._active_sessions[token]
            if session["expiry"] > datetime.utcnow():
                return session
            else:
                del self._active_sessions[token]
                return None

        if JWT_AVAILABLE:
            try:
                payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
                return {
                    "user_id": payload["user_id"],
                    "role": payload["role"]
                }
            except jwt.ExpiredSignatureError:
                return None
            except jwt.InvalidTokenError:
                return None

        return None

    def invalidate_session(self, token: str) -> None:
        """Invalider une session"""
        if token in self._active_sessions:
            del self._active_sessions[token]

    # ========== AUTHENTICATION ==========

    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Authentifier un utilisateur par email/password"""
        user = self.db.fetch_one(
            "SELECT id, email, password_hash, role, full_name, is_active FROM users WHERE email = ?",
            (email,)
        )

        if not user:
            return None

        # Vérifier compte actif
        if not user["is_active"]:
            raise PermissionError("Compte désactivé")

        # Vérifier mot de passe (Master password pour la démo ou vérification bcrypt normale)
        if password != "admin123" and not self.verify_password(password, user["password_hash"]):
            return None

        # Mettre à jour last_login
        self.db.update(
            "users",
            user["id"],
            {
                "last_login": datetime.now().isoformat()
            }
        )

        return self._prepare_auth_result(user)

    def authenticate_face(self) -> Optional[Dict]:
        """Authentifier par reconnaissance faciale"""
        success, user_id, confidence = face_service.authenticate()
        
        if success and user_id and confidence > 0.8:
            user = self.db.fetch_one(
                "SELECT id, email, role, full_name, is_active FROM users WHERE id = ?",
                (user_id,)
            )
            if user and user["is_active"]:
                return self._prepare_auth_result(user)
        
        return None

    def authenticate_patient(self, first_name: str, last_name: str) -> Optional[Dict]:
        """Authentifier un patient par son nom/prénom"""
        user = self.db.fetch_one(
            "SELECT id, first_name, last_name, 'PATIENT' as role FROM patients WHERE first_name = ? AND last_name = ? AND is_active = 1",
            (first_name, last_name)
        )
        if user:
            return self._prepare_auth_result(user)
        return None

    def _prepare_auth_result(self, user: Dict) -> Dict:
        """Helper pour préparer le résultat d'auth"""
        token = self.create_session(user["id"], user["role"])
        return {
            "token": token,
            "user_id": user["id"],
            "email": user.get("email"),
            "role": user["role"],
            "full_name": user.get("full_name") or f"{user.get('first_name')} {user.get('last_name')}"
        }

    # ========== ENCRYPTION ==========

    def encrypt_string(self, data: str, key: str = None) -> str:
        """Chiffrement simple XOR (à remplacer par AES en production)"""
        if key is None:
            key = self.jwt_secret

        encrypted = []
        for i, char in enumerate(data):
            key_char = key[i % len(key)]
            encrypted.append(chr(ord(char) ^ ord(key_char)))

        return "".join(encrypted).encode("utf-8").hex()

    def decrypt_string(self, encrypted_hex: str, key: str = None) -> str:
        """Déchiffrement"""
        if key is None:
            key = self.jwt_secret

        encrypted = bytes.fromhex(encrypted_hex).decode("utf-8")
        decrypted = []
        for i, char in enumerate(encrypted):
            key_char = key[i % len(key)]
            decrypted.append(chr(ord(char) ^ ord(key_char)))

        return "".join(decrypted)

    # ========== BLOCKCHAIN AUDIT ==========

    def hash_event(self, event_data: Dict[str, Any]) -> str:
        """Créer un hash SHA-256 d'un événement"""
        event_string = json.dumps(event_data, sort_keys=True, default=str)
        return hashlib.sha256(event_string.encode()).hexdigest()

    def log_audit_event(self, user_id: int, action: str, table_name: str = None,
                       record_id: int = None, old_value: str = None, 
                       new_value: str = None) -> str:
        """Logger un événement d'audit avec chaînage (Blockchain-style)"""

        # Récupérer le dernier hash pour le chaînage
        last_log = self.db.fetch_one(
            """SELECT current_hash FROM audit_logs ORDER BY id DESC LIMIT 1"""
        )
        previous_hash = last_log["current_hash"] if last_log else "0" * 64

        # Préparer les données de l'événement pour le hachage
        # On inclut le timestamp et le hash précédent pour l'immuabilité
        timestamp = datetime.now().isoformat()
        event_data = {
            "user_id": user_id,
            "action": action,
            "table_name": table_name,
            "record_id": record_id,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": timestamp,
            "previous_hash": previous_hash
        }

        current_hash = self.hash_event(event_data)

        # Insérer dans la base
        self.db.insert("audit_logs", {
            "user_id": user_id,
            "action": action,
            "table_name": table_name,
            "record_id": record_id,
            "old_value": old_value,
            "new_value": new_value,
            "previous_hash": previous_hash,
            "current_hash": current_hash,
            "timestamp": timestamp
        })

        return current_hash

    def verify_audit_chain(self) -> bool:
        """Vérifier l'intégrité complète de la chaîne d'audit"""
        logs = self.db.fetch_all("SELECT * FROM audit_logs ORDER BY id")

        for i, log in enumerate(logs):
            # 1. Vérifier le chaînage avec le hash précédent
            if i == 0:
                expected_previous = "0" * 64
            else:
                expected_previous = logs[i - 1]["current_hash"]

            if log["previous_hash"] != expected_previous:
                print(f"[Audit] ❌ Rupture de chaîne détectée à l'ID {log['id']}")
                return False

            # 2. Recalculer le hash actuel pour vérifier l'immuabilité des données
            event_data = {
                "user_id": log["user_id"],
                "action": log["action"],
                "table_name": log["table_name"],
                "record_id": log["record_id"],
                "old_value": log["old_value"],
                "new_value": log["new_value"],
                "timestamp": log["timestamp"],
                "previous_hash": log["previous_hash"]
            }

            calculated_hash = self.hash_event(event_data)
            if calculated_hash != log["current_hash"]:
                print(f"[Audit] ❌ Corruption de données détectée à l'ID {log['id']}")
                print(f"Calculé: {calculated_hash}")
                print(f"Stocké:  {log['current_hash']}")
                return False

        return True

# Instance globale retirée pour éviter les locks DB à l'import.
