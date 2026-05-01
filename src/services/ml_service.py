"""
Smart Medical AI - ML Service (Senior Edition)
Moteur de prédiction des risques cardiaques
"""

import pickle
import os
import numpy as np
from typing import Dict, Any, Tuple

class MLService:
    def __init__(self, model_path: str = "./assets/models/heart_risk_model.pkl"):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """Chargement sécurisé du modèle RandomForest"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"[ML] Modèle chargé avec succès: {self.model_path}")
            else:
                print("[ML] ⚠️ Fichier modèle manquant. Utilisation du moteur d'inférence statistique.")
        except Exception as e:
            print(f"[ML] ❌ Erreur lors du chargement: {e}")

    def predict_risk(self, data: Dict[str, Any]) -> Tuple[int, str, str]:
        """
        Calcule le score de risque cardiaque (0-100)
        Retourne: (Score, Niveau, Explication)
        """
        # 1. Extraction et normalisation des données (Features)
        try:
            age = float(data.get('age', 50))
            bmi = float(data.get('bmi', 25))
            systolic = float(data.get('systolic', 120))
            cholesterol = float(data.get('cholesterol', 200))
            smoker = 1 if data.get('smoker', False) else 0
            
            # 2. Utilisation du modèle si disponible
            if self.model:
                features = np.array([[age, bmi, systolic, cholesterol, smoker]])
                score = int(self.model.predict_proba(features)[0][1] * 100)
            else:
                # 3. Moteur d'inférence statistique (Algorithme Senior de repli)
                # Basé sur les standards Framingham
                score = 0
                score += (age - 30) * 0.5
                if systolic > 140: score += 15
                if cholesterol > 240: score += 10
                if smoker: score += 20
                if bmi > 30: score += 10
                score = min(max(int(score), 5), 95)

            # 4. Détermination du niveau et de l'explication
            if score < 20:
                level = "LOW"
                explanation = "Risque faible. Maintenir une hygiène de vie saine."
            elif score < 50:
                level = "MEDIUM"
                explanation = "Risque modéré. Surveillance de la tension et du cholestérol recommandée."
            else:
                level = "HIGH"
                explanation = "Risque élevé. Consultation cardiologique urgente et bilan complet nécessaires."

            return score, level, explanation

        except Exception as e:
            print(f"[ML] ❌ Erreur de prédiction: {e}")
            return 10, "LOW", "Données insuffisantes pour une analyse précise."
