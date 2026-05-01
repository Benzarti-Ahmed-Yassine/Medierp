import pytest
import os
from src.services.face_service import FaceRecognitionService

class TestBiometricService:
    @pytest.fixture
    def service(self):
        return FaceRecognitionService(data_dir="./tests/temp_biometrics")

    def test_service_initialization(self, service):
        """Test l'initialisation du service"""
        status = service.get_status()
        assert "ready" in status
        assert "data_dir" in status
        assert status["data_dir"] == "./tests/temp_biometrics"

    def test_status_reporting(self, service):
        """Test le rapport d'état"""
        status = service.get_status()
        assert isinstance(status, dict)
        assert "cascade_loaded" in status

    def test_directory_creation(self, service):
        """Vérifie que le dossier de données est créé"""
        assert os.path.exists("./tests/temp_biometrics")
        
    @classmethod
    def teardown_class(cls):
        """Nettoyage après les tests"""
        import shutil
        if os.path.exists("./tests/temp_biometrics"):
            shutil.rmtree("./tests/temp_biometrics")
