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
        """Capturer des images et entraîner le modèle pour un utilisateur spécifique"""
        if not self.has_face_module:
            print("[FaceID] ❌ Module Face non disponible. Impossible d'enrôler.")
            return False

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[FaceID] ❌ Caméra non détectée.")
            return False

        print(f"[FaceID] Enrôlement de l'utilisateur {user_id}. Regardez la caméra...")
        
        face_samples = []
        ids = []
        count = 0
        max_samples = 30 # Nombre d'échantillons pour un bon entraînement

        while count < max_samples:
            ret, frame = cap.read()
            if not ret: break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                count += 1
                face_samples.append(gray[y:y+h, x:x+w])
                ids.append(user_id)
                
                # Visualisation optionnelle (si on avait une fenêtre de prévisualisation)
                # cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            
            if count % 5 == 0:
                print(f"[FaceID] Progression: {count}/{max_samples}")
            
            time.sleep(0.1)

        cap.release()

        if len(face_samples) > 0:
            print(f"[FaceID] Entraînement avec {len(face_samples)} échantillons...")
            # Si le modèle existe déjà, on pourrait utiliser update(), sinon train()
            # Pour la démo, on ré-entraîne tout
            self.recognizer.train(face_samples, np.array(ids))
            
            # Sauvegarder le modèle
            model_path = os.path.join(self.data_dir, "trainer.yml")
            self.recognizer.write(model_path)
            self.is_trained = True
            return True
        
        return False

    def authenticate(self) -> Tuple[bool, Optional[int], float]:
        """
        Authentifier l'utilisateur via la webcam.
        Retourne: (success, user_id, confidence)
        """
        if not self.is_trained:
            print("[FaceID] ⚠️ Modèle non entraîné.")
            return False, None, 0.0

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[FaceID] ❌ Caméra non détectée.")
            return False, None, 0.0

        print("[FaceID] Authentification en cours...")
        
        start_time = time.time()
        timeout = 5 # 5 secondes pour authentifier
        
        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            if not ret: break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                user_id, loss = self.recognizer.predict(gray[y:y+h, x:x+w])
                
                # Pour LBPH, loss < 100 est généralement correct, plus c'est bas, mieux c'est
                # On convertit en score de confiance (0-1)
                confidence = max(0, (100 - loss) / 100)
                
                if confidence > 0.6: # Seuil de confiance
                    print(f"[FaceID] ✅ Utilisateur reconnu: {user_id} (Confiance: {confidence:.2f})")
                    cap.release()
                    return True, user_id, confidence
            
            time.sleep(0.1)

        cap.release()
        print("[FaceID] ❌ Authentification échouée (Timeout ou inconnu).")
        return False, None, 0.0

    def get_status(self) -> Dict[str, Any]:
        """État du service"""
        return {
            "ready": self.is_trained,
            "cascade_loaded": not self.face_cascade.empty(),
            "data_dir": self.data_dir
        }

# Instance globale
face_service = FaceRecognitionService()
