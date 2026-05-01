"""
Smart Medical AI - Application Core
QApplication singleton avec initialisation complète (Compatible Multi-Qt)
"""

import sys
import os
from pathlib import Path

from ..utils.qt_compat import QtWidgets, QtCore, QtGui

from .database import DatabaseManager
from .security import SecurityManager
from .events import EventBus, EventType


class SmartMedicalApp(QtWidgets.QApplication):
    """
    Application principale Smart Medical AI.
    """
    _instance = None

    def __new__(cls, argv=None):
        if cls._instance is None:
            # Définir la politique High DPI AVANT la création de l'instance pour PySide6
            if hasattr(QtCore.Qt.HighDpiScaleFactorRoundingPolicy, "PassThrough"):
                QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
                    QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
                )
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, argv=None):
        if argv is None:
            argv = sys.argv
        super().__init__(argv)

        self.setApplicationName("Smart Medical AI")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("DrDidier")

        self.db: DatabaseManager = None
        self.security: SecurityManager = None
        self.events: EventBus = None
        self.current_user = None

        self._initialized = False

    def initialize(self) -> bool:
        if self._initialized:
            return True

        try:
            print("[App] Initialisation Smart Medical AI...")
            self.db = DatabaseManager()
            self.security = SecurityManager()
            self.events = EventBus()
            self._load_stylesheet()
            self._configure_fonts()

            self._initialized = True
            return True

        except Exception as e:
            print(f"[App] ERREUR initialisation: {e}")
            return False

    def _load_stylesheet(self) -> None:
        style_path = Path(__file__).parent.parent.parent / "config" / "styles.qss"
        if style_path.exists():
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def _configure_fonts(self) -> None:
        font = QtGui.QFont("Segoe UI", 10)
        font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
        self.setFont(font)

    def set_current_user(self, user_data: dict) -> None:
        self.current_user = user_data
        if user_data:
            self.events.emit(EventType.USER_LOGIN, user_data)

    def logout(self) -> None:
        if self.current_user:
            self.events.emit(EventType.USER_LOGOUT, self.current_user)
            self.current_user = None

    @classmethod
    def get_instance(cls) -> "SmartMedicalApp":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def create_app() -> SmartMedicalApp:
    app = SmartMedicalApp()
    app.initialize()
    return app
