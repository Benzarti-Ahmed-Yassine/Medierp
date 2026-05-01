import pytest
from src.services.ml_service import MLService

class TestMLService:
    @pytest.fixture
    def service(self):
        return MLService()

    def test_predict_low_risk(self, service):
        """Test prédiction risque faible"""
        data = {
            "age": 25,
            "bmi": 20,
            "systolic": 110,
            "cholesterol": 160,
            "smoker": False
        }
        score, level, explanation = service.predict_risk(data)
        assert score < 30
        assert level in ["LOW", "MEDIUM"] # Dépend de si le modèle est chargé ou non

    def test_predict_high_risk(self, service):
        """Test prédiction risque élevé"""
        data = {
            "age": 75,
            "bmi": 32,
            "systolic": 170,
            "cholesterol": 280,
            "smoker": True
        }
        score, level, explanation = service.predict_risk(data)
        assert score > 40
        assert level in ["MEDIUM", "HIGH"]

    def test_fallback_prediction(self, service):
        """Test l'algorithme de repli"""
        data = {
            "age": 60,
            "systolic": 150,
            "cholesterol": 250,
            "smoker": True
        }
        score, level, explanation = service._fallback_prediction(data)
        assert score > 0
        assert isinstance(score, int)
        assert level in ["MEDIUM", "HIGH"]
