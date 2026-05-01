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
                print("[ML] ⚠️ Fichier modèle manquant. Initialisation requise.")
        except Exception as e:
            print(f"[ML] ❌ Erreur lors du chargement: {e}")

    def train_initial_model(self, data_samples: list = None) -> bool:
        """Entraîner un modèle initial avec des données synthétiques (Framingham-like)"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Si pas de données, on génère un dataset synthétique réaliste
        if data_samples is None:
            print("[ML] Génération de données synthétiques pour l'entraînement...")
            X = []
            y = []
            for _ in range(1000):
                age = np.random.randint(20, 90)
                bmi = np.random.randint(18, 45)
                systolic = np.random.randint(90, 200)
                cholesterol = np.random.randint(150, 350)
                smoker = np.random.randint(0, 2)
                
                # Logique de risque simplifiée pour le dataset synthétique
                risk_score = (age - 30) * 0.1 + (systolic - 120) * 0.2 + (cholesterol - 200) * 0.1 + smoker * 5 + (bmi - 25) * 0.5
                risk_prob = 1 / (1 + np.exp(-0.1 * (risk_score - 10))) # Sigmoïde
                
                X.append([age, bmi, systolic, cholesterol, smoker])
                y.append(1 if np.random.random() < risk_prob else 0)
            
            X = np.array(X)
            y = np.array(y)
        else:
            X = np.array([s[:5] for s in data_samples])
            y = np.array([s[5] for s in data_samples])

        print("[ML] Entraînement du RandomForestClassifier...")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Sauvegarde
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"[ML] Modèle sauvegardé dans {self.model_path}")
        return True

    def predict_risk(self, data: Dict[str, Any]) -> Tuple[int, str, str]:
        """
        Calcule le score de risque cardiaque (0-100) via RandomForest
        Retourne: (Score, Niveau, Explication)
        """
        if not self.model:
            # Fallback temporaire si pas de modèle
            return self._fallback_prediction(data)

        try:
            # 1. Extraction des features (Age, BMI, Systolic BP, Cholesterol, Smoker)
            age = float(data.get('age', 50))
            bmi = float(data.get('bmi', 25))
            systolic = float(data.get('systolic', 120))
            cholesterol = float(data.get('cholesterol', 200))
            smoker = 1 if data.get('smoker', False) else 0
            
            features = np.array([[age, bmi, systolic, cholesterol, smoker]])
            
            # 2. Prédiction de probabilité
            prob = self.model.predict_proba(features)[0][1]
            score = int(prob * 100)

            # 3. Détermination du niveau et de l'explication
            if score < 15:
                level = "LOW"
                explanation = "Risque très faible. Excellents indicateurs."
            elif score < 40:
                level = "LOW"
                explanation = "Risque faible. Maintenir une surveillance annuelle."
            elif score < 70:
                level = "MEDIUM"
                explanation = "Risque modéré. Modification de l'hygiène de vie et suivi régulier recommandés."
            else:
                level = "HIGH"
                explanation = "Risque élevé. Intervention cardiologique et traitement préventif nécessaires."

            return score, level, explanation

        except Exception as e:
            print(f"[ML] ❌ Erreur de prédiction: {e}")
            return self._fallback_prediction(data)

    def _fallback_prediction(self, data: Dict[str, Any]) -> Tuple[int, str, str]:
        """Algorithme statistique de repli (Framingham-like)"""
        age = float(data.get('age', 50))
        systolic = float(data.get('systolic', 120))
        cholesterol = float(data.get('cholesterol', 200))
        smoker = 1 if data.get('smoker', False) else 0
        
        score = 0
        score += (age - 30) * 0.4
        if systolic > 140: score += 12
        if cholesterol > 240: score += 8
        if smoker: score += 15
        
        score = min(max(int(score), 5), 95)
        level = "LOW" if score < 30 else ("MEDIUM" if score < 65 else "HIGH")
        return score, level, "Résultat basé sur l'analyse statistique (modèle ML non chargé)."
