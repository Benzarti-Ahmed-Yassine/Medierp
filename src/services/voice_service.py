"""
Smart Medical AI - Voice Service (Senior Edition)
Service de dictée vocale pour consultation
"""

import threading
from ..utils.qt_compat import QtCore

class VoiceService(QtCore.QObject):
    # Signaux pour communiquer avec l'interface Qt
    transcription_ready = QtCore.Signal(str)
    status_changed = QtCore.Signal(str)
    error_occurred = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.is_listening = False
        self._recognizer = None
        self._setup_recognizer()

    def _setup_recognizer(self):
        """Initialisation de l'API de reconnaissance (Google Speech API via speech_recognition)"""
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._mic = sr.Microphone()
            print("[Voice] Moteur de reconnaissance vocale prêt.")
        except Exception as e:
            print(f"[Voice] ⚠️ Bibliothèques manquantes ou micro non détecté. Mode simulation activé.")
            self._recognizer = None

    def start_listening(self):
        """Lance l'écoute dans un thread séparé (Senior Non-Blocking UI)"""
        if self.is_listening: return
        
        self.is_listening = True
        self.status_changed.emit("🔴 Écoute en cours...")
        
        thread = threading.Thread(target=self._listen_process, daemon=True)
        thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.status_changed.emit("🎤 Dictée arrêtée.")

    def _listen_process(self):
        """Processus de reconnaissance (Background Thread)"""
        if self._recognizer is None:
            # Simulation si pas de micro/lib
            import time
            time.sleep(2)
            if self.is_listening:
                self.transcription_ready.emit("Ceci est une simulation de dictée vocale : Le patient présente des douleurs thoraciques depuis 24h.")
                self.stop_listening()
            return

        import speech_recognition as sr
        try:
            with self._mic as source:
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            if self.is_listening:
                text = self._recognizer.recognize_google(audio, language="fr-FR")
                self.transcription_ready.emit(text)
        except Exception as e:
            self.error_occurred.emit(f"Erreur vocale : {str(e)}")
        finally:
            self.stop_listening()
