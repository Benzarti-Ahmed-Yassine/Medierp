"""
Smart Medical AI - Face Recognition Service
Authentification biométrique via OpenCV
"""

import os
import json
import time
from typing import Optional, Dict, Any, Tuple
import cv2
import numpy as np

class FaceRecognitionService:
    """
    Service de biométrie faciale.
    Permet l'enrôlement et l'authentification des professionnels.
    """

    def __init__(self, data_dir: str = "./assets/biometrics/faces"):
        self.data_dir = data_dir
        self.cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
        
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.has_face_module = True
        except AttributeError:
            print("[FaceID] AVERTISSEMENT: Module 'cv2.face' non trouvé. Installez 'opencv-contrib-python'. Mode simulation activé.")
            self.recognizer = None
            self.has_face_module = False
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.is_trained = self._load_trained_data()

    def _load_trained_data(self) -> bool:
        """Charger les données d'entraînement existantes"""
        if not self.has_face_module:
            return False
            
        model_path = os.path.join(self.data_dir, "trainer.yml")
        if os.path.exists(model_path):
            try:
                self.recognizer.read(model_path)
                return True
            except Exception as e:
                print(f"[FaceID] Erreur chargement: {e}")
        return False

    def capture_and_train(self, user_id: int) -> bool:
        """Capturer des images et entraîner le modèle pour un utilisateur"""
        # Note: Dans une application réelle, on ouvrirait la caméra ici
        # Pour cette démo, on simule l'entraînement
        print(f"[FaceID] Enrôlement de l'utilisateur {user_id}...")
        time.sleep(2)
        return True

    def authenticate(self) -> Tuple[bool, Optional[int], float]:
        """
        Authentifier l'utilisateur via la webcam.
        Retourne: (success, user_id, confidence)
        """
        print("[FaceID] Initialisation de la caméra...")
        
        # Simuler une authentification réussie pour la démo
        # En production, on utiliserait cv2.VideoCapture(0)
        time.sleep(1.5)
        
        # Simuler un résultat positif pour l'utilisateur de démo (ID 1)
        return True, 1, 0.95

    def get_status(self) -> Dict[str, Any]:
        """État du service"""
        return {
            "ready": self.is_trained,
            "cascade_loaded": not self.face_cascade.empty(),
            "data_dir": self.data_dir
        }

# Instance globale
face_service = FaceRecognitionService()
