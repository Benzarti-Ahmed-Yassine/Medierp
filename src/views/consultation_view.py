"""
Smart Medical AI - Consultation View (AI Integrated)
"""

from ..utils.qt_compat import QtWidgets, QtCore, uic
from ..services.ml_service import MLService
from ..services.voice_service import VoiceService
from ..core.app import SmartMedicalApp
import os

class ConsultationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = SmartMedicalApp.get_instance()
        
        # Initialisation Services
        self.ml = MLService()
        self.voice = VoiceService()
        
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "consultation.ui")
        uic.loadUi(ui_path, self)
        
        self._connect_signals()

    def _connect_signals(self):
        # Dictée Vocale
        if hasattr(self, "btnVoice"):
            self.btnVoice.clicked.connect(self._toggle_voice)
        self.voice.transcription_ready.connect(self._on_voice_transcription)
        self.voice.status_changed.connect(self._on_voice_status)

        # Analyse IA
        if hasattr(self, "btnAnalyze"):
            self.btnAnalyze.clicked.connect(self._on_analyze)

    def _toggle_voice(self):
        if not self.voice.is_listening:
            self.voice.start_listening()
        else:
            self.voice.stop_listening()

    def _on_voice_transcription(self, text):
        if hasattr(self, "txtNotes"):
            current = self.txtNotes.toPlainText()
            self.txtNotes.setPlainText(current + "\n" + text)

    def _on_voice_status(self, status):
        if hasattr(self, "lblVoiceStatus"):
            self.lblVoiceStatus.setText(status)

    def _on_analyze(self):
        """Déclenche la prédiction IA"""
        # Récupération des données depuis les champs (ex: Tension, Age)
        data = {
            "age": 65, # Exemple, à lier au patient sélectionné
            "bmi": 28,
            "systolic": 155,
            "cholesterol": 240,
            "smoker": True
        }
        
        score, level, explanation = self.ml.predict_risk(data)
        
        # Mise à jour de l'UI
        if hasattr(self, "lblRiskScore"):
            self.lblRiskScore.setText(f"{score}%")
        if hasattr(self, "lblRiskLevel"):
            self.lblRiskLevel.setText(level)
            color = "#ff4d4f" if level == "HIGH" else "#faad14" if level == "MEDIUM" else "#52c41a"
            self.lblRiskLevel.setStyleSheet(f"font-weight: bold; color: {color};")
        if hasattr(self, "txtAIExplanation"):
            self.txtAIExplanation.setText(explanation)
