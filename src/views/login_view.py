"""
Smart Medical AI - Professional Login (Senior Developer Edition)
Design & Logique alignés sur MediERP
"""

import os
from ..utils.qt_compat import QtWidgets, QtCore, QtGui, uic
from ..core.security import SecurityManager

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connexion - MediERP")
        self.setFixedSize(450, 600)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Overlay ultra-clair au lieu de sombre
        self.setStyleSheet("QDialog { background-color: rgba(255, 255, 255, 0.6); }")

        
        self.security = SecurityManager()
        self.user_data = None
        self._setup_ui()

    def _setup_ui(self):
        # Frame principale (Container arrondi)
        self.container = QtWidgets.QFrame(self)
        self.container.setObjectName("MainContainer")
        self.container.setGeometry(25, 25, 400, 550)
        self.container.setStyleSheet("""
            QFrame#MainContainer {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e8e8e8;
            }
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #d9d9d9;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                background-color: #ffffff;
            }
        """)
        
        # Effet d'ombre (Drop Shadow)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)
        
        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(40, 50, 40, 50)
        layout.setSpacing(18)

        # 1. Logo & Titre
        lbl_icon = QtWidgets.QLabel("➕")
        lbl_icon.setStyleSheet("font-size: 40pt; color: #1890ff;")
        lbl_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_icon)

        lbl_title = QtWidgets.QLabel("MediERP")
        lbl_title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #001529;")
        lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_subtitle = QtWidgets.QLabel("Système de gestion médicale")
        lbl_subtitle.setStyleSheet("color: #8c8c8c; margin-bottom: 20px;")
        lbl_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_subtitle)

        # 2. Champs Saisie
        self.txtEmail = QtWidgets.QLineEdit()
        self.txtEmail.setPlaceholderText("✉️ Email professionnel")
        self.txtEmail.setFixedHeight(48)
        layout.addWidget(self.txtEmail)

        self.txtPassword = QtWidgets.QLineEdit()
        self.txtPassword.setPlaceholderText("🔑 Mot de passe")
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPassword.setFixedHeight(48)
        layout.addWidget(self.txtPassword)

        # 3. Boutons
        layout.addSpacing(10)
        self.btnLogin = QtWidgets.QPushButton("🚀 Se connecter")
        self.btnLogin.setObjectName("btnPrimary")
        self.btnLogin.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        self.btnLogin.setFixedHeight(48)
        self.btnLogin.clicked.connect(self._on_login)
        layout.addWidget(self.btnLogin)

        self.btnFaceID = QtWidgets.QPushButton("📷 Face ID")
        self.btnFaceID.setStyleSheet("""
            QPushButton {
                background-color: #ffffff; 
                color: #1890ff; 
                border: 1px solid #1890ff;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
            }
        """)
        self.btnFaceID.setFixedHeight(48)
        self.btnFaceID.clicked.connect(self._on_face_id)
        layout.addWidget(self.btnFaceID)

        layout.addStretch()
        
        self.lblStatus = QtWidgets.QLabel("")
        self.lblStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lblStatus)

    def _on_login(self):
        email = self.txtEmail.text().strip()
        password = self.txtPassword.text()
        
        result = self.security.authenticate(email, password)
        if result:
            self.user_data = result
            self.accept()
        else:
            self.lblStatus.setText("❌ Identifiants incorrects")
            self.lblStatus.setStyleSheet("color: #ff4d4f;")

    def _on_face_id(self):
        self.lblStatus.setText("📷 Analyse faciale...")
        QtCore.QTimer.singleShot(1500, self._process_face_id)

    def _process_face_id(self):
        result = self.security.authenticate_face()
        if result:
            self.user_data = result
            self.accept()
        else:
            self.lblStatus.setText("❌ Reconnaissance échouée")

    def get_user(self) -> dict:
        return self.user_data or {}

class PatientLoginDialog(QtWidgets.QDialog):
    """Espace Patient - Design MediERP"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Espace Patient - MediERP")
        self.setFixedSize(450, 500)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self._setup_ui()

    def _setup_ui(self):
        self.container = QtWidgets.QFrame(self)
        self.container.setGeometry(25, 25, 400, 450)
        self.container.setStyleSheet("background-color: white; border-radius: 20px;")
        
        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(40, 40, 40, 40)
        
        lbl_icon = QtWidgets.QLabel("👤")
        lbl_icon.setStyleSheet("font-size: 40pt; color: #52c41a;")
        lbl_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_icon)

        lbl_title = QtWidgets.QLabel("Espace Patient")
        lbl_title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #001529;")
        lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)
        
        self.txtCin = QtWidgets.QLineEdit()
        self.txtCin.setPlaceholderText("Votre CIN (ex: AB123456)")
        self.txtCin.setFixedHeight(45)
        layout.addWidget(self.txtCin)
        
        self.btnConnect = QtWidgets.QPushButton("Accéder à mon dossier")
        self.btnConnect.setStyleSheet("background-color: #52c41a; color: white; font-weight: bold;")
        self.btnConnect.setFixedHeight(45)
        self.btnConnect.clicked.connect(self.accept)
        layout.addWidget(self.btnConnect)
        
        layout.addStretch()
        
        btn_close = QtWidgets.QPushButton("Retour")
        btn_close.clicked.connect(self.reject)
        layout.addWidget(btn_close)
