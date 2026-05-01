"""
Smart Medical AI - Speech Service
Reconnaissance vocale et dictée
"""

import time
from typing import Optional, Callable
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

class SpeechService:
    """
    Service de gestion de la voix:
    - Dictée vocale (STT)
    - Synthèse vocale (TTS)
    """

    def __init__(self):
        self.recognizer = sr.Recognizer() if SPEECH_AVAILABLE else None
        self.engine = pyttsx3.init() if VOICE_AVAILABLE else None
        
        if self.engine:
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)

    def listen(self, callback: Optional[Callable[[str], None]] = None) -> str:
        """Écouter et convertir en texte"""
        if not SPEECH_AVAILABLE:
            return "Reconnaissance vocale non disponible (install speech_recognition)"

        print("[Voice] Écoute en cours...")
        # Simuler une dictée pour la démo
        time.sleep(2)
        text = "Le patient présente une légère hypertension et une fatigue chronique."
        
        if callback:
            callback(text)
        return text

    def speak(self, text: str) -> None:
        """Synthèse vocale"""
        if not VOICE_AVAILABLE:
            print(f"[Voice] TTS non disponible: {text}")
            return

        self.engine.say(text)
        self.engine.runAndWait()

# Instance globale
speech_service = SpeechService()
