"""
Smart Medical AI - MainWindow (Senior RBAC Edition)
Séparation des vues par rôle (Docteur Yassine, Secrétaire, Admin)
"""

from ..utils.qt_compat import QtWidgets, QtCore, QtGui
from .dashboard_view import DashboardWidget
from .patient_view import PatientListView
from .patient_detail_view import PatientDetailView
from .consultation_view import ConsultationWidget
from .extra_views import AgendaWidget, FacturationWidget, AdminDashboardWidget, SettingsWidget
from .components import AvatarLabel
from ..core.app import SmartMedicalApp

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = SmartMedicalApp.get_instance()
        self.user_data = self.app.current_user
        self.role = self.user_data.get('role', 'ASSISTANT')
        
        self._setup_ui()
        self._apply_role_permissions()
        self._connect_signals()

    def _setup_ui(self):
        self.setWindowTitle("MediERP - Système de Gestion Médicale")
        self.setMinimumSize(1400, 900)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. SIDEBAR
        self.nav_panel = QtWidgets.QFrame()
        self.nav_panel.setObjectName("nav_panel")
        self.nav_panel.setFixedWidth(260)
        nav_layout = QtWidgets.QVBoxLayout(self.nav_panel)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        lbl_logo = QtWidgets.QLabel("➕ MediERP")
        lbl_logo.setObjectName("lblLogo")
        nav_layout.addWidget(lbl_logo)

        self.btn_group = QtWidgets.QButtonGroup(self)
        self.nav_buttons = {}
        
        # Tous les menus possibles
        all_menus = [
            ("dashboard", "📊 Tableau de bord"),
            ("patients", "👥 Patients"),
            ("agenda", "📅 Rendez-vous"),
            ("consultation", "🩺 Consultation IA"),
            ("billing", "💰 Facturation"),
            ("admin", "🛡️ Administration"),
            ("settings", "⚙️ Paramètres")
        ]

        for key, label in all_menus:
            btn = QtWidgets.QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedHeight(55)
            nav_layout.addWidget(btn)
            self.btn_group.addButton(btn)
            self.nav_buttons[key] = btn

        nav_layout.addStretch()
        
        # Profil Utilisateur
        profile_frame = QtWidgets.QFrame()
        profile_frame.setStyleSheet("background-color: #f5f5f5; margin: 10px; border-radius: 10px; border: 1px solid #e8e8e8;")
        p_layout = QtWidgets.QHBoxLayout(profile_frame)
        self.side_avatar = AvatarLabel(size=35)
        self.side_avatar.set_photo(self.user_data.get('photo_path'))
        p_layout.addWidget(self.side_avatar)
        lbl_user = QtWidgets.QLabel(f"{self.user_data.get('full_name', 'User')}\n<small>{self.role}</small>")
        lbl_user.setStyleSheet("color: #262626; font-size: 9pt;")
        p_layout.addWidget(lbl_user)
        nav_layout.addWidget(profile_frame)

        main_layout.addWidget(self.nav_panel)

        # 2. CONTENT AREA
        content_area = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        header = QtWidgets.QFrame()
        header.setObjectName("header_bar")
        header.setFixedHeight(80)
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        name = self.user_data.get('full_name', 'Utilisateur').split()[-1]
        lbl_welcome = QtWidgets.QLabel(f"Bonjour, {name} 👋")
        lbl_welcome.setStyleSheet("font-size: 15pt; font-weight: 600; color: #262626;")
        header_layout.addWidget(lbl_welcome)
        header_layout.addStretch()
        
        search_bar = QtWidgets.QLineEdit()
        search_bar.setPlaceholderText("Rechercher...")
        search_bar.setFixedWidth(300)
        header_layout.addWidget(search_bar)
        
        content_layout.addWidget(header)

        self.stack = QtWidgets.QStackedWidget()
        self.views = {
            "dashboard": DashboardWidget(),
            "patients": PatientListView(),
            "patient_detail": PatientDetailView(),
            "agenda": AgendaWidget(),
            "consultation": ConsultationWidget(),
            "billing": FacturationWidget(),
            "admin": AdminDashboardWidget(),
            "settings": SettingsWidget()
        }
        for view in self.views.values():
            self.stack.addWidget(view)
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_area)

        self.nav_buttons["dashboard"].setChecked(True)

    def _apply_role_permissions(self):
        """Masquer les menus selon le rôle"""
        role_map = {
            "DOCTOR": ["dashboard", "patients", "agenda", "consultation", "settings"],
            "ASSISTANT": ["dashboard", "patients", "agenda", "billing"],
            "ADMIN": ["dashboard", "admin", "settings"]
        }
        
        allowed = role_map.get(self.role, ["dashboard"])
        for key, btn in self.nav_buttons.items():
            btn.setVisible(key in allowed)

    def _connect_signals(self):
        for key, btn in self.nav_buttons.items():
            btn.clicked.connect(lambda checked, k=key: self._switch_view(k))

    def _switch_view(self, key):
        self.stack.setCurrentWidget(self.views[key])

    def open_patient_dossier(self, patient_id):
        """Méthode globale pour ouvrir la fiche détaillée d'un patient"""
        detail_view = self.views["patient_detail"]
        detail_view.load_patient(patient_id)
        self.stack.setCurrentWidget(detail_view)
        
        # Deselect sidebar buttons visually if not in 'patients' tab
        self.nav_buttons["patients"].setChecked(True)
